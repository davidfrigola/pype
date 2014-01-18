from pype.model import *

def metadata_model_test():
    item = BaseItem({"key1":"value1"})
    item.setMetadataValue("key2","value2")

    assert item.getMetadataValue("key1")=="value1"
    assert item.getMetadataValue("key2")=="value2"

    assert item.getMetadataValue("keynotinmetadata")==None

def metadata_model_value_test():

    item = BaseItem(None,"value")

    assert item.getValue() == "value"
def metadata_creation_on_set_test():

    item = BaseItem(None)

    item.setMetadataValue("key2","value2")

    assert item.getMetadataValue("key2")=="value2"

def set_parent_test():

    item = BaseItem(None)

    item.setParent("parent")

    assert item.getParent()=="parent"

    assert item.getMetadataValue("parent")=="parent"

def gethash_default_test():

    item = BaseItem(None,"value")

    hash = item.getHash()

    assert hash is not None

def gethash_onlyOnce_test():

    item = BaseItem({HASH_ONCE:True},"value")

    hash1 = item.getHash()
    hash2 = item.getHash()

    assert hash1 == hash2

def gethash_valueashash_test():
    item = BaseItem({VALUE_AS_HASH:True},"value")

    assert "value" == item.getHash()

def getid_samevalueashash_test():

    item = BaseItem(None,"value")

    assert item.getId() == item.getHash()
