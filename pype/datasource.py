import logging

logger = logging.getLogger("pype.datasource    ")


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

class MongoDataSource(AbstractDataSource):

    __config = None

    __mongoClient = None

    __mongoDatabaseName = "dry_database"

    __mongoCollectionName = "dry_collection"

    __collection = None

    def __init__(self,config):

        self.__config = config

        if MONGO_DATASOURCE_CONFIG in config:
            ## TODO get mongoClient based on config

            pass
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

        self.__collection.insert({"hash":item.getHash(),
                                  "value":item.getValue(),
                                  "timestamp":datetime.datetime.utcnow()})

    def get(self,item):

        return self.__collection.find_one({"hash":item.getHash()})

    def update(self,item):
        #TODO
        pass

    def delete(self,item):

        self.__collection.delete({"hash":item.getHash()})

