from pype.extra_processor import *
from pype.core import *


import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

item1 = BaseItem(None,"touch test2")

# executing script PER item, exec command = touch test
processor = ScriptProcessor({SCRIPT_EXEC_MODE:SCRIPT_EXEC_ONCE ,SCRIPT_EXEC_COMMAND:"touch test"})
result = processor.process(item1)


# executing script PER ITEM VALUE, command = item value (touch test 2)
processor = ScriptProcessor({SCRIPT_EXEC_MODE:SCRIPT_EXEC_PERITEM ,SCRIPT_EXEC_ITEMVALUEASCOMMAND:True})

result = processor.process(item1)

# executing script PER ITEM, exec command item value
item1.setValue("touch test3")
item2 = BaseItem(None,"touch test4")

result = processor.processList([item1,item2])
