import inspect, importlib, re

__doc__ = """Inspects a module and prints the docs for the module and its members"""

class Inspector:
    """
    dict = {moduleName: (docstring,
                         dict{classes: { class name : {docstring, subclass dict, method dict}},
                         dict{functions: { function name : {docstring, parameters w/ defaults}} }
    """
    def __init__(self, moduleName):
        try:
            globals()[moduleName] = importlib.import_module(moduleName)
        except Exception as e:
            print("Couldn't import module. Is it in your current directory or Python path?")
            return None

        self.docs = { moduleName: {'docstring': eval('inspect.getdoc(' + moduleName + ')'),
                                   'classes': {}, 
                                   'functions': {}
                                  }
                    }
        self.moduleName = moduleName

        members = eval('dir(' + moduleName + ')')

        regex = re.compile('__(\S+)__')
        for m in members:
            print(m)
            if regex.match(m):
                continue
            item = moduleName + '.' + m
            if eval('inspect.isclass(' + item + ')'):
                self.docs[moduleName]['classes'].update(self.inspect_class(item))
            elif eval('inspect.isfunction(' + item + ')'):
                self.docs[moduleName]['functions'].update(self.inspect_function(item))
            
        pass


    def inspect_class(self, class_str):
        print(class_str)
        members = eval('dir(' + class_str + ')')
        class_name = eval(class_str + '.__name__')
        docs = {class_name: {'docstring': eval('inspect.getdoc(' + class_str + ')'),
                                               'classes': {},
                                               'functions': {}
                                              }
                }

        regex = re.compile('__(\S+)__')
        for m in members:
            if regex.match(m):
                continue
            new_item = class_str + '.' + m
            if eval('inspect.isclass(' + new_item + ')'):
                docs[class_name]['classes'].update(self.inspect_class(new_item))
            elif eval('inspect.isfunction(' + new_item + ')'):
                docs[class_name]['functions'].update(self.inspect_function(new_item))


        return docs


    def inspect_function(self, fn_str):
        print(fn_str)
        function_name = eval(fn_str + '.__name__')
        docs = {function_name: {'docstring': eval('inspect.getdoc(' + fn_str + ')'),
                                'parameters': {}
                                }
                }
                
        return docs


    def print_docs(self):
        print('Module ' + self.moduleName + ':')
        print(self.docs[self.moduleName]['classes'])
        print(self.docs[self.moduleName]['functions'])

        pass


def main():
    x = inspector(input('Module to inspect: '))
    x.print_docs()


if __name__ == '__main__':
    main()