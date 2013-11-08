from core import AbstractListProcessor,AbstractProcessor

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