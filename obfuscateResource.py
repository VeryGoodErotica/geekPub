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
            return hashlib.sha1(uid.encode('utf-8')).digest()
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

def obfuscateFile(key,original,obfuscated):
    if len(key) != 20:
        print("Key must be 20 bytes.")
        sys.exit(1)
    kbprocessed = 0
    with open(original,'rb') as f1,open(obfuscated,'wb') as f2:
        while True:
            buf=f1.read(1024)
            if buf:
                ba = bytearray()
                n = 0
                for byte in buf:
                    if kbprocessed == 0:
                        m = (n % 20)
                        keybyte = key[m:(m+1)]
                        #The XOR
                        byte = byte ^ ord(keybyte)
                    ba.append(byte)
                    n += 1
                n=f2.write(ba)
                kbprocessed = 1 #just can't be 0
            else:
                break
    print("Obfuscated (or de-obfuscated) file written to " + obfuscated)

def main():
    if len(sys.argv) != 3:
        showUsage()
    key = getObfuscationKey(sys.argv[1])
    newfile = getOutputFile(sys.argv[2])
    print ("Program not yet tested.")
    obfuscateFile(key,sys.argv[2],newfile)

if __name__ == "__main__":
    main() 
