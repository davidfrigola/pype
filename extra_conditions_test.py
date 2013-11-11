

from pype.extra_conditions import *
from pype.core import *
from pype.extra import *

import re

base = BaseItem(None)
base.setValue("text with isthere text in")

containsText = ContainsTextCondition({"value":"isthere"})
noContainsText = ContainsTextCondition({"value":"NOTHERE"})
noContainsText2 = ContainsTextCondition({"value":"OTHER_NOT_CONTAINED_TEXT"})
print containsText.evaluate(base)
print noContainsText.evaluate(base)

conditionalProcessor = ConditionalProcessor({CONDITIONS_LIST:[containsText,noContainsText],CONDITION_EVALUATION:CONDITION_EVALUATION_ATLEASTONE})

result = conditionalProcessor.processList([base])
for e in result:
    print e.getValue();


conditionalProcessor = ConditionalProcessor({CONDITIONS_LIST:[containsText,noContainsText],CONDITION_EVALUATION:CONDITION_EVALUATION_MUSTALL})

result = conditionalProcessor.processList([base])
print "Should be 0 : " + str(len(result))


conditionalProcessor = ConditionalProcessor({CONDITIONS_LIST:[noContainsText2,noContainsText],CONDITION_EVALUATION:CONDITION_EVALUATION_NOTALL})

result = conditionalProcessor.processList([base])
print "Should be 1 : " + str(len(result))

