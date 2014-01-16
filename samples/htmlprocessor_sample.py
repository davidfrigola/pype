from pype.core import *
from pype.html import *

#logging
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

item = BaseItem(None,"https://github.com")

htmlprocessor = HtmlProcessor({HTML_REQUEST_AGENT_HEADER:"Some user-agent"})

result = htmlprocessor.process(item)

print str(result[0])