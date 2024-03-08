Example on how to use p1689 with gcc and ninja
==============================================

This shows how to use gcc with its support for p1689 to export dependency
information and how to use that in a ninja file to provide dynamic dependency
information to build C++ modules.

As of writing GCC does not support exporting dependency information for header
units (so no `import <iostream>` for example). Also this example hardcodes file
and directory names. While it does generate a ninja file, you can't modify which
builddir is used, it globs all C++ files for one executable and it hardcodes a
GCM folder. Running this outside the project directory may cause destruction.
The parsing of the p1689 files is also really rudimentary and paths are built
using string concatenation. **You have been warned.**

Currently this requires at least gcc 14 and is hardcoded to use `g++-14`, you
can edit that in `./modulebuild.py` though.

How to use
----------

Generate a builddir and build.ninja:

```sh
./modulebuild.py
```

Compile:

```sh
ninja -C builddir
```

You can also modify the module names and it should automatically rebuild, what
is necessary.

Notes
-----

At first I tried to use one dyndep file for each object file. However that lead
to issues, when you only did a partial rebuild. Ninja won't load dyndep files
for all the object files you depend on and if your module changed, it might not
know how to build the gcm file. I solved this by combining all the dyndep files
into one and depend on that dyndep file in the targets for each object. This
synchronization point seems to be necessary anyway however, since otherwise
Ninja would possibly not have build the dyndep file for some module.

Apart from the modulebuild script, 2 other scripts are necessary. One, as
explained above, to do basically `cat $in > $out` for all the dyndep files. And
another one to translate the output format from gcc into a dyndep file. These 2
scripts could be combined, but I haven't bothered yet.
