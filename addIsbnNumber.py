#!/usr/bin/env python3
import sys
import os
import pathlib
from xml.dom import minidom

def showUsage():
    print ("Usage: " + sys.argv[0] + " path/to/content.opf yourISBNnumber")
    sys.exit(1)

def checkDigit(isbn):
    length = len(isbn)
    if not length == 12:
        print ("This should not have happened. Bug in program.")
        sys.exit(1)
    try:
        foo=int(isbn)
    except:
        print ("This should not have happened. Bug in program.")
        sys.exit(1)
    s = int(isbn[0:1]) + (3 * int(isbn[1:2])) + int(isbn[2:3]) + (3 * int(isbn[3:4])) + int(isbn[4:5]) + (3 * int(isbn[5:6])) + int(isbn[6:7]) + (3 * int(isbn[7:8])) + int(isbn[8:9]) + (3 * int(isbn[9:10])) + int(isbn[10:11]) + (3 * int(isbn[11:12]))
    modulo = s % 10
    return str((10 - modulo) % 10)

def cleanNumber(isbn):
    isbn = isbn.translate({32: None}) # remove space
    isbn = isbn.translate({45: None}) # remove dash
    length = len(isbn)
    if length == 9:
        # 10 digit w/o check
        isbn = '978' + isbn
    elif length == 10:
        # 10 digit w/ check, validate
        check = isbn[-1:].upper()
        isbn = isbn[0:9]
        try:
            foo=int(isbn)
        except:
            print ("Invalid ISBN")
            sys.exit(1)
        s = (10 * int(isbn[0:1])) + (9 * int(isbn[1:2])) + (8 * int(isbn[2:3])) + (7 * int(isbn[3:4])) + (6 * int(isbn[4:5])) + (5 * int(isbn[5:6])) + (4 * int(isbn[6:7])) + (3 * int(isbn[7:8])) + (2 * int(isbn[8:9]))
        modulo = s % 11
        n = ((11 - modulo) % 11)
        if n == 10:
            checkd = 'X'
        else:
            checkd = str(n)
        if check == checkd:
            isbn = '978' + isbn
        else:
            print ("ten digit ISBN failed check digit test. Invalid ISBN.")
            sys.exit(1)
    try:
        foo=int(isbn)
    except:
        print ("Invalid ISBN")
        sys.exit(1)
    length = len(isbn)
    if length == 12:
        return (isbn + checkDigit(isbn))
    elif length == 13:
        check = isbn[-1:]
        isbn = isbn[0:12]
        checkd = checkDigit(isbn)
        if check == checkd:
            return (isbn + check)
        else:
            print ("thirteen digit ISBN failed check digit test. Invalid ISBN.")
            sys.exit(1)
    print ("Invalid ISBN")
    sys.exit(1)

def insertIsbn(xml, isbn):
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
        if uid == 'prng-uuid':
            uid = 'isbn-13'
            root.setAttribute("unique-identifier", uid)
    else:
        uid = 'isbn-13'
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
    TextISBN = mydom.createTextNode(isbn)
    node = mydom.createElement("dc:identifier")
    node.appendChild(TextISBN)
    node.setAttribute("id",uid)
    text = mydom.createTextNode("isbn")
    meta = mydom.createElement("meta")
    meta.appendChild(text)
    meta.setAttribute("refines", "#" + uid)
    # some readers are not fully compliant with ePub3 and need the ISBN to be before other dc:identifier nodes
    if len(nodelist) == 0:
        metadata.appendChild(node)
        metadata.appendChild(meta)
    else:
        metadata.insertBefore(node,nodelist[0])
        metadata.insertBefore(meta,nodelist[0])
    string = mydom.toprettyxml(indent="  ",newl="\n",encoding="UTF-8").decode()
    string = '\n'.join([x for x in string.split("\n") if x.strip()!=''])
    fh = open(xml, "w")
    fh.write(string)
    fh.close()
    print ("ISBN number added as Unique Identifier.")

def main():
    if len(sys.argv) != 3:
        showUsage()
    opf = pathlib.Path(sys.argv[1])
    if not opf.exists():
        showUsage()
    isbn = cleanNumber(sys.argv[2])
    insertIsbn(sys.argv[1], isbn)

if __name__ == "__main__":
    main()
