
from pype.html import *
from pype.extra import *
from pype.modifiers import *

htmlprocessor = HtmlProcessor({"find":{"h2":{"class":"title"}}})
h2processor = BSProcessor({"find":{"a":{"itemprop":"url"}}})
aprocessor = BSProcessor({"get":["href"]})

addBaseUrlModifier = PrependStringModifier({"prependvalue":"http://bandaancha.eu"})

modifierprocessor = ModifierProcessor({MODIFIERS_LIST:[addBaseUrlModifier]})

chain = ChainProcessor({PROCESSORS_LIST:[htmlprocessor,h2processor,aprocessor,modifierprocessor]})

base = BaseItem(None)
base.setValue("http://bandaancha.eu/")

result = chain.process(base)

for e in result:
    if e is None:
        print "NONE"
    else:
        print str(e.getValue()) +" <<<<< " +  str(e.getMetadataValue("parent").getValue())

chainSleep = ChainProcessor({PROCESSORS_LIST:[SleepProcessor({PROCESS_SLEEP_MIN:1,PROCESS_SLEEP_MAX:10,PROCESS_SLEEP_RND:True}),htmlprocessor]})

result = chainSleep.processList(result)

for e in result:
    if e is None:
        print "NONE"
    else:
        print str(e.getValue()) +" <<<<< " +  str(e.getMetadataValue("parent").getValue())