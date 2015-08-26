import os, sys, time


def html_dir():
  return os.path.abspath(sys.path[0]) + '/web_base/'


def get_base(): 
    with open(html_dir() + 'base_page.html', 'r') as page:
        return page.read()


def fill_base(*, title = "{title}", body = "{body}", sidebar = "{sidebar}", footer = "{footer}"):
    base = get_base()
    base = base.format(title = title, 
                       sidebar = sidebar, 
                       body = body, 
                       footer = footer)

    return base


def get_css():
    with open(html_dir() + 'style.css', 'r') as css:
        return css.read()


def get_info():
    with open(html_dir() + 'element_info.html') as info:
        return info.read()


def fill_info(*, name = "{name}", type = "{type}", args = "{args}", classes = "{classes}", functions = "{functions} "):
    info = get_info()
    info = info.format( name = name, 
                        args = args, 
                        classes = classes, 
                        functions = functions )

    return info


def fill_sidebar(*, name = "{name}", module = "{module}"):
    if name == module:
        html = '<li><a class="sbmodule" href="{module}/{name}.html"</a>{name}</li>'
    else:
        html = '<li><a class="sbelement" href="{module}/{name}.html"</a>{name}</li>'

    return html.format(name = name, module = module)


def get_gd():
    with open(html_dir() + 'gracefuldocs_about.html') as g:
        return g.read()


def generate_index(modulename, docstring):
    html = '<h3><i>{title}:</i></h3><hr/>\n<p class="bodytext">{doc}</p>'
    return html.format(title = modulename, doc = docstring)


def generate_footer(modulename):
    curtime = time.localtime()
    return "<p>" + modulename + " documentation generated on " \
                      + str(curtime.tm_mon) + "/" + str(curtime.tm_mday) \
                      + "/" + str(curtime.tm_year) \
                      + "</p><p>Written in Python</p>"