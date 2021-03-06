import os
import urllib2
import datetime
from pype.model import BaseItem
import logging
from pype.core import AbstractListProcessor
from pype.config_validator import ContainsKeyAndInstanceConfigValidator
from pype.datasource import RedisDataSource

logger = logging.getLogger("pype.file")

# Folder in wich store files
FILE_FOLDER = "filefolder"
# Subfolder (within main folder) where store the files. Will be obtained from item metadata (if present)
FILE_SUBFOLDER_METADATA = "filesubfolder"
# Flag FILE_ADD_AS_METADATA: if true, adds to metadata the file
# if false, returns the file
FILE_ADD_AS_METADATA = "addasmetadata"
# Field name for file as metadata within the item
FILE_ADD_AS_METADATA_FIELD = "file"

FILE_NAME_NUMBER = "filenamenumber"

FILE_ADD_DATE = "file_add_date"

FILE_ADD_DATE_PREV_EXT = "file_add_date_prev_ext"

class AbstractFileProcessor(AbstractListProcessor):

    def getDateForFilename(self):
        now = datetime.datetime.now()
        return now.strftime("%Y%m%d_%H%M%S")

    def getFilenameWithDateTimePrevExtension(self,filename):

        result = filename
        #TODO
        lastDot = filename.rfind('.')
        if lastDot == 0:
            result = filename + self.getDateForFilename()
        else:
            result = filename[:lastDot] + "_" +  self.getDateForFilename() + filename[lastDot:]

        return result

""" Downloads a file from a url """
class FileDownloader(AbstractFileProcessor):

    __config = {}

    def __init__(self,config):

        self.__config = config;
        # Validate folder
        if not FILE_FOLDER in config:
            logger.error("You must specify a file folder")
            raise "You must specify a file folder"
        if not FILE_ADD_AS_METADATA in config:
            logger.error("You must specify the metadata FLAG")
            raise "You must specify the metadata FLAG"

    def process(self,item,file_name=None):

        downloadFileHandler = urllib2.urlopen(item.getValue())
        if file_name is None:
            file_name = item.getValue().split('/')[-1]
        directory = self.__config[FILE_FOLDER] + self.__getFileSubfolder(item)

        if not os.path.exists(directory):
            logger.info("Creating folder "+directory)
            os.makedirs(directory)

        # TODO use FILE_ADD_DATE to add date YYYYMMDDhhmm
        logger.info("Downloading filehandler to "+directory+file_name)

        filehandler = open(directory + file_name,'w')
        filehandler.write(downloadFileHandler.read())
        filehandler.close()
        # Return result
        if self.__config[FILE_ADD_AS_METADATA]:
            item.setMetadataValue(FILE_ADD_AS_METADATA_FIELD,filehandler)
            return[item]
        else:
            newFileItem = BaseItem(None)
            newFileItem.setParent(item)
            newFileItem.setValue(filehandler)
            return [newFileItem]

    def processList(self,items):
        result = []
        for index,item in enumerate(items):
            if FILE_NAME_NUMBER in self.__config and self.__config[FILE_NAME_NUMBER]:
                processedItem = self.process(item,str(index))
            else:
                processedItem = self.process(item,None)

            if processedItem is not None:
                result = result + processedItem
            else:
                logger.warning("Processed item %s returns [] empty array",str(item))

        return result
    """ Item subfolder based on metadata """
    def __getFileSubfolder(self,item):
        if not item.getMetadataValue(FILE_SUBFOLDER_METADATA) is None:
            return item.getMetadataValue(FILE_SUBFOLDER_METADATA)+"/"
        else:
            logger.debug("No subfolder configured")
            return ""



FILE_NAME = "fileprocessor_filename"
FILE_OP = "fileprocessor_operation"
FILE_OP_STORE = "fileprocessor_operation_store"
FILE_OP_RETRIEVE = "fileprocessor_operation_retrieve"
FILE_METADATA_FILENAME = "fileprocessor_metadata_filename"
""" Fileprocessor
    * OP = STORE : stores all item values into the configured file
    * OP = RETRIEVE : retrieves all item values into new item objects from the configured file
"""
class FileProcessor(AbstractFileProcessor):

    __config = {}

    __filehandler = None

    def __init__(self,config):

        self.__config = config


    def process(self,item):

        result = []
        if self.__config[FILE_OP]==FILE_OP_STORE:
            # Write item value and newline, adds metadata filename and returns item
            self.__filehandler.write(item.getValue()+"\n")
            item.setMetadataValue(FILE_METADATA_FILENAME,self.__config[FILE_NAME])
            result = [item]
        elif self.__config[FILE_OP]==FILE_OP_RETRIEVE:
            # Open the file, strip lines and generate new items
            lines = [line.strip() for line in open(self.__config[FILE_NAME],"r")]
            for l in lines:
                item = BaseItem({"parent",item})
                item.setValue(l)
                result.append(item)
            pass
        else:
            raise "Unknown operation"

        return result


    def processList(self,items):

        result = []
        if self.__config[FILE_OP]==FILE_OP_STORE:
            #Open file and process all items
            filename = self.__config[FILE_NAME]
            if FILE_ADD_DATE in self.__config and self.__config[FILE_ADD_DATE]:
                if FILE_ADD_DATE_PREV_EXT not in self.__config:
                    filename = filename + self.getDateForFilename()
                else:
                    # Issue #44
                    filename = self.getFilenameWithDateTimePrevExtension(filename)

            self.__filehandler = open(filename,"a")
            for item in items:
                result.extend(self.process(item))
            self.__filehandler.close()

        elif self.__config[FILE_OP]==FILE_OP_RETRIEVE:
            for item in items:
                result = result + self.process(item)
            pass
        else:
            raise "Unknown operation"

        return result;



REDIS_DATASOURCE = "redis_datasource"
#REDIS_OP = "redisprocessor_operation"
#REDIS_OP_STORE = "redisprocessor_operation_store"
#REDIS_OP_RETRIEVE = "redisprocessor_operation_retrieve"

REDIS_METADATA = "redis_metadata"
class RedisStoreProcessor(AbstractListProcessor):

    """ REDIS Processor : Using redis as storage
    This processor stores all ITEM VALUES into REDIS (defined in datasource)
     """

    __datasource = None

    def __init__(self,config):
        if self.validateConfig(config):
            self.__datasource = config[REDIS_DATASOURCE]


    def process(self, item):
        self.__datasource.store(item)
        item.setMetadataValue(REDIS_METADATA,"stored")


    def validateConfig(self, config):

        if AbstractListProcessor.validateConfig(self, config):
            # Validate processor config

            # Contains datasource
            return ContainsKeyAndInstanceConfigValidator({REDIS_DATASOURCE:type(RedisDataSource)})


class RedisGetProcessor(AbstractListProcessor):
    """ REDIS Processor : Using redis as origin for values
        Items passed are ignored : just obtain all redis elements
    """

    __datasource = None

    def __init__(self,config):
        if self.validateConfig(config):
            self.__datasource = config[REDIS_DATASOURCE]


    def process(self, item):

        return self.__obtainAllRedisElements()

    def processList(self, items):

        return self.__obtainAllRedisElements()

    def __obtainAllRedisElements(self):

        return self.__datasource.all()


    def validateConfig(self, config):

        if AbstractListProcessor.validateConfig(self, config):
            # Validate processor config

            # Contains datasource
            return ContainsKeyAndInstanceConfigValidator({REDIS_DATASOURCE:type(RedisDataSource)})







