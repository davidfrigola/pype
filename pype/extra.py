from core import AbstractListProcessor,AbstractProcessor
import random
from time import sleep

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
                items = p.processList(items)

            return items
        else:
            raise "No processor chain defined. Set it in the config"


class ModifierProcessor(AbstractListProcessor):

    def __init__(self,config):
        self.config = config

    def process(self,item):
        result = []
        for modifier in self.config[MODIFIERS_LIST]:
            if not isinstance(modifier,AbstractModifier):
                raise "Unknown modifier in the modifiers list " + str(modifier)
            else:
                result = modifier.modify(item)

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


""" Apply more than 1 processor to the same items list, and get the result as a single list """
class ParalelProcessor(AbstractListProcessor):

    config = {}

    def __init__(self,config):
        self.config = config
        if (not PROCESSORS_LIST in self.config) or (self.config[PROCESSORS_LIST] is None):
            raise "Bad configuration : need a processors list"


    def process(self,item):

        result =[]
        for processor in self.config[PROCESSORS_LIST]:
            pResult = processor.process(item)
            if pResult is not None:
                result.extend(pResult)
            else:
                # WARNING : TODO : logger?
                pass

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
                return False
        return True

    def __evaluateNotAll(self,item):

        for c in self.config[CONDITIONS_LIST]:
            if c.evaluate(item):
                # DBG condition c not passed
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
        return true

PROCESS_SLEEP_MIN = "sleepmin"
PROCESS_SLEEP_MAX = "sleepmax"
PROCESS_SLEEP_RND = "sleeprandom"
""" Sleeps a random amount of time (seconds) for each item processed
    Uses sleepmin and sleepmax for the amount of time to sleep.
    Randomly, for each
    And does just it, returning the same element.
"""
class SleepProcessor(AbstractListProcessor):

    __time_min = 0
    __time_max = 0
    __time_random = False;


    def __init__(self,config):
        self.config = config
        self.__time_min = config[PROCESS_SLEEP_MIN]
        self.__time_max = config[PROCESS_SLEEP_MAX]
        self.__time_random = config[PROCESS_SLEEP_RND]


    def process(self,item):
        self.__sleep()
        return [item]


    def __sleep(self):
        time = self.__time_min
        if self.__time_random:
            # sleep randomly
            time =random.uniform(self.__time_min,self.__time_max)

        print "Sleeping %s sec" + str(time)
        sleep(time)
