from bs4 import BeautifulSoup
import requests
import logging

import sys

from core import *

logger = logging.getLogger("pype.html")


""" Config constants for HtmlProcessor """
FROM_TEXT = "fromtext"

class HtmlProcessor(AbstractListProcessor):

    config = None

    def __init__(self,config):
        self.config = config





    def process(self,item):
        """ Process a HTML item , retrieving whatever is in config
            - item should contain a valid web url
        """
        if FROM_TEXT  in self.config and self.config[FROM_TEXT]:
            logger.debug("Using text to obtain BS object")
            htmlBS = BeautifulSoup(item.getValue())
        else:
            logger.debug("Request to "+item.getValue())
            htmlBS = BeautifulSoup(requests.get(item.getValue()).text)
        bsHtmlItem = BaseItem({"parent":item})
        bsHtmlItem.setValue(htmlBS)

        bsProcessor = BSProcessor(self.config)

        return bsProcessor.process(bsHtmlItem)





""" BS Object processor
    using BeautifullSoup features to parse HTML and find elements
    Implemented FIND filter (set "find" in the metadata and a valid BS find expression)
"""
class BSProcessor(HtmlProcessor):

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

        if "find" in self.config and self.config["find"] is not None:
            logger.debug("Processing 'find' config " + str(self.config["find"]))
            findConfigDict = self.config["find"]
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

        elif "get" in self.config and self.config["get"] is not None:

            logger.debug("Processing 'get' config " + str(self.config["get"]))
            getConfigDict = self.config["get"]
            for getKey in getConfigDict:

                if getKey is not None:

                    getItem = BaseItem({"parent":item})
                    getItem.setValue(bsObject.get(getKey))
                    result.append(getItem)

                else:
                    raise "Error : should provide something to GET"

        else:
            result = None

        return result