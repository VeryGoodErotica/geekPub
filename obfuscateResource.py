#!/usr/bin/env python
import sys
import os
import pathlib
from xml.dom import minidom
import hashlib

def showUsage():
    print ("Usage: " + sys.argv[0] + " path/to/contents.opf path/to/resource.ext")
    sys.exit(1)

def getObfuscationKey(xml):
    opf = pathlib.Path(xml)
    if not opf.exists ():
        print ("OPF File Not Found")
        sys.exit(1)
    try:
        mydom = minidom.parse(xml)
    except:
        print (xml + " is not a valid XML file.")
        sys.exit(1)
    try:
        pubid = mydom.getElementsByTagName('package')[0].attributes['unique-identifier'].value
    except:
        print ("Could not read unique-identifier attribute.")
        sys.exit(1)
    nodelist = mydom.getElementsByTagName('dc:identifier')
    for node in nodelist:
        if node.hasAttribute('id') and node.getAttribute('id') == pubid:
            try:
                uid = node.firstChild.nodeValue
            except:
                print ("Unique Identifier has no value.")
                sys.exit(1)
            # TODO - remove U+0020, U+0009, U+000D, U+000A
            if len(uid) == 0:
                print ("Unique Identifier has no value.")
                sys.exit(1)
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

def main():
    if len(sys.argv) != 3:
        showUsage()
    key = getObfuscationKey(sys.argv[1])
    newfile = getOutputFile(sys.argv[2])
    print ("Program not yet finished.")

if __name__ == "__main__":
    main() 
