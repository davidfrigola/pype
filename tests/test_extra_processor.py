from pype.extra_processor import *
from pype.model import *

item1 = BaseItem(None)
item1.setValue("item1")
item2 = BaseItem(None)
item2.setValue("item2")

items = [item1,item2]

def prepend_items_test():
    addItem1 = BaseItem(None)
    addItem1.setValue("addItem1")
    addItem2 = BaseItem(None)
    addItem2.setValue("addItem2")
    prependItems = [addItem1,addItem2]
    prependProcessor = AddItemsProcessor({ADDITEMS_PREPEND:prependItems})
    result = prependProcessor.processList(items)

    assert len(result)==len(items) + len(prependItems)


def postpend_items_test():
    addItem1 = BaseItem(None)
    addItem1.setValue("addItem1")
    addItem2 = BaseItem(None)
    addItem2.setValue("addItem2")
    postpendItems = [addItem1,addItem2]
    postpendProcessor = AddItemsProcessor({ADDITEMS_POSTPEND:postpendItems})
    result = postpendProcessor.processList(items)

    assert len(result)==len(items) + len(postpendItems)


def prepostpend_items_test():
    addItem1 = BaseItem(None)
    addItem1.setValue("addItem1")
    addItem2 = BaseItem(None)
    addItem2.setValue("addItem2")
    addItems = [addItem1,addItem2]
    addItemsProcessor = AddItemsProcessor({ADDITEMS_POSTPEND:addItems,ADDITEMS_PREPEND:addItems})
    result = addItemsProcessor.processList(items)

    assert len(result)==len(items) + (2 * len(addItems))


def logitem_nomodify_test():
    item1 = BaseItem(None,"item1")
    item2 = BaseItem(None,"item2")

    processor = LogItemsProcessor(None)
    result = processor.processList([item1,item2])

    assert result[0] == item1
    assert result[1] == item2