from pype.modifiers import *
from pype.extra import *

base = BaseItem({"parent":None})
base.setValue("This is my value")

addTESTModifier = PrependStringModifier({"prependvalue":"____PREPEND___TEST___"})
modifierProcessor = ModifierProcessor({"modifierslist":[addTESTModifier]})

result = modifierProcessor.process(base)

for e in result:
    print e.getValue() + "<<<" + e.getMetadataValue("parent").getValue()
