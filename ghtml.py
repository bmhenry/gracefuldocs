import os, sys, time

# Directory functions:

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


# HTML from templates functions

def get_base():
    """Returns the base html page as text"""
    with open(html_dir() + 'base_page.html', 'r') as page:
        return page.read()


def get_css():
    """Gets the CSS stylesheet and returns it as text"""
    with open(html_dir() + 'style.css', 'r') as css:
        return css.read()


def get_info():
    """Gets the base html page for a class/function and returns it as text"""
    with open(html_dir() + 'element_info.html') as info:
        return info.read()


def get_gd():
    """Gets the 'About' page for GracefulDocs and returns it as text"""
    with open(html_dir() + 'gracefuldocs_about.html') as g:
        return g.read()


# Fill templates functions

def fill_base(*, title = "{title}", body = "{body}", sidebar = "{sidebar}", footer = "{footer}"):
    """Gets the base html page and fills it with the given information"""
    base = get_base()
    base = base.format(title = title, 
                       sidebar = sidebar, 
                       body = body, 
                       footer = footer)

    return base


def fill_info(*, name = "{name}", type = "{type}", args = "{args}", classes = "{classes}", functions = "{functions} "):
    """Gets the base html page for a class/function and fills it with the given information"""
    info = get_info()
    info = info.format( name = name, 
                        args = args, 
                        classes = classes, 
                        functions = functions )

    return info


def generate_index(modulename, docstring):
    """Creates the index page for the documentation"""
    html = '<h3><i>{title}:</i></h3><hr/>\n<p class="bodytext">{doc}</p>\n'
    return html.format(title = modulename, doc = docstring)


def generate_footer(modulename):
    """Creates the footer for the bottom of the pages using the module name"""
    curtime = time.localtime()
    time_string = str(curtime.tm_mon) + "/" + str(curtime.tm_mday) + "/" + str(curtime.tm_year)
    return_string = "<p>" + modulename + " documentation generated on " + time_string + "</p>" 
    return_string += "<p>Written in Python</p>"
    
    return return_string

def generate_nav_link(element_name):
    sidebar_string = "<li class='sb_el_link'><a href='elements/{element_name}.html'>{element_name}</a></li>".format(element_name = element_name)
    return sidebar_string