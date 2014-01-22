from bs4 import BeautifulSoup
import requests
import logging
import traceback

import sys

from core import *

logger = logging.getLogger("pype.html")


""" Config constants for HtmlProcessor """
FROM_TEXT = "fromtext"
HEADERS_PROVIDER = "headers_provider"
class HtmlProcessor(AbstractListProcessor):

    __config = {}

    def __init__(self,config):
        if config is not None:
            self.__config = config
        ## TODO Validate config




    def process(self,item):
        """ Process a HTML item , retrieving whatever is in config
            - item should contain a valid web url
        """
        try:
            if FROM_TEXT  in self.__config and self.__config[FROM_TEXT]:
                logger.debug("Using text to obtain BS object")
                htmlBS = BeautifulSoup(item.getValue())
            else:
                logger.debug("Request to "+ str(item.getValue()))
                try:
                    headers = self.__getHeaders()
                    if headers is not None:
                        htmlBS = BeautifulSoup(requests.get(item.getValue(),headers=headers).text)
                    else:
                        htmlBS = BeautifulSoup(requests.get(item.getValue()).text)
                except:
                    logger.error("Some errors requesting item value.Returning [] ")
                    traceback.print_exc()
                    return []
            bsHtmlItem = BaseItem({"parent":item})
            bsHtmlItem.setValue(htmlBS)

            bsProcessor = BSProcessor(self.__config)

            return bsProcessor.process(bsHtmlItem)

        except:
            logger.error("Errors during html processing : ignoring")
            traceback.print_exc()
            return []

    def __getHeaders(self):
        if HEADERS_PROVIDER in self.__config and self.__config[HEADERS_PROVIDER] is not None:
            return self.__config[HEADERS_PROVIDER].getHeaders()
        else:
            return None
""" BS Object processor
    using BeautifullSoup features to parse HTML and find elements
    Implemented FIND filter (set "find" in the metadata and a valid BS find expression)
"""
class BSProcessor(HtmlProcessor):

    __config = None

    def __init__(self,config):
        self.__config = config

    """ Item should be a BaseItem with a BSObject set as value """
    def process(self,item):

        result = []

        if item is None:
            logger.info("None item : returning None")
            return None
        else:

            foundItems = self.internalProcess(item.getValue(),item)
            if foundItems is not None:
                logger.info("Found "+ str(len(foundItems))+" item(s)")
                result.extend(foundItems)
            else:
                logger.warn("No items found")
                resultItem = BaseItem({"parent":item})
                resultItem.setValue(item)
                result.append(resultItem)

        return result

    """ Process inside the bsObject  (BS one) """
    def internalProcess(self,bsObject,item):

        result = []

        if "find" in self.__config and self.__config["find"] is not None:
            logger.debug("Processing 'find' config " + str(self.__config["find"]))
            findConfigDict = self.__config["find"]
            # Process all find config definitions
            for findKey in findConfigDict:

                if findConfigDict[findKey] is not None:
                     foundElements = bsObject.find_all(findKey, findConfigDict[findKey])
                else:
                    foundElements = bsObject.findAll(findKey)

                for foundElement in foundElements:
                    foundItem = BaseItem({"parent":item})
                    foundItem.setValue(foundElement)
                    result.append(foundItem)

        elif "get" in self.__config and self.__config["get"] is not None:

            logger.debug("Processing 'get' config '" + str(self.__config["get"]) + "'")
            getConfigDict = self.__config["get"]
            for getKey in getConfigDict:
                logger.debug("Processing GET '"+getKey+"'")
                if getKey is not None:

                    getItem = BaseItem({"parent":item})
                    getItem.setValue(bsObject.get(getKey))
                    result.append(getItem)

                else:
                    raise "Error : should provide something to GET"
        elif "text" in self.__config:
            result.append(BaseItem({"parent":item},bsObject.text))
        else:
            logger.warning("Nothing to process internally. Returning same item")
            result = [item]

        return result



class AbstractHeaderProvider:
    """ Abstract header provider
    """


    config = {}

    def __init__(self,config):
        if config is not None:
            self.config = config
        else:
            logger.warn("None config for header provider")

    def getHeaders(self):
        """ To be implemented by subclasses
            Must return headers as a DICT

            headers = { "header1":"valueheader1",...}

        """
        pass


USER_AGENT_HEADER = "user_agent_header"

class DefaultUserAgentHeaderProvider(AbstractHeaderProvider):
    """ To be used by HtmlProcessor as default header provider with agent """
    """ Config can contain a USER_AGENT_HEADER key with the user agent value for the User-Agent header"""

    def __init__(self,config):
        super(DefaultUserAgentHeaderProvider,self).__init__(config)

    def getHeaders(self):
        if USER_AGENT_HEADER in self.config and self.config[USER_AGENT_HEADER] is not None:
            return {"User-Agent" : self.config[USER_AGENT_HEADER]}
        else:
            return {'User-Agent': 'Mozilla/5.0'}



class RandomUserAgentHeadersProvider(AbstractHeaderProvider):

    def __init__(self,config):
        super(RandomUserAgentHeadersProvider,self).__init__(config)

    def getHeaders(self):
        # TODO Implement random user agent
        #1. Obtain from "useragents.txt" file
        #2. Obtain one from there

        pass


