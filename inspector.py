"""Inspects a module and returns this information for documentation"""

import re
import sys
import os

import inspect  # uses isfunction, isclass, signature
import importlib  # uses import_module



class Inspector:
	"""
	Inspects a file or directory given the directory, then returns a dictionary
	containing the package or module's information.

	If the path is to a directory, Inspector will determine whether it's a
	Python package or whether it just contains Python files.
	"""

	def __init__(self, mainpath):
		self.mainpath = os.path.abspath(mainpath)
		self.module_info = []
		self.package_docs = None

		# make sure that the file/folder exists
		if not os.path.exists(mainpath):
			print("Couldn't find the specified path.",
					"Make sure it's in your current directory or that you gave"
					+ " the full path.")
			self.module_info = None
			return

		# regex to find anything like '__init__' or '__repr__', etc.
		self.regex = re.compile('__(\S+)__')

		# directory (package) or module?
		if os.path.isdir(mainpath):
			# directory
			# TODO
			pass

		elif os.path.isfile(mainpath):
			# file

			# get directory and determine the title of the site
			self.directory, filename = os.path.split(mainpath)
			self.title = os.path.splitext(filename)[0]

			self.inspect_file(mainpath)
			pass

		else:
			print("Couldn't find a Python package or module at the given path.")
			self.module_info = None


	def inspect_dir(self, fullpath):
		# TODO
		pass


	def inspect_file(self, fullpath):
		"""Inspects a Python file for docs, classes, and functions."""
		# Try to import the file to gather information
		module = importlib.machinery.SourceFileLoader(fullpath)

		if not module:
			return

		docs = {
			"name": "",
			"docstring": "",
			"classes": [],
			"functions": []
		}

		# get basic module information
		docs["name"] = module.__name__
		docs["docstring"] = module.__doc__

		members = dir(module)
		for member in members:
			# don't get __init__, __repr__, etc.
			if self.regex.match(member):
				continue

			member_object = getattr(module, member)
			if inspect.isclass(member_object):
				docs['classes'].append(self.inspect_class(member_object))
			elif inspect.isfunction(member_object):
				docs['functions'].append(self.inspect_function(member_object))

		return docs


	def inspect_class(self, obj):
		"""Inspects a class for docs, subclasses, and subfunctions"""
		
		docs = {
			"name": "",
			"docstring": "",
			"classes": [],
			"functions": []
		}

		docs["name"] = obj.__name__
		docs["docstring"] obj.__doc__

		members = dir(obj)
		for member in members:
			# don't get __init__, __repr__, etc.
			if self.regex.match(member):
				continue

			member_object = getattr(module, member)
			if inspect.isclass(member_object):
				docs['classes'].append(self.inspect_class(member_object))
			elif inspect.isfunction(member_object):
				docs['functions'].append(self.inspect_function(member_object))

		return docs


	def inspect_function(self, obj):
		"""Inspects a function for docs, subclasses, and subfunctions"""
		pass


