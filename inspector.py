"""Inspects a module and prints the docs for the module and its members"""

import re, sys, os
from inspect import isfunction, isclass, getfullargspec
from importlib import import_module


"""
TODO:

add imported module to globals

"""


class Inspector:
    """
    Inspects a mainpath file or directory and then returns a dictionary
    containing the package or module's information.
    """


    def __init__(self, mainpath):

        self.mainpath = mainpath
        self.module_info = []
        self.package_docs = None
        
        # make sure the file/folder exists
        if not os.path.exists(mainpath):
            print("Couldn't find the specified path.")
            self.module_info = None
            return

        # this regex will find anything like '__init__' or '__repr__', etc.
        self.regex = re.compile('__(\S+)__')

        # Is this path a directory (package) or a module?
        if os.path.isdir(mainpath):
            # a directory was given.
            self.directory, self.titlename =  os.path.split(mainpath)

            store_path = sys.path[0]
            sys.path[0] = self.directory
            
            try:
                # try to import as a package to get documentation
                package = import_module(mainpath)
                self.package_docs = package.__doc__
                globals()[package.__name__] = package
            except Exception:
                # oh well, just import the modules
                pass
            finally:
                # restore system path
                # ALWAYS NEEDS TO BE DONE
                sys.path[0] = store_path


            module_paths = []
            for root, dirs, files in os.walk(mainpath):
                for file in files:
                    fname, fext = os.path.splitext(file)
                    if fext == '.py' and not self.regex.match(fname):
                        module_paths.append((root,fname))

            print(module_paths)
            for module in module_paths:
                mod_dict = self.inspect_module(module)
                if mod_dict is not None:
                    self.module_info.append(mod_dict)

        elif os.path.isfile(mainpath):
            self.module_info.append(self.inspect_module(mainpath))
            self.titlename = self.module_info[0]["name"]

        else:
            print("Couldn't find a Python module at the given path.")
            self.module_info = None


    def inspect_module(self, module_path):
        """
        Inspects a single module, getting information on classes, functions,
        and the module itself.
        """

        # module_root is the python object/module path
        module_root = module_path[0]
        # module_name is the name of the module
        module_name = module_path[1]

        stringpath = module_root + '.' + module_name

        # fix import path to use working directory instead of gracefuldocs folder
        store_path = sys.path[0]
        sys.path[0] = module_root

        # make an attempt to import the module
        try:
            cur_module = import_module(stringpath)
            module_name = cur_module.__name__
            #globals()['module_name'] = cur_module
        except Exception as e:
            print("Error: " + str(e))
            print("Couldn't import module " + stringpath + ". Is it in your current directory or Python path?")
            return None
        finally:
            # return import path to what it was before
            # ALWAYS NEEDS TO BE DONE
            sys.path[0] = store_path

        # the format for documenting a module
        docs = { "name" : "" , "docstring" : "", "classes": [], "functions" : [] }

        # get the docstring for the module
        docs["docstring"] = cur_module.__doc__

        # inspect the members of the module
        self.inspect_members(module_name, docs)

        return docs


    def inspect_members(self, parent_name, docs, *, c_or_f = False):
        """Gets the members of a module/class/function and calls inspection on each"""

        # get members of module/submodule
        members = eval('dir(' + parent_name + ')')

        # check each of the module's members and document if possible
        for member in members:
            # skip __init__, etc.
            if self.regex.match(member) and not (c_or_f and member == "__init__"):
                continue

            # document each member
            member_namepath = parent_name + '.' + member
            if eval('isclass(' + member_namepath + ')'):
                docs['classes'].append(self.inspect_class(member_namepath))
            elif eval('isfunction(' + member_namepath + ')'):
                docs['functions'].append(self.inspect_function(member_namepath))

        pass


    def get_args(self, function_name):
        """Gets the arguments and default values for a function. Use the __init__() of a class to
        get class defaults"""

        argspec = getfullargspec(function_name)
        init_args = argspec.args
        init_vals = argspec.defaults

        return_args = []

        for index, arg in enumerate(init_args):
            subindex = len(init_args) -  len(init_vals)
            if index >= subindex:
                return_args.append((arg, init_vals[index - subindex]))
            else:
                return_args.append((arg))

        return return_args
        


    def inspect_class(self, class_name):
        """Inspects a class for docs, subclasses, and subfunctions"""

        docs = { "name" : "" , "docstring" : "", "classes": [], "functions" : [], "args" : [] }

        docs['name'] = eval(class_name + '.__name__')
        docs['docstring'] = eval(class_name + '.__doc__')

        docs['args'] = self.get_args(class_name + '.__init__')
        
        self.inspect_members(class_name, docs)

        return docs


    def inspect_function(self, fn_name):
        """Inspects a function for docs, subclasses, and subfunctions"""

        docs = { "name" : "" , "docstring" : "", "classes": [], "functions" : [] }

        docs['name'] = eval(fn_name + '.__name__')
        docs['docstring'] = eval(fn_name + '.__doc__')

        docs['args'] = self.get_args(fn_name)

        self.inspect_members(fn_name, docs)

        return docs