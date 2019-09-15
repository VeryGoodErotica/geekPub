geekPub Shell Utilities
=======================

These are shell utilities intended to accompany my coming (still barely started)
ePub book on ePub.

The Python utilities here are tested with Python 3.6 and may not work with older
versions.

The python scripts that manipulate XML files use the `minidom` library to do
so. That library does something I (and many others) am not too fond of, it
reorders all attributes in a node to alphabetical order.

Workarounds for this behavior can be found at

https://stackoverflow.com/questions/662624/preserve-order-of-attributes-when-modifying-with-minidom

However, all of them were beyond the scope of this project. I choose to just
live with it, but feel free to implement one of those solutions if you want
to.

All scripts here are MIT license. See the LICENSE file.


INSTALLATION
------------

At least one of the scripts *requires* Python 3.6 and the others may as well.
On older UNIX systems you may need to install Python 3.6. For well-maintained
distributions this is usually easy, e.g. on CentOS 7 with EPEL:

    yum install python36 python36-pip python36-pytz

In those cases, you need to change the shebang from

    #!/usr/bin/env python

to something like (depending on your system)

    #!/usr/bin/env python36

With the exception of enterprise (LTS) distributions, I believe most Linux
distributions at this point already ship with Python 3.6 or newer and you
do not have to do anything (except *maybe* install the pytz package) for these
scripts to work.

I recommend putting the python scripts into `~/bin/` or if they need to be
made available in multiple user accounts, into `/usr/local/bin/`

Be sure to set the execution bit on them (e.g. `chmod +x ~/bin/*.py`)

I would appreciate it if a MacOS user (or even a Windows user) would send me
a README with Python 3.6 install instructions for those operating systems, I
do not have regular access to them.

I know MacOS already has Python but last time I had access to MacOS it was a
really outdated version and I had to install a newer one, I believe using a
program called `homebrew` but I can not recall. It is quite possible there are
official packages distributed by the Python maintainers for MacOS as well.

For the `bash` shell script(s) they are not intended to be installed in a
directory in your path but are intended to be skeletons you modify as needed to
automate your workflow. For example, they assume your content directory is
called `EPUB` and that your OPF file is called `content.opf` but the ePub
specification does not make such assertions. Using `OEBPS` for the content
directory is also extremely common.


createSkeletonEpub.py
---------------------

This script can be used to create a new projet. It creates the `META-INF`
directory and the `container.xml` file along with the content directory and the
OPF file. The script can be run without arguments in which case default values
are used, or you can use switches to override the default values:

    usage: createSkeletonEpub.py [-h] [-t TITLE] [-d DESCRIPTION] [-g GENRE]
                                 [-a AUTHOR] [-p PUBLISHER] [-e PUBLICATIONDATE]
                                 [-x XMLLANG] [-l BOOKLANG] [-D OEBPS] [-f OPF]
    
    Setup an initial ePub 3 container structure. All arguments are optional.
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TITLE, --title TITLE
                            The title of the book
      -d DESCRIPTION, --description DESCRIPTION
                            A short description of the book
      -g GENRE, --genre GENRE
                            The genre the book fits into
      -a AUTHOR, --author AUTHOR
                            The author of the book
      -p PUBLISHER, --publisher PUBLISHER
                            The book publisher
      -e PUBLICATIONDATE, --pubdate PUBLICATIONDATE
                            Publication date
      -x XMLLANG, --xmllang XMLLANG
                            BCP 47 language string for the Package Document File
                            (OPF)
      -l BOOKLANG, --lang BOOKLANG
                            BCP 47 language string for the language of the book
      -D OEBPS, --contentdir OEBPS
                            Content directory for your ePub files
      -f OPF, --opffile OPF
                            File name for the Package Document File (OPF)

The default for the publication data metadata is six weeks in the future and
will almost certainly need editing within the Package Document File but since it
is requires metadata, I had to use something. If you know the planned
publication date when running the script, the `-e` or `--pubdate` switches will
override that guess and accepts string dates, such as `"5 dec 2020"` etc.

The default values when used without switches are at the top of the
`createSkeletonEpub.py` file just under all the `import whatever` declarations
if you want to customize the defaults for your environment.

The script uses a coulple python dependencies some systems may not have:

1. `language_tags` - used to validate BCP 47 language tags.
2. `dateparser` - used to normalize date strings.

Both are available via `pip` if your operating system vendor does not have
packages for them.

The `createSkeletonEpub.py` will create a unique identifier using a UUID but you
can use the `addIsbnNumber.py` to use an ISBN number instead if you have (or
get) one.


generateUniqueIdentifier.py
---------------------------

