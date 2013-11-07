
# Example : http://bandaancha.eu/
from pype.html import *

htmlprocessor = HtmlProcessor({"field":"link"})

base = BaseItem(None)
base.setValue("http://bandaancha.eu/")
result = htmlprocessor.process(base)

for e in result:
    print str(e.getValue()) +" <<<<< " +  str(e.getMetadataValue("parent").getValue())