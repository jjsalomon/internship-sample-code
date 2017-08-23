# -*- coding: utf-8 -*-
# install hachoir
# pip install -U hachoir3
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import os

file = os.getcwd() +'\output.avi'
parser = createParser(file)
metadata = extractMetadata(parser)
charlist = []
stringlist = []
for line in metadata.exportPlaintext():
    charlist += line
    
stringlist = ''.join(charlist)
Duration = int(stringlist[19:21])

