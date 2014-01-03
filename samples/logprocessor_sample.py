from pype.extra_processor import *
from pype.core import *

item1 = BaseItem(None,"item1")

processor = LogItemsProcessor(None)

result = processor.processList([item1])
