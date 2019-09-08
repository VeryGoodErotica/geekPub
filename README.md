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

At least one of the scripts *requires* Python 3.6 and the other may as well.
On older UNIX systems you may need to install Python 3.6. For well-maintained
distributions this is usually easy, e.g. on CentOS 7 with EPEL:

    yum install python36 python36-pip python36-pytz

In those cases, you need to change the shebang from

    #!/usr/bin/env python

to

    #!/usr/bin/env python36

With the exception of enterprise (LTS) distributions, I believe most Linux
distributions at this point already ship with Python 3.6 or newer and you
do not have to do anything (except *maybe* install the pytz package) for these
scripts to work.

I recommend putting the python scripts into `~/bin/` or if they need to be
made available in multiple user accounts, into `/usr/local/bin`

Be shure to set the execution bit on them (e.g. `chmod +x ~/bin/*.py`)

I would appreciate it if a MacOS user (or even a Windows user) would send me
a README with Python 3.6 install instructions for those operating systems, I
do not have regular access to them.

I know MacOS already has Python but last time I had access to MacOS it was a
really outdated version and I had to install a newer one, I believe using a
program called `homebrew` but I can not recall.

For the `bash` shell script(s) they are not intended to be installed in a
directory in your path but are intended to be skeletons you modify as needed to
automate your workflow. For example, they assume your content directory is
called `OEBPS` and that your OPF file is called `content.opf` but the ePub
specification does not make such assertions.


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
confidence the same UUID is not already in use elsewhere.

If and when you do decide to get an actual ISBN, you can change your Unique
Identifier to that ISBN in the future, but note that doing so will mean that
any obfuscated resources need to be re-obfuscated from their original source,
as the cryptography key used to obfuscate the resources is generated from the
Unique Identifier.

This script will exit if it detects the `content.opf` file already has a
Unique Identifier set up.

This script takes a single argument: The path to your `content.opf` file.


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


mkepub.sh
---------

This is an example shell script for creating an ePub archive from the UNIX
command line. You will need to modify it for your own use.

The concept, it makes it easy to pull your ePub sources from a `git` or other
revision control system and create the archive without needing fancy GUI tools.

The example shell script makes use of the `updateTimestamp.py` script to update
the modification timestamp before it creates the archive.
