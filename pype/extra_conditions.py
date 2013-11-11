from extra import AbstractCondition
import re



# Define some basic conditions



""" Regex evaluation on text value"""
class RegexCondition(AbstractCondition):

    __p = None
    __config = {}

    def __init__(self,config):
        self.__config["value"] = config["value"]
        self.__p = re.compile(self.__config["value"])

    def evaluate(self,item):
         #DBG
        # print "Value to match : "+ self.__config["value"] + " in ["+str(item.getValue())+"]"
        # print "DBG : match : " + str(self.__p.match(item.getValue()))
        return not self.__p.match(item.getValue()) is None


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

