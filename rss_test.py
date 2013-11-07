
# Example : http://www.medscape.com/cx/rssfeeds/2667.xml
from pype.rss import *

rssprocessor = RssProcessor({"field":"link"})

base = BaseItem(None)
base.setValue("http://www.medscape.com/cx/rssfeeds/2667.xml")
result = rssprocessor.process(base)

for e in result:
    print str(e.getValue()) + str(e.getMetadataValue("parent"))