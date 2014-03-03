from extra import *
from extra_conditions import *
from logging import *

logger = logging.getLogger("pype.extra.processor")


#---------------------------------------------------------------------------
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

#---------------------------------------------------------------------------

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
SCRIPT_EXEC_ITEMVALUEASCOMMAND = "exectuescriptitemvalueascommand"

#SCRIPT_EXEC_OS = "executescriptos"
#SCRIPT_EXEC_OS_NIX = "executescriptosnix"
#SCRIPT_EXEC_OS_WIN = "executescriptoswin"

#SCRIPT_EXEC_COMMAND_PARAM_ITEM_VALUE = "executescriptcommandparamitemvalue"
class ScriptProcessor(AbstractProcessor):


    __config = {}
    __mode = None

    def __init__(self,config):
        self.__config = config
        ##TODO Validate config
        if not SCRIPT_EXEC_MODE in config:
            raise "ScriptProcessor requires execution mode set in config"
        else:
            self.__mode = config[SCRIPT_EXEC_MODE]


    def process(self,item):
        if self.__mode==SCRIPT_EXEC_PERITEM:

            self.__executescript(item)

        else:
            self.__executescript(None)

        return [item]

    def processList(self,items):
        """ Process a list of items """
        if self.__mode == SCRIPT_EXEC_ONCE:
            self.__executescript(None)
        else:
            result = []
            for item in items:

                result = result + self.process(item)




    def __executescript(self,item):

        #see http://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
        #see http://stackoverflow.com/questions/14894993/running-windows-shell-commands-with-python
        # os or subprocess??s
        if SCRIPT_EXEC_ITEMVALUEASCOMMAND in self.__config and self.__config[SCRIPT_EXEC_ITEMVALUEASCOMMAND]:

            scriptcommand = item.getValue()
        else:
            scriptcommand = self.__config[SCRIPT_EXEC_COMMAND]


        logger.info("Executing script " + str(scriptcommand) + "for item " + str(item))
        import os

        os.system(scriptcommand)



#---------------------------------------------------------------------------
ADDITEMS_PREPEND = "additems_prepend"
ADDITEMS_POSTPEND = "additems_postpend"
ADDITEMS_DATASOURCE = "additems_datasource"
class AddItemsProcessor(AbstractListProcessor):
    """
        Add fixed items to the stream.

    """
    __config = {}

    __itemstoprepend = None
    __itemstopostpend = None
    __datasoruce = None
    def __init__(self,config):
        self.__config = config
        if ADDITEMS_PREPEND in config:
            self.__itemstoprepend = config[ADDITEMS_PREPEND]
        if ADDITEMS_POSTPEND in config:
            self.__itemstopostpend = config[ADDITEMS_POSTPEND]
        if ADDITEMS_DATASOURCE in config:
            self.__datasoruce = config[ADDITEMS_DATASOURCE]

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
            result = result + self.__itemstopostpend

        if self.__datasoruce is not None:
            result = result + self.__datasource.all()
        return result


LOGITEMS_MODE = "logitems_mode"
LOGITEMS_MODE_LOGGER = "logitems_mode_logger"
LOGITEMS_MODE_STDOUT = "logitems_mode_stdout"

class LogItemsProcessor(AbstractListProcessor):
    """
        Just a logger for items in the stream (debug/trace purposes)
        Two modes available:
        * STDOUD (default if not set in config) prints the item
        * LOGGER : uses INFO level to log to the configured logger
    """
    __config = {}

    def __init__(self,config):
        if config is not None:
            self.__config = config

    def process(self,item):
        if not LOGITEMS_MODE in self.__config:
            # default mode stdout
            self.__config = {LOGITEMS_MODE : LOGITEMS_MODE_STDOUT}

        if self.__config[LOGITEMS_MODE] == LOGITEMS_MODE_LOGGER:
            logger.info(str(item))
        else:
            #default
            print str(item)

        return [item]