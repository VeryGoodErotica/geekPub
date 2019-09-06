#!/usr/bin/env python
import sys
import os
import pathlib
from xml.dom import minidom
import hashlib

def getObfuscationKey(xml):
    opf = pathlib.Path(xml)
    if not opf.exists ():
        print ("OPF File Not Found")
        sys.exit(1)
    mydom = minidom.parse(xml)
    pubid = mydom.getElementsByTagName('package')[0].attributes['unique-identifier'].value
    nodelist = mydom.getElementsByTagName('dc:identifier')
    for node in nodelist:
        if node.hasAttribute('id') and node.getAttribute('id') == pubid:
            uid = node.firstChild.nodeValue
            # TODO - remove U+0020, U+0009, U+000D, U+000A
            return hashlib.sha1(uid.encode('utf-8'))
    print ("Could not find Unique ID in OPF")
    sys.exit(1)

def getOutputFile(input):
    orig = pathlib.Path(input)
    if not orig.exists ():
        print ("File to obfuscate (or de-obfuscate) does not exist.")
        sys.exit(1)
    filename, extension = os.path.splitext(input)
    if len(filename) > 4:
        # See if already obfuscated
        end = filename[-4:]
        if end == '-obf':
            newfilename = filename[:-4] + extension
        else:
            newfilename = filename + '-obf' + extension
    else:
        newfilename = filename + '-obf' + extension
    new = pathlib.Path(newfilename)
    if new.exists ():
        print ("Target output file " + newfilename + " already exists.")
        sys.exit(1)
    return newfilename

key = getObfuscationKey(sys.argv[1])
newfile = getOutputFile(sys.argv[2])

print ("Program not yet finished.") 
