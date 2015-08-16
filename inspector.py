"""Inspects a module and prints the docs for the module and its members"""

import inspect, importlib, re, sys, os


"""
TODO:

check if the module is a directory
 if so, search for .py files and directories inside
 import each and inspect them
"""

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



def Inspector(module):
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