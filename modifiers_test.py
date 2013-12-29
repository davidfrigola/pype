from pype.modifiers import *
from pype.extra import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

base = BaseItem({"parent":None})
base.setValue("This is my value")

addTESTModifier = PrependStringModifier({"prependvalue":"____PREPEND___TEST___"})
removePREPENDModifier = RemoveStringModifier({REMOVE_VALUE:"PREPEND"})
modifierProcessor = ModifierProcessor({MODIFIERS_LIST:[addTESTModifier]})

result = modifierProcessor.process(base)

modifierProcessor = ModifierProcessor({MODIFIERS_LIST:[removePREPENDModifier]})

result = modifierProcessor.processList(result)

for e in result:
    print e.getValue() + "<<<" + e.getMetadataValue("parent").getValue()



