"""
This is some documentation.
"""

class TestClass:

	def __init__(self, parent = 7, test = "something", *, somethingelse = "nada"):
		"""Docstring in the wrong place. Can we find it?"""
		print(parent)

	def subfunction_in_class(self, s1, s2, s3 = "something"):
		"""This is just a test function."""
		print(s1, s2, s3)


def test_function(x, y = 10):
	"""A function"""
	print(x * y * 2)

	class ClassX_in_function:
		"""This is a subclass"""
		def __init__(self, parent):
			return

	def subfunction_in_function(z, theta = 20):
		"""A sub function"""
		print(z * theta * 3.14)