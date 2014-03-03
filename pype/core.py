import logging

from model import *

logger = logging.getLogger("pype")

class AbstractProcessor:
    """ Abstract Processor Base Class
        - Defines the base API for a processor
        - Does not implement anything (that's abstract)

    """
    config = {}

    def __init__(self,config):
        """ The config object should contain all the configuration needed

        """
        if not self.validateConfig(config):
            raise BaseException("Config validation error")
        else:
            self.config = config


    def process(self,item):
        """ Process an item """
        pass


    def processList(self,items):
        """ Process a list of items """
        pass

    def validateConfig(self,config):
        logger.warning("No validation override in the processor.")
        return True

class AbstractListProcessor(AbstractProcessor):
    """ Implements list processing
        Uses the process method for each element in the list.
    """

    def processList(self,items):
        result = []
        for item in items:
            processedItem = self.process(item)
            if processedItem is not None:
                result = result + processedItem
            else:
                logger.warning("Processed item %s returns [] empty array",str(item))

        return result


CONFIG_VALIDATOR = "config_validator"
class AbstractConfigValidator:

    config = {}

    def __init__(self,validatorconfig = {}):

        self.config = validatorconfig

    def validate(self,config):

        pass


class FakeConfigValidator(AbstractConfigValidator):

    def validate(self,config):
        return True

VALIDATORS_LIST = "validators_list"

class MultipleConfigValidator(AbstractConfigValidator):

    def validate(self,config):

        if(VALIDATORS_LIST in self.config and self.config[VALIDATORS_LIST] is not None):
            for v in self.config[VALIDATORS_LIST]:
                if not v.validate(config):
                    logger.error("Validator "+str(v)+" does not validate this config.")
                    return False
        else:
            raise "Error : Needs a list of validators"

        # All validators return True
        return True

