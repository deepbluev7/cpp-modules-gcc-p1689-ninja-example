#!/usr/bin/python

import sys

outfile = sys.argv[1]
with open(outfile, 'w') as out:
    out.write('ninja_dyndep_version = 1\n')

    for f in sys.argv[2:]:
        print(f"Combining {f}")
        with open(f, mode='r') as f:
            out.write(f.read())

