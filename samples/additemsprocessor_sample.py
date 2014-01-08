from pype.extra_processor import *
from pype.core import *

item1 = BaseItem(None,"item1")
item2 = BaseItem(None,"item2")
processor = AddItemsProcessor({ADDITEMS_PREPEND:[item1],ADDITEMS_POSTPEND:[item1]})

result = processor.processList([])

for e in result:
    print str(e)