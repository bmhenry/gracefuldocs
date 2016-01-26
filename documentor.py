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
	Documentation can be saved with a call to Generator.save('path_to_save')
	"""

	def __init__(self, mainpath):
		# inspect along the given path
		mod_info = inspector.Inspector(mainpath)
		data = mod_info.module_info
		pages = None

		self.log = logging.getLogger("GracefulDocs")

		if data is None:
			log.info("Cancelling documentation creation... no module info found.")
			exit()

		# create html pages from inspection results
		pages = {
			"index.html": ghtml.generate_index(data["name"], data["docstring"]),
			"style.css": ghtml.get_css(),
			"gracefuldocs_about.html": ghtml.get_gd()
		}

		self.mod_info = mod_info
		self.data = data
		self.pages = pages

		# other function calls here
		self._fill_pages()

		pass


	def _fill_pages(self):
		"""Plugs existing page information into the base page with styles, etc."""
		if self.pages is None:
			self.log.info("Couldn't get any information about the module.")

		pass


	def save(self, savepath):
		"""Saves documentation to the given file path"""

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