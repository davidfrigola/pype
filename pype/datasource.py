import logging

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
        print item.metadata
        self.__collection.insert({"hash":item.getHash(),
                                  "value":item.getValue(),
                                  "metadata":item.metadata,
                                  "timestamp":datetime.datetime.utcnow()})

    def get(self,item):

        return self.__collection.find_one({"hash":item.getHash()})

    def update(self,item):
        #TODO
        pass

    def delete(self,item):
        logger.warning("Deleting item " + str(item.getHash()))
        self.__collection.remove({"hash":item.getHash()})

