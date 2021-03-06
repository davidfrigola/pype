from core import AbstractListProcessor,AbstractProcessor
from datasource import *
import random
from time import sleep
import logging

logger = logging.getLogger("pype.extra")

# Some global constants
# The processor chain config key
PROCESSORS_LIST = "processorslist"
# The modifiers list config key
MODIFIERS_LIST = "modifierslist"



""" MetaProcessor
    Provides a chain of processing, set the chain [in order]
    in the PROCESSORS_LIST config
"""
class ChainProcessor(AbstractListProcessor):



    config = {}

    def __init__(self,config):
        self.config = config


    def process(self,item):

        if self.config[PROCESSORS_LIST] is not None:

            # items MUST be a list
            if not isinstance(item,list):
                items = [item]
            else:
                items = item

            for p in self.config[PROCESSORS_LIST]:
                if not isinstance(p,AbstractProcessor):
                    raise "Set a non-processor element in the processor chain config " + str(p)
                logger.info("Starting processor "+str(p)+"with "+str(len(items))+" items")
                items = p.processList(items)
                logger.info("Obtained "+str(len(items))+" items")
            return items
        else:
            raise "No processor chain defined. Set it in the config"


class ModifierProcessor(AbstractListProcessor):

    __config = {}

    def __init__(self,config):
        self.__config = config

    def process(self,item):
        result = []
        if MODIFIERS_LIST in self.__config and not self.__config[MODIFIERS_LIST] is None:
            for modifier in self.__config[MODIFIERS_LIST]:
                if not isinstance(modifier,AbstractModifier):
                    raise "Unknown modifier in the modifiers list " + str(modifier)
                else:
                    logger.debug("Modifying "+str(item.getValue())+" using "+ str(modifier))
                    result = modifier.modify(item)
        else:
            logger.warn("Nothing to modify : no list of modifiers")
            result = [item]


        return result


""" Base class for modifiers
    Implements the identity modifier (returns the same item passed, as list)
"""
class AbstractModifier:

    config = {}

    def __init__(self,config):
        self.config = config


    def modify(self,item):
        # TO Implement by subclasses
        return [item]

    def setValue(self,value):
        pass

""" Apply more than 1 processor to the same items list, and get the result as a single list """
class ParalelProcessor(AbstractListProcessor):

    config = {}

    def __init__(self,config):
        self.config = config
        if (not PROCESSORS_LIST in self.config) or (self.config[PROCESSORS_LIST] is None):
            logger.error("Bad configuration : need a processor list")
            raise "Bad configuration : need a processors list"


    def process(self,item):

        result =[]
        for processor in self.config[PROCESSORS_LIST]:
            pResult = processor.process(item)
            if pResult is not None:
                result.extend(pResult)
            else:
                logger.warning("Result = None using processor : "+str(processor))

        return result



# The conditions list
CONDITIONS_LIST = "conditionslist"
# The condition evaluation
CONDITION_EVALUATION = "conditionevaluation"

# CONDITION EVALUATION TYPES
CONDITION_EVALUATION_MUSTALL = "mustall"
CONDITION_EVALUATION_NOTALL = "notall"
CONDITION_EVALUATION_ATLEASTONE = "atleastone"

""" Processor with some conditions
    Only items that accomplish the conditions will be return
"""
class ConditionalProcessor(AbstractListProcessor):

    config = {}

    def __init__(self,config):
        self.config = config
        if CONDITIONS_LIST not in config or config[CONDITIONS_LIST] is None:
            raise "Bad configuration : must provide at least one condition"
        else:
            # TODO Check that all conditions are instance of AbstractCondition
            pass

    def process(self,item):

        if self.__evaluateConditions(item):
            return [item]
        return []

    def __evaluateConditions(self,item):
        #Evaluate conditions depending on the condition evaluation type
        if self.config[CONDITION_EVALUATION]==CONDITION_EVALUATION_MUSTALL:
            return self.__evaluateMustAll(item)
        elif self.config[CONDITION_EVALUATION]==CONDITION_EVALUATION_NOTALL:
            return self.__evaluateNotAll(item)
        elif self.config[CONDITION_EVALUATION]==CONDITION_EVALUATION_ATLEASTONE:
            return self.__evaluateAtLeastOne(item)
        else:
            return True

    def __evaluateMustAll(self,item):

        for c in self.config[CONDITIONS_LIST]:
            if not c.evaluate(item):
                # DBG condition c not passed
                #print "Condition %s not passed",str(c)
                logger.info("Not passed condition "+str(c))
                return False
        return True

    def __evaluateNotAll(self,item):

        for c in self.config[CONDITIONS_LIST]:
            if c.evaluate(item):
                # print "Condition %s not passed",str(c)
                return False
        return True

    def __evaluateAtLeastOne(self,item):
        for c in self.config[CONDITIONS_LIST]:
            if c.evaluate(item):
                return True
        # DBG no condition passed for the item
        print "No condition passed"
        return False


""" Base class for conditions """
class AbstractCondition:

    config = {}

    def __init__(self,config):
        self.config = config


    def evaluate(self,item):
        ## Not a real condition
        return True

PROCESS_WAIT_MIN = "process_wait_min"
PROCESS_WAIT_MAX = "process_wait_max"
PROCESS_WAIT_RND = "process_wait_random"
""" Sleeps a random amount of time (seconds) for each item processed
    Uses sleepmin and sleepmax for the amount of time to sleep.
    Randomly, for each (if not random, fix to sleep min)
    And does just it, returning the same element.
"""
class WaitProcessor(AbstractListProcessor):

    __time_min = 0
    __time_max = 0
    __time_random = False;


    def __init__(self,config):
        self.config = config
        self.__time_min = config[PROCESS_WAIT_MIN]
        self.__time_max = config[PROCESS_WAIT_MAX]
        self.__time_random = config[PROCESS_WAIT_RND]


    def process(self,item):
        self.__sleep(item)
        return [item]


    def __sleep(self,item):
        time = self.__time_min
        if self.__time_random:
            # sleep randomly
            time =random.uniform(self.__time_min,self.__time_max)

        logger.info("Sleeping seconds : " +  str(time) +" on " + str(item.getValue()))
        sleep(time)


