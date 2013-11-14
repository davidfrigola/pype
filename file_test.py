from pype.file import *

item = BaseItem(None)
item.setValue("https://code.google.com/intl/es/images/gd-logo.png")
item.setMetadataValue(FILE_SUBFOLDER_METADATA,"subfolder")
downloader = FileDownloader({FILE_FOLDER:"C:/tmp/",FILE_ADD_AS_METADATA:False})

result = downloader.process(item)

print str(result)