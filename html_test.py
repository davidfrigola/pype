
# Example : http://bandaancha.eu/
from pype.html import *

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

htmlprocessor = HtmlProcessor({"find":{"h2":{"class":"title"}}})
h2processor = BSProcessor({"find":{"a":{"itemprop":"url"}}})

base = BaseItem(None)
base.setValue("http://bandaancha.eu/")
result = htmlprocessor.process(base)

for e in result:
    if e is None:
        print "NONE"
    else:
        print str(e.getValue()) +" <<<<< " +  str(e.getMetadataValue("parent"))
        aResult = h2processor.process(e)
        for a in aResult:
            print "Found link ----- " + str(a.getValue())
            print str(a.getValue().get("href"))
