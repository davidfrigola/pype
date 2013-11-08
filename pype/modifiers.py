from pype.core import *
from pype.extra import AbstractModifier


PREPEND_VALUE = "prependvalue"

""" Prepends a string to the value of the item (should be a string) """
class PrependStringModifier(AbstractModifier):

    def __init__(self,config):
        self.config = config
        if (not PREPEND_VALUE in config) or config[PREPEND_VALUE] is None:
            raise "Configuration must contain "+PREPEND_VALUE

    def modify(self,item):

        itemResult = BaseItem({"parent":item})
        itemResult.setValue(self.config[PREPEND_VALUE] + item.getValue())


        return [itemResult]