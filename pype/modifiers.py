from pype.core import *
from pype.extra import AbstractModifier
import logging

logger = logging.getLogger("pype.modifiers")

PREPEND_VALUE = "prependvalue"

""" Prepends a string to the value of the item (should be a string) """
class PrependStringModifier(AbstractModifier):

    def __init__(self,config):
        self.config = config
        if (not PREPEND_VALUE in config) or config[PREPEND_VALUE] is None:
            logger.error("Configuration must contain "+PREPEND_VALUE)
            raise "Configuration must contain "+PREPEND_VALUE

    def modify(self,item):

        logger.debug("Prepending "+str(self.config[PREPEND_VALUE]))


        itemResult = BaseItem({"parent":item})
        itemResult.setValue(str(self.config[PREPEND_VALUE]) + str(item.getValue()))

        logger.debug("Modification result " + str(itemResult.getValue()))
        return [itemResult]

    def setValue(self,value):
        self.config = {PREPEND_VALUE:value}


REMOVE_VALUE = "remove_value"

class RemoveStringModifier(AbstractModifier):

    def __init__(self,config):
        self.config = config
        if (not REMOVE_VALUE in config) or config[REMOVE_VALUE] is None:
            logger.error("Configuration must contain "+REMOVE_VALUE)
            raise "Configuration must contain "+REMOVE_VALUE

    def modify(self,item):

        itemResult = BaseItem({"parent":item})
        logger.debug("Removing value "+self.config[REMOVE_VALUE])
        newValue = item.getValue()
        newValue = newValue.replace(self.config[REMOVE_VALUE],'')
        itemResult.setValue(newValue)

        logger.debug("Modification result " + str(itemResult.getValue()))
        return [itemResult]

    def setValue(self,value):
        self.config = {REMOVE_VALUE:value}
"""
    Modifies item using metadata values
"""
METADATA_STRING_MODIFY_FROM_ANCESTOR = "metadata_string_modify_from_parent"
METADATA_STRING_MODIFY_FROM_VALUE = "metadata_string_modify_from_value"
METADATA_STRING_MODIFY_MODIFIER = "metadata_string_modify_modifier"

class FromMetadataStringModifier(AbstractModifier):

    __config = None

    def __init__(self,config):
        self.__config = config
        pass

    def modify(self,item):

        baseItem = item
        if METADATA_STRING_MODIFY_FROM_ANCESTOR in self.__config:
            for i in range(int(self.__config[METADATA_STRING_MODIFY_FROM_ANCESTOR])):
                baseItem = baseItem.getMetadataValue("parent")

        logger.debug("Item "+str(baseItem))
        logger.debug(" Value from item " + str(self.__config[METADATA_STRING_MODIFY_FROM_VALUE]))
        valueForModifier = baseItem.getMetadataValue(str(self.__config[METADATA_STRING_MODIFY_FROM_VALUE]))

        logger.debug("Value for modifer " + str(valueForModifier))

        modifier = self.__config[METADATA_STRING_MODIFY_MODIFIER]
        modifier.setValue(valueForModifier)

        return modifier.modify(item)

""" Postpends a string to the value of the item (should be a string) """
POSTPEND_VALUE = "postpend_value"
class PostpendStringModifier(AbstractModifier):

    def __init__(self,config):
        self.config = config
        if (not POSTPEND_VALUE in config) or config[POSTPEND_VALUE] is None:
            logger.error("Configuration must contain "+POSTPEND_VALUE)
            raise "Configuration must contain "+POSTPEND_VALUE

    def modify(self,item):

        logger.debug("Postpending "+str(self.config[POSTPEND_VALUE]))


        itemResult = BaseItem({"parent":item})
        itemResult.setValue(str(item.getValue())+ str(self.config[POSTPEND_VALUE]))

        logger.debug("Modification result " + str(itemResult.getValue()))
        return [itemResult]

    def setValue(self,value):
        self.config = {POSTPEND_VALUE:value}


