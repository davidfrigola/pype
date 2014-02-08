from pype.core import *

# Defition of a sample config validator
# Just checks that the configuration contains a "valid" key
class SampleConfigValidator(AbstractConfigValidator):

    def __init__(self,config):
        pass

    def validate(self,config):
        return "valid" in config

# Testing with a valid configuration
try:
    processor=AbstractListProcessor({"valid":True,CONFIG_VALIDATOR:SampleConfigValidator(None)})
except:
    print "This should not happen [1]"

# Testing with an invalid configuration
try:
    processor=AbstractListProcessor({"novalid":True,CONFIG_VALIDATOR:SampleConfigValidator(None)})
    print "This should not happen [2]"
except:
    print "Expected config error here"
