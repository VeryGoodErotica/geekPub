#!/usr/bin/env python
import sys
import os
import pathlib
from xml.dom import minidom

def showUsage():
    print ("Usage: " + sys.argv[0] + " path/to/META-INF")
    sys.exit(1)

def createMetaFile(xml):
    mydom = minidom.parseString('<display_options/>')
    root = mydom.getElementsByTagName('display_options')[0]
    platform = mydom.createElement('platform')
    platform.setAttribute('name','*')
    text = mydom.createTextNode('true')
    option = mydom.createElement('option')
    option.appendChild(text)
    option.setAttribute('name','specified-fonts')
    platform.appendChild(option)
    root.appendChild(platform)
    string = mydom.toprettyxml(indent="  ",newl="\n",encoding="UTF-8").decode()
    string = string.replace("?>", " standalone=\"yes\"?>")
    string = '\n'.join([x for x in string.split("\n") if x.strip()!=''])
    fh = open(xml, "w")
    fh.write(string)
    fh.close()
    print ("META-INF file for iBooks fonts created.")

def main():
    if len(sys.argv) != 2:
        showUsage()
    metainf = pathlib.Path(sys.argv[1])
    if not metainf.exists():
        showUsage()
    if not metainf.is_dir():
        showUsage()
    if not metainf.name == 'META-INF':
        showUsage()
    xmlpath = metainf.joinpath('com.apple.ibooks.display-options.xml')
    if xmlpath.exists():
        print ("File already exists. Exiting.")
        sys.exit(1)
    xml = xmlpath.resolve()
    createMetaFile(xml)

if __name__ == "__main__":
    main()
