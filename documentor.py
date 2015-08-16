"""
Documents a module given the module name as an input.
Utilizes the Inspector function to get the documentation for the module,
then produces a static HTML site.
"""

import os, re, sys, webbrowser
from .inspector import Inspector
import html as ghtml

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


def documentor(module):
    """Obtains documentation for the module given"""

    fulldata = Inspector(module)

    if fulldata is None:
        print("Cancelled documentation creation.")
        exit()

    print(fulldata)
    pass
    
    modulename = [name for name in fulldata][0]
    moduledata = fulldata[modulename]

    sidebar = "<p><a href='index.html'><b>{title}</b></a></p>\n"
    sidebar += "<i>Classes:</i><ul>{classes}</ul>"
    sidebar += "<i>Functions:</i><ul>{fns}</ul>"

    s_classes = ''
    s_fns = ''

    html = {"index.html": ghtml.generate_index(modulename, moduledata['docstring']),
            "style.css" : ghtml.get_css(),
            "classes.html" : "",
            "functions.html" : "",
            "gracefuldocs_about.html" : ghtml.get_gd()}

    for class_ in moduledata['classes']:
        new = doc_element(class_, moduledata['classes'][class_], gen_sidebar = True)
        html.update(new[0])
        s_classes += new[1]
    for fn_ in moduledata['functions']:
        new = doc_element(fn_, moduledata['functions'][fn_], gen_sidebar = True)
        html.update(new[0])
        s_fns += new[1]


    footer = ghtml.generate_footer(modulename)

    sidebar = sidebar.format(title = modulename, classes = s_classes, fns = s_fns)
    if sidebar:
        sidebar += '\n<div style="height: 5vh"></div>'

    base = ghtml.fill_base(title = modulename, sidebar = sidebar, footer = footer)

    for key in html:
        if key == 'style.css':
            continue
        #code.interact(local = locals())
        html[key] = base.format(body = html[key])

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

    for key in html:
        with open(outdir + '/' + key, 'w') as doc:
            doc.write(html[key])

    u_open = input("Documenation written. Open in browser now? (Y/N) ")

    if u_open.lower() in ['y', 'yes']:
        webbrowser.open(url = os.path.abspath(outdir + '/index.html'), new = 2)

    pass

if __name__ == '__main__':
    main()