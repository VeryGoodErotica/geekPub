Font Subsetting
===============

This directory contains only text files with Unicode ranges that I use in
conjunction with `pyftsubset` from [fonttools](https://github.com/fonttools/fonttools)
to subset large fonts into smaller fonts that only contain the glyphs I am
likely to need.

See my (coming) book for more information.


WesternLatinRange.txt
---------------------

All the Unicode glyphs associated with Latin-1 (ISO-8859-1), Latin-9 (ISO-8859-15)
and Windows-1252 plus two additional glyphs. Generally reduces a TTF font file
to about 40-45 kB in size.

    unicode-range: U+0020-007E,U+00A0-00FF,U+0152-0153,U+0160-0161,U+0178,U+017D-017E,U+0192,U+02C6,U+02DC,U+2013-2014,U+2018-201A,U+201C-201E,U+2020-2022,U+2026,U+2030,U+2039-203A,U+20AC,U+2116-2117,U+2122;


OrnamentalRange.txt
-------------------

All the printable 7-bit ASCII plus the ornamental/dingbat glyphs from the
Unicode 'Miscellaneous Technical' block (`U+2300-23FF`), 'Miscellaneous Symbols'
block (`U+2600-26FF`), and 'Dingbats' Block (`U+2700-27BF`). With the DejaVu
Sans fonts, this results in a TTF subset about 105 kB in size, but the size
will vary depending upon how many glyphs from that range your original font
actually has support for.

    unicode-range: U+0020-007E,U+2300-23FF,U2600-27BF;
