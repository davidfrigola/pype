from pype.core import *
from pype.file import *
from pype.extra_processor import *

items = []
for i in range(1,20):
    items = items + [BaseItem(None,"item"+str(i))]

filename="./test_fileprocessor.txt"
writeprocessor = FileProcessor({FILE_NAME:filename,FILE_OP:FILE_OP_STORE})

for i in range(1,2):
    writeprocessor.processList(items)

readprocessor = FileProcessor({FILE_NAME:filename,FILE_OP:FILE_OP_RETRIEVE})

result = readprocessor.processList([BaseItem(None,filename)])

#output results
print "Showin readed items -as strings- from file"
loggerprocessor = LogItemsProcessor(None)
loggerprocessor.processList(result)

print "File " + filename + " will be removed now"
#Delete file
import os
os.remove(filename)