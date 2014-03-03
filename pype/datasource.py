import logging
from core import *
from config_validator import *
from pype.config_validator import KEY_VALUE

logger = logging.getLogger("pype.datasource")


class AbstractDataSource:

    def __init__(self,config):
        pass

    def exists(self,item):
        pass

    def store(self,item):
        pass

    def get(self,item):
        pass

    def update(self,item):
        pass

    def delete(self,item):
        pass

    def all(self):
        pass


from pymongo import MongoClient
import datetime

MONGO_DATASOURCE_CONFIG = "mongodatasourceconfig"
MONGO_DATABASE = "database"
MONGO_COLLECTION = "collection"

class MongoDataSource(AbstractDataSource):

    __config = None

    __mongoClient = None

    __mongoDatabaseName = "dry_database"

    __mongoCollectionName = "dry_collection"

    __collection = None

    def __init__(self,config):

        self.__config = config

        if MONGO_DATASOURCE_CONFIG in config:
            logger.info("Datasource configuration provided : "
                        + "DB:" + str(config[MONGO_DATASOURCE_CONFIG][MONGO_DATABASE])
                        + " COLLECTION : " + str(config[MONGO_DATASOURCE_CONFIG][MONGO_COLLECTION]))

            self.__mongoDatabaseName=config[MONGO_DATASOURCE_CONFIG][MONGO_DATABASE]
            self.__mongoCollectionName = config[MONGO_DATASOURCE_CONFIG][MONGO_COLLECTION]
            ## TODO get mongoClient based on config with user/pass
            self.__mongoClient = MongoClient()

        else:
            logger.info("Created mongo client without config params (default)")
            self.__mongoClient = MongoClient()

        ## Obtain collection
        self.__collection = self.__mongoClient[self.__mongoDatabaseName][self.__mongoCollectionName]

    def exists(self,item):
        ## TODO configurable 'hash' field
        return not self.get(item) is None

        pass

    def store(self,item):
        logger.debug("Storing "+str(item))

        self.__collection.insert({"hash":item.getHash(),
                                  "value":item.getValue(),
                                 # "metadata":item.metadata,
                                  "timestamp":datetime.datetime.utcnow()})

    def get(self,item):

        return self.__collection.find_one({"hash":item.getHash()})

    def update(self,item):
        #TODO
        pass

    def delete(self,item):
        logger.warning("Deleting item " + str(item.getHash()))
        self.__collection.remove({"hash":item.getHash()})

    def all(self):

        result = []
        dbResult = self.__collection.find();
        for dbEntity in dbResult:
            item = BaseItem(dbEntity["metadata"])
            item.setValue(dbEntity["value"])
            result.append(item)

        return result



#Issue #26



import redis

REDIS_DATASOURCE_CONFIG = "redis_datasource_config"
REDIS_DATASOURCE_CONFIG_HOST = "redis_datasource_config_host"
REDIS_DATASOURCE_CONFIG_PORT = "redis_datasource_config_port"
REDIS_DATASOURCE_CONFIG_DB = "redis_datasource_config_db"
class RedisDataSource(AbstractDataSource):

    _r = None
    def __init__(self,config):
        if self._validateConfig(config):
            self._r = redis.StrictRedis(host=config[REDIS_DATASOURCE_CONFIG][REDIS_DATASOURCE_CONFIG_HOST],
                                        port=config[REDIS_DATASOURCE_CONFIG][REDIS_DATASOURCE_CONFIG_PORT],
                                        db=config[REDIS_DATASOURCE_CONFIG][REDIS_DATASOURCE_CONFIG_DB])
            logger.debug("Obtained internal redis handler" + str(self._r))
        else:
            raise BaseException("Error validating config ")


    def update(self,item):
        self.store(item)

    def store(self,item):
        self._r.set(item.getHash(), item.getValue())

    def get(self,item):
        return self._r.get(item.getHash())

    def exists(self,item):
        return self.get(item) is not None

    def all(self):

        result = []
        # Obtain all keys
        keys = self._r.keys()

        #For each key, get value
        for k in keys:
            value = self._r.get(k)
            result.append(BaseItem({"origin":"redis"},value))
        #return result
        return result

    def _validateConfig(self,config):

        validator = MultipleConfigValidator(
                        {VALIDATORS_LIST:[ContainsKeyConfigValidator({KEY_VALUE:REDIS_DATASOURCE_CONFIG})]})
        if not validator.validate(config):
            raise BaseException("Config validation error : does not contain " + REDIS_DATASOURCE_CONFIG)

        # Validate redis datasource config
        validator = MultipleConfigValidator(
                        {VALIDATORS_LIST:[ContainsKeysConfigValidator({KEYS_LIST:[REDIS_DATASOURCE_CONFIG_DB,
                                                                                  REDIS_DATASOURCE_CONFIG_HOST,
                                                                                  REDIS_DATASOURCE_CONFIG_PORT]})]})

        if not validator.validate(config[REDIS_DATASOURCE_CONFIG]):
            raise BaseException("Config validation error : config not complete ")

        return True


    def delete(self,item):
        self._r.delete(item.getHash())