Every ePub has to have a Unique Identifier defined in the `content.opf` file.
When your publication has an ISBN number, that is *usually* what is used. When
you do not have one, you can use a [UUID](https://tools.ietf.org/html/rfc4122)
instead.

This script generates a UUID and creates the necessary nodes and attributes in
your `content.opf` file to use the UUID as the unique identifier for your ePub.

UUID has no cost associated with it, nor does it have a central registry. It is
simply a hex encoded 128-bit random number with some dashes inserted. As long
as your operating system pRNG is not broken, you can have *extremely* high
confidence the same UUID is not already in use elsewhere, there are literally
3.4 X 10^38 possible UUID value, duplicates when generated via a quality pRNG
will not happen.

If and when you do decide to get an actual ISBN, you can change your Unique
Identifier to that ISBN in the future, but note that doing so will mean that
any obfuscated resources need to be re-obfuscated from their original source,
as the cryptography key used to obfuscate the resources is generated from the
Unique Identifier.

This script will exit if it detects the `content.opf` file already has a
Unique Identifier set up.

This script takes a single argument: The path to your `content.opf` file.


addIsbnNumber.py
----------------

If you have an ISBN number for your publication, this script will add it to
your `content.opf` file as the Unique Identifier. If fed a 10 digit ISBN it
will first be converted to a 13 digit ISBN, though that should not be needed
since 10 digit ISBN are not issued anymore and digital editions are *suppose*
to have a different ISBN than previous editions.

The script will exit if fed an ISBN number it detects as invalid. The script
will exit if it detects the ePub already has a Unique Identifuer *unless* the
`id` attribute for that unique identifier is `prng-uuid` which is the default
`id` attribute set by the `generateUniqueIdentifier.py` script. This is done to
prevent accidental alteration of the Unique Identifier.

If you intend to alter the Unique Identifier, manually edit your `content.opf`
file and remove the `unique-identifier` attribute from the root `package` node.

This script will not remove any existing `dc:identifier` nodes, and it is okay
to have as many of those as you need, but only one can have an `id` attribute
that corresponds with the `package` `unique-identifier` attribute.

When there are existing `dc:identifier` nodes, this script will insert the
`dc:identifier` for the ISBN number before the other(s). This is because some
ePub readers are not fully ePub 3 compliant and expect the first to be the ISBN
number.

The first argument to the script is the path to your `content.opf` file and the
second argument is the ISBN number (with or without hyphens).


updateTimestamp.py
------------------

When any change is made to your ePub, the `<meta property="dcterms:modified"></meta>`
node is suppose to updated to reflect the modification time.

This script does that, you can call if from your script that generates the ePub
before packing it into a zip archive and know that modification timestamp is
proper.

This script will remove any existing `<meta property="dcterms:modified"></meta>`
tags within `<metadata/>` and then create one using the current timestamp.

This script takes a single argument: The path to your `content.opf` file.


obfuscateResource.py
--------------------

Some third party resources have a license that *requires* you obfuscate the
resource before embedding it in a product (such as an eBook) that you
distribute.

For this reason, the ePub specification documents an obfuscation method that
can be used at

  https://www.w3.org/publishing/epub3/epub-ocf.html#sec-resource-obfuscation

Neither I nor the W3C can give advice on whether or not the algorithm there
satisfies license requirements, but that method is the only obfuscation method
that is part of the ePub specification and thus likely to be supported by the
majority of ePub software.

This script implements that algorithm to obfuscate a resource.

Please note that this script does *not* modify or create the `encryption.xml`
file that obfuscated resources must be described in. The script does not care
what the path of the resource within your ePub archive will be, so it can not
modify that file.

Please note that running the ePub obfuscation algorithm on an obfuscated file
will deobfuscate the file.

This script will *not* modify the file to be obfuscated on the filesystem. It
will create a *new* file with a different file name, and it will exit if a file
of that name already exists.

If `filename.ext` is the file to be obfuscated, `filename-obf.ext` will be the
obfuscated file that is created.

On the other hand if `filename-obf.ext` is the file to be obfuscated, then
`filename.ext` will be the obfuscated file that is created (which results in an
un-obfuscated file if `filename-obf.ext` is an obfuscated file and the __same__
obfuscation key is used)

In either case (with or without `-obf` at the end of the filename before the
file extension) the output file will *not* be created if a file of that name
already exists.

The first argument is the path to the OPF file. This is necessary to determine
the obfuscation key.

The second argument is the path to the resource to be obfuscated (or
de-obfuscated if it was already obfuscated with the same key)


iBooksFontsEmbed.py
-------------------

By default, iBooks on iOS will use embedded fonts everywhere *except* for text
that is a child of a paragraph node. Usually this works out okay, but there will
be cases that make you want to scream.

The workaround is a non-standard file called `com.apple.ibooks.display-options.xml`
in your `META-INF` directory with an option telling iBooks to use your specified
fonts everywhere.

This script creates that file.

This is just version 1 of the script. There may be other iBooks specific options
that can be set in that file, I do not know. If there are, then a *future*
version will parse the file first if it exists and add the option if it is not
already set. But this version creates the file if it does not exist and exits if
it already exists.

The script takes a single argument: The path to the `META-INF` directory.


epubcheck.sh
------------

This is a bash wrapper script for the [epubcheck](https://github.com/w3c/epubcheck)
utility.

Install it in `~/bin/` and make it executable:

    cp epubcheck.sh ~/bin/ && chmod +x ~/bin/epubcheck.sh

You will want to change the `EPUBCHECK` variable to point to the location where
you unpacked the download from their github project.

If you have more than one version a `java` installed, you *may* need to change
the `OPERATION` variable to specify the full path to the `java` executable you
want used.

If there is an option to the `epubcheck.jar` you *always* want used, you can
optionally change the `OPTIONS` variable to specify that option after the `$@`
but make sure to put it *after* the `$@` and that there is a space between
them.


mkepub.sh
---------

This is an example shell script for creating an ePub archive from the UNIX
command line. You will need to modify it for your own use.

The concept, it makes it easy to pull your ePub sources from a `git` or other
revision control system and create the archive without needing fancy GUI tools.

The example shell script makes use of the `updateTimestamp.py` script to update
the modification timestamp before it creates the archive.

The example shell script makes use of the `epubcheck.sh` shell script to check
the result for validation errors.
