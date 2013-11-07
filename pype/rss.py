import feedparser
from core import AbstractProcessor

# Configuration
# Dict with field key, should be 'link' or 'title'

class RssProcessor(AbstractProcessor):
	
	#default field to retrieve from rss items : link
	field = "link"

	def __init__(_self,config):
		# TODO config field value
		_self.field = config["field"]		

	# item should contain a valid RSS url
	def process(_self,item):
		print "processing rss item : " + str(item)
		feedresults = feedparser.parse(str(item))
		result = []
		for entry in feedresults.entries:
			
			if _self.field == "link":
				result.append(entry.link)
			elif _self.field == "title":
				result.append(entry.title)
			else:
				print "Unknown " + str(_self.field) + "field"
		return result

	def processList(_self,items):
		result = []
		for item in items:
			result = result + _self.process(self,item)
		return result
