from extra import AbstractCondition
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
         #DBG
        logger.debug("Value to match : "+ self.__config["value"] + " in ["+str(item.getValue())+"]")
        logger.debug(" match : " + str(self.__p.match(item.getValue())))
        return not self.__p.match(item.getValue()) is None

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
        return self.__regexCondition.evaluate(item)

