from bs4 import BeautifulSoup
import requests
import logging

from core import *

logger = logging.getLogger("pype_html")

class HtmlProcessor(AbstractListProcessor):

    config = None
    def __init__(self,config):
        self.config = config



    def process(_self,item):
        """ Process a HTML item , retrieving whatever config stands

            - item should contain a valid web url
        """
        #TODO
        pass