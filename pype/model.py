
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
        return self.metadata[key];

    def setMetadataValue(self,key,value):
        self.metadata[key] = value