import feedparser
import logging

logger = logging.getLogger("pype_rss")

from core import *



class RssProcessor(AbstractListProcessor):

	#default field to retrieve from rss items : link
	field = "link"

	def __init__(_self,config):
		""" Configuration
		 	Dict with field key, should be 'link' or 'title'
		 """
		_self.field = config["field"]
		logger.debug("Set field as %s",_self.field)

	def process(_self,item):
		""" Process a RSS item , retrieven the configured field as a string

			- item should contain a valid RSS url
		"""

		logger.info("processing rss item : %s" , str(item.getValue()))
		feedresults = feedparser.parse(str(item.getValue()))

		# TODO set metadata value with item reference
		result = []

		for entry in feedresults.entries:
			resultEntry = BaseItem({"parent":item})
			if _self.field == "link":
				resultEntry.setValue(entry.link)
			elif _self.field == "title":
				resultEntry.setValue(entry.title)
			else:

				""" Unknown field to obtain. Nothing to return """
				logger.warning("Unknown %s field",str(_self.field))
				return None

			if resultEntry is not None:
				# [DBG] print "Entry value " + str(resultEntry.getValue())
				result.append(resultEntry)
		logger.debug("Returning %s elements",str(len(result)))
		return result

