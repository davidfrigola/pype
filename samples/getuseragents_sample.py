from pype.extra import ChainProcessor, PROCESSORS_LIST
from pype.model import BaseItem
from pype.file import FileProcessor, FILE_NAME, FILE_OP, FILE_OP_STORE
from pype.html import HtmlProcessor,BSProcessor


# Url with all user agents (HTML format)
url="http://www.useragentstring.com/pages/All/"

# Steps of pype chain processor
# 1. Get HTML from URL and filter by li elements
# 2. Get div with id=liste in the resulting html
# 3. Get all <a elements within the li elements
# 4. Get all a values (text) from step 3
# 5. Store in a file
# This file is used in the RandomUserAgentHeadersProvider

#logging
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)




item = BaseItem(None,url)


chain = ChainProcessor({PROCESSORS_LIST:[HtmlProcessor(None),
                                          BSProcessor({"find":{"div":{"id":"liste"}}}),
                                          BSProcessor({"find":{"li":None}}),
                                          BSProcessor({"find":{"a":None}}),
                                          BSProcessor({"text":None}),
                                          FileProcessor({FILE_NAME:"./useragents.txt",FILE_OP:FILE_OP_STORE})]})
#, BSProcessor({"get":{"string"}})]}

result = chain.processList([item])




