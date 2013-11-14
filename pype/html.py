from bs4 import BeautifulSoup
import requests
import logging

import sys

from core import *

logger = logging.getLogger("pype_html")

class HtmlProcessor(AbstractListProcessor):

    config = None

    def __init__(self,config):
        self.config = config



    def process(self,item):
        """ Process a HTML item , retrieving whatever config stands

            - item should contain a valid web url
        """
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
            return None
        else:

            foundItems = self.internalProcess(item.getValue(),item)
            if foundItems is not None:
                result.extend(foundItems)
            else:
                resultItem = BaseItem({"parent":item})
                resultItem.setValue(htmlBS)
                result.append(resultItem)

        return result

    """ Process inside the bsObject  (BS one) """
    def internalProcess(self,bsObject,item):

        result = []

        if "find" in self.config and self.config["find"] is not None:
            findConfigDict = self.config["find"]
            # Process all find config definitions
            for findKey in findConfigDict:

                if findConfigDict[findKey] is not None:
                     foundElements = bsObject.find_all(findKey, findConfigDict[findKey])
                else:
                    foundElements = bsObject.find(findKey)

                for foundElement in foundElements:
                    foundItem = BaseItem({"parent":item})
                    foundItem.setValue(foundElement)
                    result.append(foundItem)

        elif "get" in self.config and self.config["get"] is not None:

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