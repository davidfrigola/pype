from extra import *
from extra_conditions import *

"""
DRY Processor : do not repeat yourself processor

Uses conditional processor, and a NOT_ALL condition with AlreadyProcessedCondition against
a Mongo datasource

"""
DRY_METADATA_FLAG = "dry_processed"
class DRYProcessor(AbstractListProcessor):

    __config={}
    __alreadyExistsCondition = None
    __datasource = None
    def __init__(self,config):

        self.__config = config
        #TODO validate configuration
        self.__datasource = MongoDataSource(config)
        self.__alreadyExistsCondition = AlreadyProcessedCondition({ALREADY_PROCESSED_DATASOURCE:MongoDataSource(config)})



    def process(self,item):

        if(self.__alreadyExistsCondition.evaluate(item)):
            logger.warn("Skipping already processed item "+str(item))
            return None
        else:
           #Store item
           self.__datasource.store(item)
           logger.debug("Stored item - DRY processor "+str(item))
           #Set stored flag
           item.setMetadataValue(DRY_METADATA_FLAG,True)
           return [item]
