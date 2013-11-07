
class AbstractProcessor:
	""" Abstract Processor Base Class
		- Defines the base API for a processor
		- Does not implement anything (that's abstract)

	"""


	def __init__(self,config):
		""" The config object should contain all the configuration needed

		"""
		pass


	def process(self,item):
		""" Process an item """
		pass


	def processList(self,items):
		""" Process a list of items """
		pass

class AbstractListProcessor(AbstractProcessor):
	""" Implements list processing
		Uses the process method for each element in the list.
	"""

	def processList(_self,items):
		result = []
		for item in items:
			result = result + _self.process(self,item)
		return result


class AbstractItem:
	""" Abstract item to process """
	metadata = {}
	value = None
	def __init__(self,metadata):
		pass


	def getMetadataValue(self,key):
		pass



class BaseItem(AbstractItem):
	""" Base item """
	def __init__(self,metadata):
		self.metadata = metadata

	def setValue(self,value):
		self.value = value

	def getValue(self):
		return self.value

	def getMetadataValue(self,key):
		return self.metadata[key];
