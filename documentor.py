import os, re, sys, webbrowser
from inspector import Inspector
import web_base.html as ghtml



def forcedir(dir_path):
    """Makes sure that a directory exists"""
    print(dir_path)
    subdirs = dir_path.strip().split('\\')
    print(subdirs)
    for path in range(len(subdirs)):
        new_path = '\\'.join(subdirs)
        print("%" + new_path + "%")
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
    pass


def doc_class(classdict):
    """Documents a class recursively, calling itself if necessary"""
    
    sidebar = ""
    html = {}

    return (html, )


def documentor(module):
    """Obtains documentation for the module given"""

    sidebar = ""

    fulldata = Inspector(module).docs
    modulename = [name for name in fulldata][0]
    moduledata = fulldata[modulename]

    html = {"index.html": ghtml.generate_index(modulename, moduledata['docstring']),
            "style.css" : ghtml.get_css(),
            "gracefuldocs.html" : ghtml.get_gd()}


    footer = ghtml.generate_footer(modulename)

    if sidebar:
        sidebar += '\n<div style="height: 5vh"></div>'

    base = ghtml.fill_base(title = modulename, sidebar = sidebar, footer = footer)

    for key in html:
        if key == 'style.css':
            continue
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