from extra import *
import re
import logging

logger = logging.getLogger("pype.extra.conditions")

# Define some basic conditions



""" Regex evaluation on text value"""
class RegexCondition(AbstractCondition):

    __p = None
    __config = {}

    def __init__(self,config):

        if self.__validateConfig(config):
            self.__config["value"] = config["value"]
            self.__p = re.compile(self.__config["value"])

    def evaluate(self,item):
        if item.getValue() is None:
            return False
         #DBG
        logger.debug("Value to match : "+ self.__config["value"] + " in ["+str(item.getValue())+"]")
        result = self.__p.match(str(item.getValue()))
        logger.debug(" match : " + str(result))
        return not  result is None

    def __validateConfig(self,config):
        if config is None:
            raise "This Condition needs configuration"
        elif not "value" in config:
            raise "This Condition needs 'value' in the configuration"
        else:
            return True

""" Contains text condition """
class ContainsTextCondition(AbstractCondition):

    # Using RegexCondition
    __regexCondition = None

    __config = {}

    def __init__(self,config):
        self.__config["value"] = ".*" + config["value"] + ".*"

        self.__regexCondition = RegexCondition(self.__config)


    def evaluate(self,item):
        if item.getValue() is None:
            return False
        return self.__regexCondition.evaluate(item)


ALREADY_PROCESSED_DATASOURCE = "alreadyprocesseddatasource"

""" Condition checks if the item has been already processed
    Must provide a dataSource component
"""
class AlreadyProcessedCondition(AbstractCondition):

    __config = {}
    __datasource = None

    def __init__(self,config):

        self.__config = config
        if ALREADY_PROCESSED_DATASOURCE in config:
            logger.info("Setting datasource "+str(config[ALREADY_PROCESSED_DATASOURCE]))
            self.__datasource = config[ALREADY_PROCESSED_DATASOURCE]

    def evaluate(self,item):
        if self.__config[ALREADY_PROCESSED_DATASOURCE] is None:
            logger.warn("No "+ALREADY_PROCESSED_DATASOURCE+ " provided!! Returning False")
            return False
        else:
            return self.__datasource.exists(item)
