from pype.model import *

def metadata_model_test():
    item = BaseItem({"key1":"value1"})
    item.setMetadataValue("key2","value2")

    assert item.getMetadataValue("key1")=="value1"
    assert item.getMetadataValue("key2")=="value2"

    assert item.getMetadataValue("keynotinmetadata")==None

def metadata_creation_on_set_test():

    item = BaseItem(None)

    item.setMetadataValue("key2","value2")

    assert item.getMetadataValue("key2")=="value2"

def set_parent_test():

    item = BaseItem(None)

    item.setParent("parent")

    assert item.getParent()=="parent"

    assert item.getMetadataValue("parent")=="parent"
