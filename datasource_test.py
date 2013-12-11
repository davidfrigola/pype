
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

from pype.extra_conditions import *
from pype.core import *
from pype.extra import *
from pype.datasource import *

item = BaseItem({"m1":"v1","m2":"v2"})
item.setValue("The Item Value")


datasource = MongoDataSource({MONGO_DATASOURCE_CONFIG:{MONGO_DATABASE:"pype_test",MONGO_COLLECTION:"test_collection"}})


datasource.store(item)
print "Exists? " + str(datasource.exists(item))
print "Item : " +str(datasource.get(item))

result = datasource.all()
for e in result:
    print "Element : " + str(e.getValue()+"-"+str(e.getMetadataValue("m1")) +"-"+ str(e.getHash()))

datasource.delete(item)

