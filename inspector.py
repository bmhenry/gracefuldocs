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
                mod_dict = inspect_module(module)
                if mod_dict is not None:
                    self.module_info.append(mod_dict)

        elif os.path.isfile(mainpath):
            self.module_info.append(inspect_module(mainpath))
            self.titlename = self.module_info[0]["name"]

        else:
            print("Couldn't find a Python module at the given path.")
            return


    def inspect_module(modulepath):
        """
        Inspects a single module, getting information on classes, functions,
        and the module itself.
        """

        # fix import path to use working directory instead of gracefuldocs folder
        store_path = sys.path[0]
        sys.path[0] = os.getcwd()

        try:
            cur_module = importlib.import_module(modulepath)
            module_name = cur_module.__name__
        except Exception as e:
            print("Couldn't import module " + module_name + ". Is it in your current directory or Python path?")
            return None

        # return import path to what it was before
        sys.path[0] = store_path

        # the format for documenting a module
        docs = { "name" : "" , "docstring" : "", "classes": [], "functions" : [] }

        # get the docstring for the module
        docs["docstring"] = eval("inspect.getdoc(" + module_name + ")")

        # get the members of the module, getting the docs for each
        

        pass


    def add_members(name, regex, docs):
        # get members of module/submodule
        members = eval('dir(' + name + ')')

        # check each of the module's members and document if possible
        for m in members:
                # skip __init__, etc.
                if regex.match(m):
                    continue

                # document each member
                item = name + '.' + m
                if eval('inspect.isclass(' + item + ')'):
                    docs[1]['classes'].append(inspect_class(item, regex))
                elif eval('inspect.isfunction(' + item + ')'):
                    docs[1]['functions'].append(inspect_function(item))



def inspect(module):
    """
    Inspects a module and returns a dictionary containing the module's 
    information.
    """

    # fix import path to use working directory not gracefuldocs folder
    #  allows importing the module in question to be examined
    store_path = sys.path[0]
    sys.path[0] = os.getcwd()

    # attempt to import module
    try:
        temp = importlib.import_module(module)
        moduleName = temp.__name__
        globals()[moduleName] = temp
    except Exception as e:
        print("Couldn't import module. Is it in your current directory or Python path?")
        return None

    # return system path to where it was
    sys.path[0] = store_path

    # the format for documenting the module
    docs = ( moduleName, 
                    {
                        'docstring': eval('inspect.getdoc(' + moduleName + ')'),
                        'classes': [], 
                        'functions': []
                    }
                )

    # this regex will find anything like '__init__' or '__repr__', etc.
    regex = re.compile('__(\S+)__')

    # check each of the module's members and document it if needed
    add_members(moduleName, regex, docs)
        
    pass


def inspect_class(class_str, regex):
    """Inspects a class and returns a dict of info"""

    class_name = eval(class_str + '.__name__')
    docs = (class_name,
                {
                    'docstring': eval('inspect.getdoc(' + class_str + ')'),
                    'classes': [],
                    'functions': []
                }
            )

    add_members(class_name, regex, docs)


    return docs


def inspect_function(fn_str):
    """Inspects a function and returns a dict of info"""

    function_name = eval(fn_str + '.__name__')
    docs = (function_name,
                {
                    'docstring': eval('inspect.getdoc(' + fn_str + ')'),
                    'parameters': {},
                    'classes': {},
                    'functions': {}
                }
            )

    add_members(class_name, regex, docs)
            
    return docs