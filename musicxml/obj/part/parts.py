from musicxml.decorators import singleton
from collections.abc import MutableSequence


@singleton
class Parts(MutableSequence):
	def __init__(self, objType):
		#list containing all the Part objects
		#-won't be catch by the local "__setattr__()"
		object.__setattr__(self, "container", [])
		object.__setattr__(self, "ref_obj", objType)


	""" ---------------------------------------
	Sequence Object methods
	This is what gives the ability to use this Object as a List
	"""
	def __getitem__(self, itemIndexOrName):
		if type(itemIndexOrName) is int:
			return list(self.container[itemIndexOrName].values())[0]
		else:
			return self._getItemByName(itemIndexOrName)
		#return self._getCPUByRole(itemName)

	def __iter__(self):
		return iter(self.container)

	def __len__(self):
		return len(self.container)
		#return len(self.CPUs)

	def __delitem__(self, itemName):
		del self[itemName]
	
	def __setitem__(self, itemName, item):
		itemName = itemName.upper()
		if itemName in self.container:
			raise f'The key "{itemName}" is already used, please use unique names'
		else:
			if not isinstance(item, self.ref_obj):
				raise f'The item should be an instance of {self.ref_obj.__class__}'

			self.append(itemName, item)

		pass

	def insert(self, pos, itemName, item):
		if not isinstance(item, self.ref_obj):
			raise f'The item should be an instance of {self.ref_obj.__class__}'

		self.container.insert(pos, {itemName: item})
		
	def append(self, itemName, item):
		self.insert(0, itemName, item)
	#------------------------------------------
	
	#Catch any call of an attribute
	def __getattr__(self, attrName):

		#first check if this attribute exists on this Object
		if attrName in self.__dict__:
			return self.__dict__[attrName]
		#if not, check if this is attribute name is in the container
		else:
			return self._getItemByName(attrName)


	def _getItemByName(self, attrName):
		attrName 	= attrName.upper()
		item 		= None
		for i in self.container:
			if attrName in i:
				item = list(i.values())[0]
				break

		return item