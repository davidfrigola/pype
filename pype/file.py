from core import *
import urllib2

FILE_FOLDER = "filefolder"

# Flag FILE_ADD_AS_METADATA: if true, adds to metadata the file
# if false, returns the file
FILE_ADD_AS_METADATA = "addasmetadata"
FILE_ADD_AS_METADATA_FIELD = "file"


""" Downloads a file from a url """
class FileDownloader(AbstractListProcessor):

    __config = {}

    def __init__(self,config):

        self.__config = config;
        # Validate folder
        if not FILE_FOLDER in config:
            raise "You must specify a file folder"
        if not FILE_ADD_AS_METADATA in config:
            raise "You must specify the metadata FLAG"

    def process(self,item):
        file = None # TODO download file
        downloadFileHandler = urllib2.urlopen(item.getValue())
        file_name = item.getValue().split('/')[-1]
        file = open(self.__config[FILE_FOLDER] + file_name,'wb')
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
