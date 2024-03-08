#!/usr/bin/python

import ninja_syntax as ninja
import json
import sys

depinfo=json.load(sys.stdin)

outfile = sys.argv[1]
gcmdir = sys.argv[2]

with open(outfile, 'w') as ninjafile:
    n = ninja.Writer(ninjafile)

    #n.variable('ninja_dyndep_version', '1')

    rules = depinfo['rules'][0]
    primaryout = rules['primary-output']
    moduledeps = []
    gcmfile = None

    if 'provides' in rules:
        provides = rules['provides']
        gcmfile = []
        for p in provides:
            if 'logical-name' in p:
                gcmfile = [gcmdir + '/' + p['logical-name'] + '.gcm']
    if 'requires' in rules:
        requires = rules['requires']
        for r in requires:
            if 'logical-name' in r:
                moduledeps = [gcmdir + '/' + r['logical-name'] + '.gcm']
    if not moduledeps:
        moduledeps = None

    n.build(outputs=primaryout, rule='dyndep', implicit_outputs=gcmfile, implicit=moduledeps)
    n.close()
