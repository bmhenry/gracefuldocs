"""Inspects a module and prints the docs for the module and its members"""

import inspect, importlib, re, sys, os


"""
TODO:

check if the module is a directory
 if so, search for .py files and directories inside
 import each and inspect them
"""


class Inspector:
    """
    Inspects a mainpath file or directory and then returns a dictionary
    containing the package or module's information.
    """


    def __init__(mainpath):

        self.mainpath = mainpath
        self.module_info = []
        
        # make sure the file/folder exists
        if not os.path.exists(mainpath):
            print("Couldn't find the specified path.")
            return

        # this regex will find anything like '__init__' or '__repr__', etc.
        self.regex = re.compile('__(\S+)__')

        if os.path.isdir(mainpath):
            # a directory was given.
            self.titlename =  os.path.split(mainpath)[1]

            module_paths = []
            for root, dirs, files in os.walk(mainpath):
                for file in files:
                    fname, fext = os.path.splitext(file)
                    if fext == '.py' and not regex.match(fname):
                        modules.append(os.path.join(root, file))

            for module in module_paths:
                mod_dict = self.inspect_module(module)
                if mod_dict is not None:
                    self.module_info.append(mod_dict)

        elif os.path.isfile(mainpath):
            self.module_info.append(self.inspect_module(mainpath))
            self.titlename = self.module_info[0]["name"]

        else:
            print("Couldn't find a Python module at the given path.")
            return


    def inspect_module(module_path):
        """
        Inspects a single module, getting information on classes, functions,
        and the module itself.
        """

        # fix import path to use working directory instead of gracefuldocs folder
        store_path = sys.path[0]
        sys.path[0] = os.getcwd()

        try:
            cur_module = importlib.import_module(module_path)
            module_name = cur_module.__name__
        except Exception as e:
            print("Couldn't import module " + module_name + ". Is it in your current directory or Python path?")
            return None

        # return import path to what it was before
        sys.path[0] = store_path

        # the format for documenting a module
        docs = { "name" : "" , "docstring" : "", "classes": [], "functions" : [] }

        # get the docstring for the module
        docs["docstring"] = cur_module.__doc__

        # inspect the members of the module
        self.inspect_members(module_name, docs)

        pass


    def inspect_members(parent_name, docs, *, c_or_f = False):
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
                if eval('inspect.isclass(' + member_namepath + ')'):
                    docs['classes'].append(inspect_class(member_namepath))
                elif eval('inspect.isfunction(' + member_namepath + ')'):
                    docs['functions'].append(inspect_function(member_namepath))

        pass


    def inspect_class(class_name):
        """Inspects a class for docs, subclasses, and subfunctions"""

        docs = { "name" : "" , "docstring" : "", "classes": [], "functions" : [] }
        docs['name'] = eval(class_name + '.__name__')
        docs['docstring'] = eval(class_name + '.__doc__')

        self.inspect_members(class_name, docs)

        pass


    def inspect_function(fn_name):
        """Inspects a function for docs, subclasses, and subfunctions"""

        docs = { "name" : "" , "docstring" : "", "classes": [], "functions" : [] }
        docs['name'] = eval(fn_name + '.__name__')
        docs['docstring'] = eval(fn_name + '.__doc__')

        self.inspect_members(fn_name, docs)

        pass