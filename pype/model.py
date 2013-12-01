import logging
import hashlib

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

    """ Obtain the hash-id like value for the item """
    def getHash(self):
        pass


HASH_ONCE = "hash_only_once"

""" Base item """
class BaseItem(AbstractItem):

    metadata = {}

    __hash = None

    def __init__(self,metadata):
        if not metadata is None:
            self.metadata = metadata

    def setValue(self,value):
        self.value = value

    def getValue(self):
        return self.value

    def setParent(self,parent):
        self.setMetadataValue("parent",parent)

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
        logger.debug("Setting "+str(key)+" - "+str(value)+" to metadata")
        self.metadata[key] = value

    """ Obtain hash sha512
        Based on a string value
    """
    def getHash(self):

        if HASH_ONCE in self.metadata and self.metadata[HASH_ONCE]:
            if self.__hash is None:
                logger.debug("Generating hash only once")
                self.__hash = haslib.sha512(str(self.getValue())).hexdigest()
        else:
            logger.debug/("Generating hash on demand. Use HASH_ONCE for only once generation")
            self.__hash = haslib.sha512(self.getValue()).hexdigest()

        return self.__hash

