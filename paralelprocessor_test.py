from pype.modifiers import *
from pype.extra import *

base = BaseItem({"parent":None})
base.setValue("This is my value")

addTESTModifier1 = PrependStringModifier({"prependvalue":"1____PREPEND___TEST___1"})
addTESTModifier2 = PrependStringModifier({"prependvalue":"2____PREPEND___TEST___2"})
modifierProcessor1 = ModifierProcessor({"modifierslist":[addTESTModifier1]})
modifierProcessor2 = ModifierProcessor({"modifierslist":[addTESTModifier2]})

paralelProcessor = ParalelProcessor({"processorslist":[modifierProcessor1,modifierProcessor2]})

result = paralelProcessor.process(base)
for e in result:
    print e.getValue() + "<<<<" + str(e.getMetadataValue("parent"))
