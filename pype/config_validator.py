from pype.core import AbstractConfigValidator, VALIDATORS_LIST,\
    MultipleConfigValidator
import logging

logger = logging.getLogger("pype.config.validator")
# Configuration validators

class NoNoneConfigValidator(AbstractConfigValidator):

    def validate(self,config):

        return config is not None



KEY_VALUE = "key_value"
class ContainsKeyConfigValidator(AbstractConfigValidator):


    def validate(self,config):

        result =  self.config[KEY_VALUE] in config
        logger.debug("Checking for " + self.config[KEY_VALUE] + " in " + str(config) + ":" + str(result))
        return result

KEYS_LIST = "keys_list"
class ContainsKeysConfigValidator(AbstractConfigValidator):


    def validate(self,config):

        validatorslist = [NoNoneConfigValidator(None)]
        # GEnerate key validators
        for key in self.config[KEYS_LIST]:
            validatorslist.extend([ContainsKeyConfigValidator({KEY_VALUE:str(key)})])


        multipleValidator = MultipleConfigValidator({VALIDATORS_LIST:validatorslist})

        return multipleValidator.validate(config)

INSTANCEOF_DICT="instanceof_dict"
class ContainsKeyAndInstanceConfigValidator(AbstractConfigValidator):

    """ Checks if the configuration dict contains all keys, and values are instance of the ones provided as validator config

        Sample config
        {"list":type([])} : will check a list in a "list" key in the config dict
    """



    def validate(self,config):
        for key in self.config:

            if not key in config:
                logger.warn("Key " + str(key) + " is not in the configuration")
                return False
            else:
                if not isinstance(config[key],self.config[key]):
                    return False

        # All OK
        return True

