"""
Documents a module given the module name as an input.
Utilizes the Inspector function to get the documentation for the module,
then produces a static HTML site.
"""

import code
import os
import re
import sys
import webbrowser

import inspector
import ghtml



def force_dir()
def forcedir(dir_path):
    """Makes sure that a directory exists"""

    subdirs = dir_path.strip().split('\\')
    for path in range(len(subdirs)):
        new_path = '\\'.join(subdirs)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
    pass


class Documentor:
	"""Obtains documentation for a given package or module."""

	def __init__(self, fullpath):
		pass

	