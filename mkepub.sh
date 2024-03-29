#!/bin/bash

rm -f yourBook.epub

[ ! -d EPUB ] && exit 1

cd EPUB
~/bin/updateTimestamp.py content.opf

find . -print |grep "~$" |while read file; do
  rm -f ${file}
done
find . -print |grep "\.swp$" |while read file; do
  rm -f ${file}
done
cd ..

if [ ! -d META-INF ]; then
mkdir META-INF
cat <<EOF > META-INF/container.xml
<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml" />
  </rootfiles>
</container>
EOF
fi

echo -n application/epub+zip >mimetype

zip -r -X youBook.zip mimetype META-INF EPUB
mv yourBook.zip yourBook.epub

~/bin/epubcheck.sh yourBook.epub

# run accessibility check if available
if hash ace 2>/dev/null; then
  ace -f -s -o AceReport yourBook.epub
  echo "Accessibility report written to AceReport directory"
fi
