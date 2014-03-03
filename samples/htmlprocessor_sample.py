from pype.core import BaseItem
from pype.html import HtmlProcessor

#logging
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

item = BaseItem(None,"https://github.com")

htmlprocessor = HtmlProcessor({})

result = htmlprocessor.process(item)

print str(result[0])