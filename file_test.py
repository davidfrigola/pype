from pype.storage import *

item = BaseItem(None)
item.setValue("https://code.google.com/intl/es/images/gd-logo.png")
item.setMetadataValue(FILE_SUBFOLDER_METADATA,"subfolder")
downloader = FileDownloader({FILE_FOLDER:"C:/tmp/",FILE_ADD_AS_METADATA:False})

result = downloader.process(item)

print str(result)

filename = "./test.txt"

fileprocessor = FileProcessor({FILE_NAME:filename,FILE_OP:FILE_OP_STORE})

print fileprocessor.getDateForFilename()

exit

item2 = BaseItem(None)
item2.setValue("value2")

result = fileprocessor.processList([item,item2])

fileprocessor = FileProcessor({FILE_NAME:filename,FILE_OP:FILE_OP_RETRIEVE})
fileItem = BaseItem(None)
fileItem.setValue(filename)

result = fileprocessor.process(fileItem)
print "Values retrieved from file " + filename
for e in result:
    print str(e.getValue())+"-"+str(e.getHash())