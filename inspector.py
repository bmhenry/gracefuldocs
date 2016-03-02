"""
Contains the Inspector class:

	Inspects a file or directory given the directory, then returns a dictionary
	containing the package or module's information.

	If the path is to a directory, Inspector will determine whether it's a
	Python package or whether it just contains Python files.


	Information is stored in Inspector.module_info as follows:

	self.module_info = 
	{
		"name": "",
		"docstring": "",
		"classes": 
		[
			{
				"name": "",
				"parents": "",  # for example, like "packagename/modulename/"
				"docstring": "",
				"args": "",
				"classes": [],
				"functions": []	  
			},
			etc. for other classes
		],
		"functions": 
		[
			{
				"name": "",
				"parents": "",  # for example, like "packagename/modulename/classname"
				"docstring": "",
				"args": "",
				"parameters": []
			},
			etc. for other functions
		]
	}

	README and LICENSE files will usually be found and included. If these are written in
	plaintext or HTML, they will be included as such. If they are writen in Markdown, their
	contents will be converted to HTML for display.

	Inspector will not move/destroy/modify in any way your existing files of any type.
"""


import ast
import inspect  # uses isfunction, isclass, signature
import importlib  # uses import_module
import re
import sys
import os

import code
import json



# TODO: include readme and license files, convert markdown to html
# TODO: redo this to use the ast module instead of importing

