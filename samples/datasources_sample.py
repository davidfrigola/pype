from pype.datasource import RedisDataSource, REDIS_DATASOURCE_CONFIG,\
    REDIS_DATASOURCE_CONFIG_HOST, REDIS_DATASOURCE_CONFIG_PORT
from pype.model import BaseItem, HASH_ONCE

#logging
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


# DRY processor using REDIS

redisds = RedisDataSource({REDIS_DATASOURCE_CONFIG:{REDIS_DATASOURCE_CONFIG_HOST:"192.168.10.10",
                                                    REDIS_DATASOURCE_CONFIG_PORT:"6379"}})

nonexisting = redisds.get(BaseItem(None,"test"))
print "Non existing result " + str(nonexisting)

storedItem = BaseItem({HASH_ONCE:True},"stored value into redis")
redisds.store(storedItem)

existing = redisds.get(storedItem)

print "Existing value :[" + str(existing) + "] stored"
redisds.delete(storedItem)

print "The value has been deleted : should not be found ->" + str(redisds.get(storedItem))
