import feedparser
import logging

logger = logging.getLogger("pype.rss")

from core import *



class RssProcessor(AbstractListProcessor):

	#default field to retrieve from rss items : link
	field = "link"

	def __init__(self,config):
		""" Configuration
		 	Dict with field key, should be 'link' or 'title'
		 """
		self.field = config["field"]
		logger.debug("Set field as %s",self.field)

	def process(self,item):
		""" Process a RSS item , retrieving the configured field as a string

			- item should contain a valid RSS url
		"""

		logger.info("processing rss item : %s" , str(item.getValue()))
		feedresults = feedparser.parse(str(item.getValue()))

		# TODO set metadata value with item reference
		result = []

		for entry in feedresults.entries:
			resultEntry = BaseItem({"parent":item})
			if self.field == "link":
				resultEntry.setValue(entry.link)
			elif self.field == "title":
				resultEntry.setValue(entry.title)
			elif self.field == "content":
				resultEntry.setValue(entry.content)
			else:

				""" Unknown field to obtain. Nothing to return """
				logger.warning("Unknown %s field",str(self.field))
				return None

			if resultEntry is not None:
				#Add always title as metadata
				resultEntry.setMetadataValue("title",entry.title)
				logger.debug("Entry value for '" + self.field + "'= " + str(resultEntry.getValue()))
				result.append(resultEntry)
		logger.debug("Returning %s elements",str(len(result)))
		return result

