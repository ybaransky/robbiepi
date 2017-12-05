#!/usr/bin/env python

class _const (object):
	'''clever defining constants idiom from Python Cookbook v2'''

	class ConstError(TypeError): 
		pass

	def __setattr__(self, name, value): 
		if name in self.__dict__: 
			raise self.ConstError, "Can't rebind const(%s)" % name
		self.__dict__[name] = value

	def __delattr__(self, name):
		if name in self.__dict__:
			raise self.ConstError, "Can't unbind const(%s)" % name
		raise NameError, name

	def __str__(self) :
		return "const " + str(self.__dict__)

import sys
sys.modules[__name__] = _const()