class Inspector:
	"""Inspects a file or directory given the directory, then returns a dictionary
	containing the package or module's information.

	If the path is to a directory, Inspector will determine whether it's a
	Python package or whether it just contains Python files.


	Information is stored in Inspector.module_info as follows:

	self.module_info = 
	{
		"name": "",
		"docstring": "",
		"classes": 
		[
			{
				"name": "",
				"parents": "",  # for example, like "packagename/modulename/"
				"docstring": "",
				"args": "",
				"classes": [],
				"functions": []	  
			},
			etc. for other classes
		],
		"functions": 
		[
			{
				"name": "",
				"parents": "",  # for example, like "packagename/modulename/classname"
				"docstring": "",
				"args": "",
				"parameters": []
			},
			etc. for other functions
		]
	}

	README and LICENSE files will usually be found and included. If these are written in
	plaintext or HTML, they will be included as such. If they are writen in Markdown, their
	contents will be converted to HTML for display.

	Inspector will not move/destroy/modify in any way your existing files of any type.
	"""

	def __init__(self, mainpath):
		self.mainpath = os.path.abspath(mainpath)
		self.module_info = None
		self.package_docs = None

		# make sure that the file/folder exists
		if not os.path.exists(mainpath):
			print("Couldn't find the specified path.",
					"Make sure it's in your current directory or that you gave the full path.")
			self.module_info = None
			return

		# regex to find anything like '__init__' or '__repr__', etc.
		self.regex = re.compile('__(\S+)__')
		self.py_regex = re.compile('((\S+).py)', flags = re.IGNORECASE)
		self.info_regex = re.compile('(readme)|(license)', flags = re.IGNORECASE)

		# directory (package) or module?
		if os.path.isdir(mainpath):
			# directory
			# determine the title of the package from the name of this directory
			realpath = os.path.abspath(mainpath)
			self.title = os.path.split(realpath)[1]
			
			dir_info = self.inspect_dir(realpath)

			if dir_info is not None:
				self.module_info = dir_info

			pass

		elif os.path.isfile(mainpath):
			# file
			# get directory and determine the title of the site
			self.directory, filename = os.path.split(mainpath)
			self.title = os.path.splitext(filename)[0]

			self.module_info = self.inspect_file(mainpath)
			pass

		else:
			print("Couldn't find a Python package or module at the given path.")
			self.module_info = None


	def inspect_dir(self, fullpath, parents = ""):
		"""Inspects a directory or Python package for directories, for Python code files ending in '.py'
		(including '__init__.py' and '__main__.py' files), as well as README and LICENSE files."""
		
		docs = {
			"name": "",
			"docstring": "",
			"parents": "",
			"directories": [],
			"modules": []
		}


		# get a list of all the files inside the directory
		subpaths = os.listdir(fullpath)
		print(subpaths)

		docs["name"] = os.path.split(fullpath)[1]
		docs["parents"] = parents
		parent_str = parents + "/" + docs["name"]

		# find all Python files of form '.py' as well as any README and LICENSE files
		for subpath in subpaths:
			realpath = fullpath + '/' + subpath

			if os.path.isdir(realpath):
				# subpath is a directory
				subdocs = self.inspect_dir(realpath, parent_str)
				if subdocs is not None:
					docs["directories"].append(subdocs)

			elif self.py_regex.match(subpath):
				# subpath is a .py file
				subdocs = self.inspect_file(realpath, parent_str)
				if "__init__.py" == subpath:
					docs["docstring"] = subdocs["docstring"]

				docs["modules"].append(subdocs)

			elif self.info_regex.match(subpath):
				# subpath is a README or LICENSE file
				# TODO
				pass

			else:
				subpaths.remove(subpath)

		return docs if len(subpaths) > 0 else None


	def inspect_file(self, fullpath, parents = ""):
		"""Inspects a Python file for docs, classes, and functions."""
		# get the name of the file
		directory, filename = os.path.split(fullpath)
		name, _ = os.path.splitext(filename)

		# Try to import the file to gather information
		module = importlib.machinery.SourceFileLoader(name, fullpath).load_module()
		#code.interact(local = locals())

		if not module:
			return

		docs = {
			"name": "",
			"docstring": "",
			"parents": "",
			"classes": [],
			"functions": []
		}

		# get basic module information
		docs["name"] = module.__name__
		docs["docstring"] = module.__doc__.strip() if module.__doc__ != None else ""
		docs["parents"] = parents + '/' + module.__name__

		# create the parent name string to pass to children
		parent_str = module.__name__ + "/"

		members = dir(module)
		for member in members:
			# don't get __init__, __repr__, etc.
			if self.regex.match(member):
				continue

			member_object = getattr(module, member)
			if inspect.isclass(member_object):
				docs["classes"].append(self.inspect_class(member_object, parent_str))
			elif inspect.isfunction(member_object):
				docs["functions"].append(self.inspect_function(member_object, parent_str))

		return docs


	def inspect_class(self, obj, parents):
		"""Inspects a class for docs, subclasses, and subfunctions"""
		
		docs = {
			"name": "",
			"docstring": "",
			"parents": parents,
			"args": "",
			"classes": [],
			"functions": []
		}

		docs["name"] = obj.__name__

		# try to get a docstring from either the class description or the 
		#  __init__ description
		docs["docstring"] = obj.__doc__.strip() if obj.__doc__ != None else ""

		# create parent string to pass to children
		parent_str = parents + obj.__name__ + "/"

		members = dir(obj)
		for member in members:
			# don't get __init__, __repr__, etc.
			if self.regex.match(member) and not member == "__init__":
				continue

			member_object = getattr(obj, member)
			
			if inspect.isclass(member_object):
				docs["classes"].append(self.inspect_class(member_object, parent_str))
			elif inspect.isfunction(member_object):
				obj_docs = self.inspect_function(member_object, parent_str)
				if obj_docs['name'] == '__init__':
					docs["args"] = obj_docs["args"]
				docs['functions'].append(obj_docs)

		return docs


	def inspect_function(self, obj, parents):
		"""Inspects a function for docs, subclasses, and subfunctions"""
		
		docs = {
			"name": "",
			"docstring": "",
			"parents": parents,
			"args": []
		}

		docs["name"] = obj.__name__
		docs["docstring"] = obj.__doc__.strip() if obj.__doc__ != None else ""

		# get function parameters
		args = inspect.signature(obj).parameters

		#this will separate keyword only args from positional ones
		arg_list = []
		kw_only = []

		for arg in args:
			param = args[arg]

			if param.default != inspect.Parameter.empty:
				string = param.name + " = " + repr(param.default)
			else:
				string = param.name

			if param.kind == inspect.Parameter.KEYWORD_ONLY:
				kw_only.append(string)
			else:
				arg_list.append(string)

		if len(kw_only) > 0:
			arg_list += ['*'] + kw_only

		docs["args"] = ', '.join(arg_list)

		return docs


def main():
	"""Used if this file is ran directly from the command line. Asks for
	a filename/path and attempts to run the Inspector class on the file/path.
	The results will be saved in a 'test_log.txt' file in your current directory."""
	x = input("Enter a file name:")
	i = Inspector(x)
	
	if i.module_info != None:
		with open('test_log.txt','w') as f:
			f.write(json.dumps(i.module_info, indent = 2))
			print("Wrote to test_log.txt")
	else:
		print("No Python files found in directory")

if __name__ == '__main__':
	main()