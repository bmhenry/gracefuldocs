"""
Documents a module given the module name as an input.
Utilizes the Inspector function to get the documentation for the module,
then produces a static HTML site.
"""

import code
import logging
import os
import re
import shutil
import sys
import webbrowser

import inspector
import ghtml



class Generator:
	"""
	Obtains documentation for a given package or module.

	After __init__, full page information is stored in Generator.pages

	Documentation can be saved with a call to Generator.save('path_to_save').
	The index.html page will be saved directly in the folder path specified.
	"""

	def __init__(self, mainpath):
		# inspect along the given path
		mod_info = inspector.Inspector(mainpath)
		data = mod_info.module_info
		pages = None

		self.log = logging.getLogger("GracefulDocs")

		if data is None:
			log.info("Cancelling documentation... no module info found.")
			exit()

		title = data["name"]

		# create html pages from inspection results
		pages = {
			"index.html": ghtml.generate_index(title, data["docstring"]),
			"style.css": ghtml.get_css(),
			"gracefuldocs_about.html": ghtml.get_gd()
		}

		# generate the sidebar navigation menu
		self.sidebar = "<p><a href='index.html'><b>{title}</b></a></p>\n"
		self.sidebar = self.sidebar.format(title = title)

		# create the page footer
		self.footer = ghtml.generate_footer(title)

		self.mod_info = mod_info
		self.data = data
		self.title = title
		self.pages = pages

		# create other pages for the classes/functions
		self._create_pages()

		# other function calls here
		self._fill_pages()

		pass


	def _create_pages(self):
		"""Adds a page to Generator.pages for every class and function"""

		self.sidebar_modules = []  # add extra sidebar links to this

		# create a page for each class -- recursive for subclasses/subfunctions
		if len(self.data['classes']) > 0:
			# start a subelement list
			self.sidebar_modules.append('<span>Classes:</span>')
			self.sidebar_modules.append('<ul>')

			for class_item in self.data['classes']:
				self._doc_class(class_item)

			self.sidebar_modules.append('</ul>')


		# create a page for each function
		if len(self.data['functions']) > 0:
			self.sidebar_modules.append('<span>Functions:</span>')
			self.sidebar_modules.append('<ul>')
			
			for function_item in self.data['functions']:
				self._doc_function(function_item)

			self.sidebar_modules.append('</ul>')


		# end
		if len(self.sidebar_modules) > 0:
			self.sidebar += "<p>Modules:</p>\n"
			for item in self.sidebar_modules:
				self.sidebar +=  item + "\n"

		pass


	def _fill_pages(self):
		"""Plugs existing page information into the base page with styles, etc."""
		if self.pages is None:
			self.log.info("Couldn't get any information about the module.")
			return

		for page in self.pages:
			if page == "style.css":
				continue

			# take the page body information and fill a base html page with it
			self.pages[page] = ghtml.fill_base(title = self.title, 
												body = self.pages[page],
												sidebar = self.sidebar,
												footer = self.footer)

		pass


	def _doc_class(self, class_item):
		"""
		Gets a class item as created by the Inspector and creates the body for
		and html page. 

		This page is automatically added to Generator.pages, and a sidebar link
		is automatically added to the sidebar.
		"""
		sidebar_link = None

		# lists for subelements
		subclasses = []
		subfunctions = []

		if class_item['name'] == None or "":
			return

		# create the sidebar link for this class
		sidebar_link = ghtml.generate_nav_link(class_item["name"])
		self.sidebar_modules.append(sidebar_link)

		# create the page body
		page = ghtml.fill_info(name = class_item["name"], type = "class")
		self.pages["elements/" + class_item["name"]] = page

		for subclass in class_item['classes']:
			#TODO
			pass

		for subfunction in class_item['functions']:
			#TODO
			pass

		pass


	def _doc_functions(self, function_item):
		#TODO
		pass


	def save(self, savepath):
		"""Saves documentation to the given file path."""

		if self.pages is None:
			self.log.info("Couldn't get any information about the module.")

		for page in self.pages:
			with open(savepath + '/' + page, 'w') as doc:
				doc.write(self.pages[page])

		pass



def main():
	log = logging.getLogger("GracefulDocs")

	# get the output folder for the documentation
	if len(sys.argv) > 2:
		outdir = sys.argv[2]
	else:
		outdir = input("Enter a folder for the HTML documentation to be written to (just '.' for current directory); enter '*quit' or '*q' to cancel:  ")
	
	# get the name of the module/file to be documented
	if len(sys.argv) > 1:
		modulename = sys.argv[1]
	else:
		modulename = input("Please enter module name to document:  ")

	# check if user asked for help
	if re.match("(-+)h | (-+)help | (\?+)", modulename.lower()):
		print("Module name must be in your system path or current working directory")

	if outdir.lower() == ['*quit']:
		exit()

	# get the full path from the relative path the user entered
	outdir = os.path.abspath(outdir)
	log.debug(outdir)

	# create the output folder for documentation if it doesn't already exist
	if not os.path.isdir(outdir):
		uin = input("This directory does not yet exist. Would you like to create it? (Y/N) ")

		if uin.lower() in "yes":
			ghtml.forcedir(os.path.abspath(outdir))
		else:
			log.info("Cancelling doc creation...")
			exit()


	# generate the docs and save
	html = Generator(modulename)
	html.save(outdir)

	log.info("Documenation written to " + outdir + " .")
	u_open = input("Open in browser now? (Y/N) ")

	if u_open.lower() in ['y', 'yes']:
		webbrowser.open(url = os.path.abspath(outdir + '/index.html'), new = 2)

	pass


if __name__ == '__main__':
	main()