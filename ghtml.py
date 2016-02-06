import os, sys, time

# Directory functions:

def forcedir(dir_path):
	"""Makes sure that a directory exists"""

	# TODO: rewrite this to not try to do some sort of high level directory rewrite like a new T:/ or something

	# check if the path already exists
	if os.path.isdir(dir_path):
		return

	# if not, make all the required folders
	# get all the folders required to be made
	subdirs = []
	while dir_path != "":
		dir_path, folder = os.path.split(dir_path)

		if folder != "":
			subdirs.insert(0, folder)
		else:
			if dir_path != "":
				subdirs.insert(0, dir_path)
			break

	# check each path along the line and make sure it exists
	for path_combo in range(len(subdirs)):
		path = '/'.join(subdirs[0 : path_combo + 1])
		print(path)

		if not os.path.isdir(path):
			os.mkdir(path)

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

def fill_base(*, title = "{title}", body = "", sidebar = "{sidebar}", footer = "{footer}"):
	"""Gets the base html page and fills it with the given information"""
	base = get_base()

	if body == (None or ""):
		body = "<i>This section is empty.</i>"

	base = base.format(title = title, 
					   sidebar = sidebar, 
					   body = body, 
					   footer = footer)

	return base


def fill_info(*, name = "", type = "", args = "", docstring = "", classes = None, functions = None):
	"""Gets the base html page for a class/function and fills it with the given information"""
	info = get_info()

	if name is None or name == "":
		name = "<i>No Name</i>"

	if docstring is None or docstring == "":
		docstring = "<i>No documentation</i>"

	class_str = ""
	if classes is None or classes == "" or len(classes) < 1:
		class_str = "<i>None</i>"
	else:
		for class_item in classes:
			string = "<li class='el_subclass_link'><a href='/html/{parents}{class_name}.html'>{class_name}</a></li>\n"
			class_str += string.format(class_name = class_item["name"], parents = class_item["parents"])

	function_str = ""
	if functions is None or functions == "" or len(functions) < 1:
		function_str = "<i>None</i>"
	else:
		string = "<li class='el_subfunction_link'><a href='/html/{parents}{name}.html'>{name}</a></li>"
		function_str = '\n'.join([string.format(name = func["name"], parents = func["parents"]) for func in functions])

	info = info.format( name = name, type = type, 
						args = args, docstring = docstring, 
						classes = class_str, functions = function_str)

	return info


def generate_index(modulename, docstring):
	"""Creates the index page for the documentation"""
	html = '<h3><i>{title}:</i></h3><hr/>\n<p class="bodytext">{doc}</p>\n'
	return html.format(title = modulename, doc = docstring)


def generate_footer():
	"""Creates the footer for the bottom of the pages"""
	curtime = time.localtime()
	time_string = str(curtime.tm_mon) + "/" + str(curtime.tm_mday) + "/" + str(curtime.tm_year)
	return_string = "<p>Documentation updated on " + time_string + "</p>" 
	return_string += "<p>Written in Python</p>"
	
	return return_string

def generate_nav_link(name, parents):
	sidebar_string = '<li class="sb_el_link"><a href="/html/{parents}{name}.html">{name}</a></li>'.format(name = name, parents = parents)
	return sidebar_string