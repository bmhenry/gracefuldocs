"""
Documents a module given the module name as an input.
Utilizes the Inspector function to get the documentation for the module,
then produces a static HTML site.
"""

import inspector
import ghtml

import code

"""
TODO:

- create the classes.html page and functions.html page

"""

def forcedir(dir_path):
    """Makes sure that a directory exists"""

    subdirs = dir_path.strip().split('\\')
    for path in range(len(subdirs)):
        new_path = '\\'.join(subdirs)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
    pass


def parse_args(args, defaults = []):
    """Takes the args and defaults dicts and puts them into a pretty string"""
    pass




class Documentor:
    """Obtains documentation for the package or module given"""

    def __init__(self, mainpath):
        mod_inspection = inspector.Inspector(mainpath)
        fulldata = mod_inspection.module_info

        if fulldata is None:
            print("Cancelled documentation creation.")
            exit()

        title = mod_inspection.titlename
        maindocs = mod_inspection.package_docs

        self._pages = { "index.html": ghtml.generate_index(titlename, fulldata),
                        "style.css" : ghtml.get_css(),
                        "classes.html" : "",
                        "functions.html" : "",
                        "gracefuldocs_about.html" : ghtml.gd() }
        
        self._sidebar = "<p><a href='index.html'><b>{title}</b></a></p>\n"
        self._sidebar += "<i>Modules:</i><ul>"

        # get each module stored in the package data
        for module in fulldata:
            # create a new folder for the module
            forcedir(outputpath + "/" + module["name"])

            # generate a page name for the module
            pagename = module["name"] + '/' + module['name'] + ".html"

            # generate a sidebar link for the module
            self._sidebar += ghtml.fill_sidebar(name = module['name'], module = module['name'])

            # get class info for the module
            for mclass in module['classes']:
                module_classes.append(mclass)
                self.doc_element(mclass, "class", module['name'] + '/')
            # get function info for the module
            for mfunc in module['functions']:
                module_functions.append(mfunc)
                self.doc_element(mfunc, "function", module['name'] + '/')

            # generate the page for the module
            self._pages[pagename] = ghtml.fill_info(name = module["name"], type = "Module", 
                args = module[''], docstring = module["docstring"], 
                classes = module_classes, functions = module_functions) 

        self._sidebar += "</ul>"


        footer = ghtml.generate_footer(modulename)

        sidebar = sidebar.format(title = modulename)
        if sidebar:
            sidebar += '\n<div style="height: 5vh"></div>'

        base = ghtml.fill_base(title = modulename, sidebar = sidebar, footer = footer)

        for page in self._pages:
            if page == 'style.css':
                continue
            #code.interact(local = locals())
            self._pages[page] = base.format(body = self._pages[page])


    def doc_element(name, element_type):
        """Documents an element recursively, calling itself if necessary"""

        if element_type == "class":
            element_type = "Class"
        elif element_type == "function":
            element_type = "Function"
        else:
            element_type = "Object"



        


def main():
    if len(sys.argv) > 1:
        modulename = sys.argv[1]
    else:
        modulename = input("Please enter module name to document:  ")

    if re.match("(-+)h | (-+)help | (\?+)", modulename.lower()):
        print("Module name must be in your Python path or current working directory")

    if len(sys.argv) > 2:
        outdir = sys.argv[2]
    else:
        outdir = input("Enter a folder for the HTML documentation to be written to (just '.' for current directory); enter '*quit' or '*q' to cancel:  ")

    if outdir.lower() in ['*quit']:
        exit()

    if not os.path.isdir(outdir):
        uin = input("This directory does not yet exist. Would you like to create it? (Y/N) ")

        if uin.lower() in "yes":
            forcedir(os.path.abspath(outdir))
        else:
            print("Cancelling doc creation...")
            exit()

    html = documentor(modulename, outdir)

    for page in html:
        with open(outdir + '/' + page, 'w') as doc:
            doc.write(html[page])

    u_open = input("Documenation written. Open in browser now? (Y/N) ")

    if u_open.lower() in ['y', 'yes']:
        webbrowser.open(url = os.path.abspath(outdir + '/index.html'), new = 2)

    pass

if __name__ == '__main__':
    main()