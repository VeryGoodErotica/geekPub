#!/usr/bin/env python
import sys
import os
import pathlib
import secrets
from xml.dom import minidom

def showUsage():
    print ("Usage: " + sys.argv[0] + " path/to/contents.opf")
    sys.exit(1)

def generateIdentifier():
    rnd = secrets.token_hex(16)
    return (rnd[0:8] + "-" + rnd[8:12] + "-" + rnd[12:16] + "-" + rnd[16:20] + "-" + rnd[20:])

def createUniqueID(xml):
    try:
        mydom = minidom.parse(xml)
    except:
        print (xml + " is not a valid XML file.")
        sys.exit(1)
    try:
        root = mydom.getElementsByTagName("package")[0]
    except:
        print ("Could not find root package node.")
        sys.exit(1)
    if root.hasAttribute("unique-identifier"):
        uid = root.getAttribute("unique-identifier")
    else:
        uid = 'prng-uuid'
        root.setAttribute("unique-identifier", uid)
    try:
        metadata = root.getElementsByTagName("metadata")[0]
    except:
        print ("Could not find metadata node.");
        sys.exit(1)
    nodelist = metadata.getElementsByTagName("dc:identifier")
    for node in nodelist:
        if node.hasAttribute("id") and node.getAttribute("id") == uid:
            print ("A unique identifier already exists. Exiting.")
            sys.exit(1)
    uuid = mydom.createTextNode(generateIdentifier())
    node = mydom.createElement("dc:identifier")
    node.appendChild(uuid)
    node.setAttribute("id",uid)
    metadata.appendChild(node)
    text = mydom.createTextNode("uuid")
    node = mydom.createElement("meta")
    node.appendChild(text)
    node.setAttribute("property", "marc:scheme")
    node.setAttribute("refines", "#" + uid)
    metadata.appendChild(node)
    string = mydom.toprettyxml(indent="  ",newl="\n",encoding="UTF-8").decode()
    string = '\n'.join([x for x in string.split("\n") if x.strip()!=''])
    fh = open(xml, "w")
    fh.write(string)
    fh.close()

def main():
    if len(sys.argv) != 2:
        showUsage()
    opf = pathlib.Path(sys.argv[1])
    if not opf.exists():
        showUsage()
    createUniqueID(sys.argv[1])

if __name__ == "__main__":
    main()
