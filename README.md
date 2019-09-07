geekPub Shell Utilities
=======================

These are shell utilities intended to accompany my coming (still barely started)
ePub book on ePub.

The Python utilities are tested with Python 3.6 and may not work with other
versions, I do not know.

All scripts here are MIT license. See the LICENSE file.


updateTimestamp.py
------------------

When any change is made to your ePub, the `<meta property="dcterms:modified"></meta>`
node is suppose to updated to reflect the modification time.

This script does that, you can call if from your script that generates the ePub
before packing it into a zip archive and know that modification timestamp is
proper.

This script will remove any existing `<meta property="dcterms:modified"></meta>`
tags within `<metadata/>` and then create one using the current timestamp.

Note that the python minidom module this script uses re-orders attributes in
other nodes as well, I consider that to be a very nasty bug in minidom even
though technically it does not matter. Workarounds to this bug if it bothers
you are discussed at:

  https://stackoverflow.com/questions/662624/preserve-order-of-attributes-when-modifying-with-minidom

This script takes a single argument: the path to your content.opf file.


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
will create a *new* file name with a different name, and it will exit if a file
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

### obfuscateResource.py WARNING

According to the specification, there are four Unicode codepoints that are to
be removed from the Unique ID before it is hashed to create the obfuscation
key.

I do not yet do this, I mostly code in PHP so I need to look up how to do regex
in python based on Unicode codepoints. However, it is unlikely the codepoints
will exist in your Unique ID.

### obfuscateResource.py WARNING TWO

This has not been fully tested. I have not (yet) created an ePub with
obfuscated resources and tested that it actually works on a variety of
different readers. That will be done shortly.
