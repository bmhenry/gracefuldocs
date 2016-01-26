import os, sys, time


def forcedir(dir_path):
    """Makes sure that a directory exists"""

    subdirs = dir_path.strip().split('\\')
    for path in range(len(subdirs)):
        new_path = '\\'.join(subdirs)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
    pass


def html_dir():
    """Returns an absolute path to the location of the html base folder"""
    return os.path.abspath(sys.path[0]) + '/web_base/'


def get_base():
    """Returns the base html page as text"""
    with open(html_dir() + 'base_page.html', 'r') as page:
        return page.read()


def fill_base(*, title = "{title}", body = "{body}", sidebar = "{sidebar}", footer = "{footer}"):
    """Gets the base html page and fills it with the given information"""
    base = get_base()
    base = base.format(title = title, 
                       sidebar = sidebar, 
                       body = body, 
                       footer = footer)

    return base


def get_css():
    """Gets the CSS stylesheet and returns it as text"""
    with open(html_dir() + 'style.css', 'r') as css:
        return css.read()


def get_info():
    """Gets the base html page for a class/function and returns it as text"""
    with open(html_dir() + 'element_info.html') as info:
        return info.read()


def fill_info(*, name = "{name}", type = "{type}", args = "{args}", classes = "{classes}", functions = "{functions} "):
    """Gets teh base html page for a class/function and fills it with the given information"""
    info = get_info()
    info = info.format( name = name, 
                        args = args, 
                        classes = classes, 
                        functions = functions )

    return info


def fill_sidebar(*, name = "{name}", module = "{module}"):
    """Returns a list element for the sidebar using the given input information"""
    if name == module:
        html = '<li><a class="sbmodule" href="{module}/{name}.html"</a>{name}</li>\n'
    else:
        html = '<li><a class="sbelement" href="{module}/{name}.html"</a>{name}</li>\n'

    return html.format(name = name, module = module)


def get_gd():
    """Gets the 'About' page for GracefulDocs and returns it as text"""
    with open(html_dir() + 'gracefuldocs_about.html') as g:
        return g.read()


def element_entry(name, modulename):
    html = "<li><a class='element_list_entry' href='{modulename}/{name}.html'>{name}</a></li>\n"
    return html.format(name = name, modulename = modulename)


def generate_index(modulename, docstring):
    """Creates the index page for the documentation"""
    html = '<h3><i>{title}:</i></h3><hr/>\n<p class="bodytext">{doc}</p>\n'
    return html.format(title = modulename, doc = docstring)


def generate_footer(modulename):
    """Creates the footer for the bottom of the pages using the module name"""
    curtime = time.localtime()
    return "<p>" + modulename + " documentation generated on " \
                      + str(curtime.tm_mon) + "/" + str(curtime.tm_mday) \
                      + "/" + str(curtime.tm_year) \
                      + "</p><p>Written in Python</p>"