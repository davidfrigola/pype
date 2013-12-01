
from pype.extra_conditions import *
from pype.core import *
from pype.extra import *
from pype.datasource import *

item = BaseItem(None)
item.setValue("The Item Value")

datasource = MongoDataSource({})

datasource.store(item)
print "Exists? " + str(datasource.exists(item))
print "Item : " +str(datasource.get(item))

