"""Inspects a module and returns this information for documentation"""

import inspect  # uses isfunction, isclass, signature
import importlib  # uses import_module
import re
import sys
import os

import code
import json



class Inspector:
	"""
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
				"docstring": "",
				"classes": [],
				"functions": []	  
			},
			etc. for other classes
		],
		"functions": 
		[
			{
				"name": "",
				"docstring": "",
				"parameters": []
			},
			etc. for other functions
		]
	}
	"""

	def __init__(self, mainpath):
		self.mainpath = os.path.abspath(mainpath)
		self.module_info = None
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

			self.module_info = self.inspect_file(mainpath)
			pass

		else:
			print("Couldn't find a Python package or module at the given path.")
			self.module_info = None


	def inspect_dir(self, fullpath):
		# TODO
		pass


	def inspect_file(self, fullpath):
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
			"classes": [],
			"functions": []
		}

		# get basic module information
		docs["name"] = module.__name__
		docs["docstring"] = module.__doc__.strip() if module.__doc__ != None else ""

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
			"args": "",
			"classes": [],
			"functions": []
		}

		docs["name"] = obj.__name__

		# try to get a docstring from either the class description or the 
		#  __init__ description
		docs["docstring"] = obj.__doc__.strip() if obj.__doc__ != None else ""

		members = dir(obj)
		for member in members:
			# don't get __init__, __repr__, etc.
			if self.regex.match(member) and not member == "__init__":
				continue

			member_object = getattr(obj, member)
			
			if inspect.isclass(member_object):
				docs['classes'].append(self.inspect_class(member_object))
			elif inspect.isfunction(member_object):
				obj_docs = self.inspect_function(member_object)
				if obj_docs['name'] == '__init__':
					docs["args"] = obj_docs["args"]
				docs['functions'].append(self.inspect_function(member_object))

		return docs


	def inspect_function(self, obj):
		"""Inspects a function for docs, subclasses, and subfunctions"""
		
		docs = {
			"name": "",
			"docstring": "",
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
	x = input("Enter a file name:")
	i = Inspector(x)
	
	if i.module_info != None:
		with open('test_log.txt','w') as f:
			f.write(json.dumps(i.module_info, indent = 2))
			print("Wrote to test_log.txt")
			

if __name__ == '__main__':
	main()