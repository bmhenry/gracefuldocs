import os, re, sys, webbrowser
import inspector



class documentor:
    """Obtains documentation for the module given"""

    def __init__(self, modulename):
        self.html = {"index.html": "<!doctype html>\n<html>\n<body>\n<p>Hello from " + modulename + ".</p>\n</body>\n</html>"}
        pass

    pass


def main():
    if len(sys.argv) > 1:
        modulename = sys.argv[1]
    else:
        modulename = input("Please enter module name to document:  ")

    if re.match("(-+)h | (-+)help | (\?+)", modulename.lower()):
        print("Module name must be in your Python path or current working directory")
    else:
        html = documentor(modulename).html

    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    else:
        outfile = input("Enter a folder for the HTML documentation to be written to, or enter #quit/#q to cancel:  ")

    if outfile.lower() in '#quit':
        exit()

    for key in html:
        with open(outfile + '/' + key, 'w') as doc:
            doc.write(html[key])

    u_open = input("Documenation written. Open in browser now? (Y/N)")

    if u_open.lower() in ['y', 'yes']:
        webbrowser.open(url = os.path.abspath(outfile + '/index.html'), new = 2)

    pass

if __name__ == '__main__':
    main()