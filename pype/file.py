from core import *
import os
import urllib2
import logging

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


""" Downloads a file from a url """
class FileDownloader(AbstractListProcessor):

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

    def process(self,item):
        file = None
        downloadFileHandler = urllib2.urlopen(item.getValue())
        file_name = item.getValue().split('/')[-1]
        directory = self.__config[FILE_FOLDER] + self.__getFileSubfolder(item)

        if not os.path.exists(directory):
            logger.info("Creating folder "+directory)
            os.makedirs(directory)

        log.info("Downloading file to "+directory+file_name)

        file = open(directory + file_name,'wb')
        file.write(downloadFileHandler.read())
        file.close()
        # Return result
        if self.__config[FILE_ADD_AS_METADATA]:
            item.setMetadataValue(FILE_ADD_AS_METADATA_FIELD,file)
            return[item]
        else:
            newFileItem = BaseItem(None)
            newFileItem.setParent(item)
            newFileItem.setValue(file)
            return [newFileItem]

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
""" Fileprocessor
    * OP = STORE : stores all item values into the configured file
    * OP = RETRIEVE : retrieves all item values into new item objects from the configured file
"""
class FileProcessor(AbstractListProcessor):

    __config = {}

    __filehandler = None

    def __init__(self,config):

        self.__config = config


    def process(self,item):

        result = []
        if self.__config[FILE_OP]==FILE_OP_STORE:
            pass
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
            ##TODO open file an store locally (class variable)
            for item in items:
                result = result + process(self,item)


        elif self.__config[FILE_OP]==FILE_OP_RETRIEVE:
            for item in items:
               result = result + process(self,item)
            pass
        else:
            raise "Unknown operation"

        return result;
