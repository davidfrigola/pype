from pype.datasource import RedisDataSource, REDIS_DATASOURCE_CONFIG,\
    REDIS_DATASOURCE_CONFIG_HOST, REDIS_DATASOURCE_CONFIG_PORT,\
    REDIS_DATASOURCE_CONFIG_DB
from pype.storage import RedisStoreProcessor, REDIS_DATASOURCE, RedisGetProcessor
from pype.model import BaseItem

# REDIS Processor Sample
# Requires a valid redis server running

# Datasource config values
redisds = RedisDataSource({REDIS_DATASOURCE_CONFIG:{REDIS_DATASOURCE_CONFIG_HOST:"192.168.10.10",
                                                    REDIS_DATASOURCE_CONFIG_PORT:"6379",
                                                    REDIS_DATASOURCE_CONFIG_DB:"test"}})

store_processor = RedisStoreProcessor({REDIS_DATASOURCE:redisds})

# Store 10 items
items = []
for i in range(10):
    items.append(BaseItem({},"item"+str(i)))

result = store_processor.processList(items)

# Obtains values
get_processor = RedisGetProcessor({REDIS_DATASOURCE:redisds})

getresult = get_processor.process(BaseItem({},"ignore"))

for e in getresult:
    print str(e)

