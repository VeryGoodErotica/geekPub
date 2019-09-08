Font Subsetting
===============

This directory contains only text files with Unicode ranges that I use in
conjunction with `pyftsubset` from [fonttools](https://github.com/fonttools/fonttools)
to subset large fonts into smaller fonts that only contain the glyphs I am
likely to need.

See my (coming) book for more information.

Using these files to subset a font is only intended as a method for reducing
the *size* of the font. It may not satisfy the font subsetting requirements
that some commercial fonts have since the result is still quite usable as a
font installed on a desktop system.


WesternLatinRange.txt
---------------------

All the Unicode glyphs associated with Latin-1 (ISO-8859-1), Latin-9 (ISO-8859-15)
and Windows-1252 plus two additional glyphs. Generally reduces a TTF font file
to about 40-45 kB in size.

    unicode-range: U+0020-007E,U+00A0-00FF,U+0152-0153,U+0160-0161,U+0178,U+017D-017E,U+0192,U+02C6,U+02DC,U+2013-2014,U+2018-201A,U+201C-201E,U+2020-2022,U+2026,U+2030,U+2039-203A,U+20AC,U+2116-2117,U+2122;


GreekRange.txt
--------------

All the printable 7-bit ASCII plus the Unicode 'Greek and Coptic' block
(`U+0370-03FF`) and the 'Greek Extended' block (`U+1F00-U+1FFF`) with additions
from ISO-8859-7, Windows-1253, ISO-5428, and 'Combining and letter-free
diacritics' referenced at Wikipedia that were not already part of the Unicode
blocks specific to Greek.

If you use Greek and there are any glyphs commonly used in Greek literature
that you notice are missing, *please* let me know so this subset can be updated
to include them.

The size of the result will vary depending as not all fonts that support Greek
also support Polytonic Greek, but for me they tended to be about 55-60 kB in
size.

    unicode-range: U+0020-007E,U+00A0,U+00A3-00A9,U+00AB-00B7,U+00BB-00BE,U+0192,U+02BC-02BD,U+02D8,U+0300-0301,U+0304,U+0306,U+0308,U+0313-0314,U+0342-0345,U+0370-03FF,U+1F00-1FFF,U+2013-2015,U+2018-201A,U+201C-201E,U+2020-2022,U+2026,U+2030,U+2039-203A,U+20AC,U+20AF,U+2122


OrnamentalRange.txt
-------------------

All the printable 7-bit ASCII plus the ornamental/dingbat glyphs from the
Unicode 'Miscellaneous Technical' block (`U+2300-23FF`), 'Miscellaneous Symbols'
block (`U+2600-26FF`), and 'Dingbats' Block (`U+2700-27BF`). With the DejaVu
Sans fonts, this results in a TTF subset about 105 kB in size, but the size
will vary depending upon how many glyphs from that range your original font
actually has support for.

    unicode-range: U+0020-007E,U+2300-23FF,U2600-27BF;
