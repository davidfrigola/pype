import logging

from core import *
from model import *

logger = logging.getLogger("pype.config.validator")
# Configuration validators

class NoNoneConfigValidator(AbstractConfigValidator):

    def validate(self,config):

        return config is not None



KEY_VALUE = "key_value"
class ContainsKeyConfigValidator(AbstractConfigValidator):


    def validate(self,config):
        return self.config[KEY_VALUE] in config


KEYS_LIST = "keys_list"
class ContainsKeysConfigValidator(AbstractConfigValidator):


    def validate(self,config):

        validatorslist = [NoNoneConfigValidator(None)]
        # GEnerate key validators
        for key in self.config[KEYS_LIST]:
            validatorslist.extend([ContainsKeyConfigValidator({KEY_VALUE:str(key)})])


        multipleValidator = MultipleConfigValidator({VALIDATORS_LIST:validatorslist})

        return multipleValidator.validate(config)



