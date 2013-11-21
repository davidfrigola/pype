import logging

from model import *

logger = logging.getLogger("pype.core")

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

	def processList(self,items):
		result = []
		for item in items:
			processedItem = self.process(item)
			if processedItem is not None:
				result = result + processedItem
			else:
				logger.warning("Processed item %s returns None",str(item))

		return result


