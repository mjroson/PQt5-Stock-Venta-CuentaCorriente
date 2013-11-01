#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Marca(object):
	"""docstring for Marca"""
	def __init__(self):
		super(Marca, self).__init__()
		self.__idMarca = 0
		self.__marca = ""

	def setIdMarca(self, idMarca):
		self.__idMarca = idMarca
	
	def getIdMarca(self):
		return self.__idMarca
	
	def setMarca(self, marca):
		self.__marca = marca
		
	def getMarca(self):
		return self.__marca

	
