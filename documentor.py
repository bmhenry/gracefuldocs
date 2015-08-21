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


def doc_element(name_, dict_, *, subdir = "", gen_sidebar = False):
    """Documents an element recursively, calling itself if necessary"""

    html = ""
    htmldict = {subdir + "/" + name_ + '.html': ''}
    sidebar = ''

    docstring = dict_['docstring']
    subclasses = dict_['classes']
    subfunctions = dict_['functions']

    html += ghtml.generate_index(name_, docstring)

    if gen_sidebar:
        sidebar = '<li><a href="{name}.html">{name}</a></li>'.format(name = name_)

    if subclasses:
        html += '<br/><br/><h4>Subclasses:</h4>\n'
        html += '<ul>\n'
        for class_ in subclasses:
            html += '<li><a href="{cname}.html">{cname}</a></li>'.format(cname = class_)
            htmldict.update(doc_element(class_, subclasses[class_])[0])
        html += '</ul>\n'
    if subfunctions:
        html += '<br/><br/><h4>Subfunctions:</h4>\n'
        for fn_ in subfunctions:
            html += '<li><a href="{fn}.html">{fn}</a></li>'.format(fn = fn_)
            htmldict.update(doc_element(fn_, subfunctions[fn_])[0])
        html += '</ul>\n'

    htmldict[name_ + '.html'] = html

    return (htmldict, sidebar)


def documentor(mainpath):
    """Obtains documentation for the package or module given"""

    mod_inspection = inspector.Inspector(mainpath)
    fulldata = mod_inspection.module_info

    if fulldata is None:
        print("Cancelled documentation creation.")
        exit()

    title = mod_inspection.titlename
    maindocs = mod_inspection.package_docs

    pages = {"index.html": ghtml.generate_index(titlename, fulldata),
             "style.css" : ghtml.get_css(),
             "classes.html" : "",
             "functions.html" : "",
             "gracefuldocs_about.html" : ghtml.gd()}
    
    sidebar = "<p><a href='index.html'><b>{title}</b></a></p>\n"
    sidebar += "<i>Modules:</i><ul>{modules}</ul>"

    s_classes = ''
    s_fns = ''
    s_modules = ''

    # get each module stored in the package data
    for module in fulldata:
        # generate a page name for the module
        pagename = module["name"] + ".html"

        # generate a sidebar link for the module
        s_modules += "<li>" + module['name'] + '</li>'

        # get class info for the module
        for mclass in module['classes']:
            module_classes.append(mclass)
            cdoc = doc_class(mclass)
            """TODO starts around here"""
        # get function info for the module
        for mfunc in module['functions']:
            module_functions.append(mfunc)

        # generate the page for the module
        pages[pagename] = ghtml.generate_modulepage(module["name"], module["docstring"], module_classes, module_functions)



    footer = ghtml.generate_footer(modulename)

    sidebar = sidebar.format(title = modulename, classes = s_classes, fns = s_fns)
    if sidebar:
        sidebar += '\n<div style="height: 5vh"></div>'

    base = ghtml.fill_base(title = modulename, sidebar = sidebar, footer = footer)

    for page in pages:
        if page == 'style.css':
            continue
        #code.interact(local = locals())
        html[page] = base.format(body = html[page])

    return html


def main():
    if len(sys.argv) > 1:
        modulename = sys.argv[1]
    else:
        modulename = input("Please enter module name to document:  ")

    if re.match("(-+)h | (-+)help | (\?+)", modulename.lower()):
        print("Module name must be in your Python path or current working directory")
    else:
        html = documentor(modulename)

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

    for page in html:
        with open(outdir + '/' + page, 'w') as doc:
            doc.write(html[page])

    u_open = input("Documenation written. Open in browser now? (Y/N) ")

    if u_open.lower() in ['y', 'yes']:
        webbrowser.open(url = os.path.abspath(outdir + '/index.html'), new = 2)

    pass

if __name__ == '__main__':
    main()