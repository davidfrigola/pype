from extra import *
from extra_conditions import *
from logging import *

logger = logging.getLogger("pype.extra.processor")
"""
DRY Processor : do not repeat yourself processor

Uses conditional processor, and a NOT_ALL condition with AlreadyProcessedCondition against
a Mongo datasource

"""
METADATA_DRY_FLAG = "dry_processed"
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
           item.setMetadataValue(METADATA_DRY_FLAG,True)
           return [item]


""" Script processor
 Executes a script
  * Per item
  * Only once
  * Command (fixed command value)

"""
SCRIPT_EXEC_MODE = "executescriptmode"
SCRIPT_EXEC_ONCE = "executescriptonce"
SCRIPT_EXEC_PERITEM = "executescriptperitem"
SCRIPT_EXEC_COMMAND = "executescritpcommand"
SCRIPT_EXEC_COMMAND_VALUE = "executescritpcommandvalue"
SCRIPT_EXEC_ITEMVALUEASCOMMAND = "exectuescriptitemvalueascommand"
SCRIPT_EXEC_OS = "executescriptos"
SCRIPT_EXEC_OS_NIX = "executescriptosnix"
SCRIPT_EXEC_OS_WIN = "executescriptoswin"

#SCRIPT_EXEC_COMMAND_PARAM_ITEM_VALUE = "executescriptcommandparamitemvalue"
class ScriptProcessor(AbstractProcessor):


    __config = {}
    __mode = None

    def __init__(self,config):
        self.__config = config
        ##TODO Validate config
        if not SCRIPT_EXEC_MODE in config:
            raise "ScriptProcessor requires execution mode set in config"


    def process(self,item):
        if self.__mode==SCRIPT_EXEC_PERITEM:

            self.__executescript(item)

        else:
            return [item]

    def processList(self,items):
        """ Process a list of items """
        if self.__mode == SCRIPT_EXEC_ONCE:
            self.__executescript(None)
        else:
            return super(ScriptProcessor,self).processList(items)




    def __executescript(self,item):
        ## TODO
        #see http://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
        #see http://stackoverflow.com/questions/14894993/running-windows-shell-commands-with-python
        # os or subprocess??s

        logger.info("Executing script " + str(self.__config[SCRIPT_EXEC_COMMAND]) + "for item " + str(item))

        # execute script with item value as parameter
        # just ignore the last parameter in the script
        pass

ADDITEMS_PREPEND = "additems_prepend"
ADDITEMS_POSTPEND = "additems_postpend"

class AddItemsProcessor(AbstractListProcessor):
    """
        Add fixed items to the stream.

    """
    __config = {}

    __itemstoprepend = None
    __itemstopostpend = None

    def __init__(self,config):
        self.__config = config
        if ADDITEMS_PREPEND in config:
            self.__itemstoprepend = config[ADDITEMS_PREPEND]
        if ADDITEMS_POSTPEND in config:
            self.__itemstopostpend = config[ADDITEMS_POSTPEND]


    def process(self,item):
        return self.__addItems([item])

    def processList(self,items):
        return self.__addItems(items)


    def __addItems(self,items):
        result = items
        if self.__itemstoprepend is not None:
            logger.debug("Prepending items")
            result = self.__itemstoprepend + result

        if self.__itemstopostpend is not None:
            logger.debug("Postpending items")
            result = result.extend(self.__itemstopostpend)
        return result
