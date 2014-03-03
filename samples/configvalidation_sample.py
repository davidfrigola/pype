import sys, traceback
#logging
import logging
from pype.config_validator import ContainsKeyConfigValidator, KEY_VALUE,\
    KEYS_LIST, ContainsKeysConfigValidator
from pype.core import AbstractConfigValidator, AbstractProcessor,\
    VALIDATORS_LIST, MultipleConfigValidator
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# Defition of a sample config validator
# Just checks that the configuration contains a "valid" key
class SampleConfigValidator(AbstractConfigValidator):

    def __init__(self,config=None):
        pass

    def validate(self,config):
        return "valid" in config
class SampleConfigOverrideProcessor(AbstractProcessor):

    __defaultConfigValidator = None

    def validateConfig(self,config):
        self.__defaultConfigValidator = SampleConfigValidator(config)
        return self.__defaultConfigValidator.validate(config)


# Testing with a valid configuration
try:
    processor=SampleConfigOverrideProcessor(config={"valid":True})
    print " OK - Valid configuration provided"
except:
    print "This should not happen [1]"
    traceback.print_exc(file=sys.stdout)

# Testing with an invalid configuration
try:
    processor=SampleConfigOverrideProcessor(config={"novalid":True})
    print "This should not happen [2]"
except:
    print " OK - Expected config error here"
    traceback.print_exc(file=sys.stdout)


# Testing multiple config validator

multipleValidator = MultipleConfigValidator({VALIDATORS_LIST:[SampleConfigValidator(),SampleConfigValidator()]})

print "Validates : " + str(multipleValidator.validate({"valid":True}))

multipleValidator =  MultipleConfigValidator({VALIDATORS_LIST:[ContainsKeyConfigValidator({KEY_VALUE:"valid"}),
                                                               ContainsKeysConfigValidator({KEYS_LIST:["valid","otherkey"]})]})

print "Validates 2 : " + str(multipleValidator.validate({"valid":True,"otherkey":True}))


print "Validates 3 : " + str(multipleValidator.validate({"valid":True,"otherkey-changed":True}))



