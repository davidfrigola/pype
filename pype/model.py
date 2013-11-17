import logging
logger = logging.getLogger("pype.model")


""" Abstract Item """
class AbstractItem:
    """ Abstract item to process """
    metadata = {}
    value = None
    def __init__(self,metadata):
        pass


    def getMetadataValue(self,key):
        pass


""" Base item """
class BaseItem(AbstractItem):

    metadata = {}


    def __init__(self,metadata):
        if not metadata is None:
            self.metadata = metadata

    def setValue(self,value):
        self.value = value

    def getValue(self):
        return self.value

    def setParent(self,parent):
        pass

    def getParent(self):
        return self.metadata["parent"]

    def getMetadataValue(self,key):
        if (not self.metadata is None) and key in self.metadata:
            return self.metadata[key];
        logger.warn("Not found "+str(key)+" in metadata")
        return None

    def setMetadataValue(self,key,value):

        if self.metadata is None:
            self.metadata = {}
        self.metadata[key] = value