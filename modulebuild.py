#!/usr/bin/python

import ninja_syntax as ninja
import os
import glob

builddir = 'builddir'
ARGS = '-fdiagnostics-color=always -fmodules-ts -std=c++23 -Wall'

if not os.path.exists(builddir):
    os.makedirs(builddir)

with open(f'{builddir}/build.ninja', 'w') as ninjafile:
    n = ninja.Writer(ninjafile)
    n.comment('This is a test')
    n.newline()
    n.variable('cxx', 'g++-14')
    n.variable('gcmdir', os.path.abspath(f'{builddir}/gcms'))
    n.newline()
    # we specify the deps format also in the compile line to prevent gcc from adding it to the header dep file
    n.rule(name='cxx_compile', command="$cxx $ARGS -MD -MQ $out -MF $DEPFILE '-fmodule-mapper=|@g++-mapper-server -r$gcmdir' -fdeps-format=p1689r5 -o $out -c $in", description='Compiling c++ object $out', deps='gcc', depfile='$DEPFILE')
    n.rule(name='cxx_modulescan', command="$cxx $ARGS -E -MD -MQ $OBJECTOUT -MF $DEPFILE '-fmodule-mapper=|@g++-mapper-server -r$gcmdir' -fdeps-file=- -fdeps-format=p1689r5 -fdeps-target=$OBJECTOUT -c $in -o /dev/null | ../moduledepfilter.py $out $gcmdir", description='Detection c++ object $OBJECTOUT module dependencies to $out', deps='gcc', depfile='$DEPFILE')

    n.rule(name='cxx_link', command="$cxx $ARGS -o $out $in", description='Linking $out')
    n.rule(name='combine_module_deps', command="../combine_dyndeps.py $out $in", description='Combining deps $out')

    n.newline()
    n.newline()

    objects = []
    moddeps = []

    for f in glob.iglob('*.cpp'):
        basename = f.removesuffix('.cpp')
        infile = '../' + f
        objout = basename + '.o'
        depfile = basename + '.d'
        moddep = basename + '.moddep'
        n.build(outputs=moddep, rule='cxx_modulescan', inputs=f'../{basename}.cpp', variables={'ARGS': ARGS, 'OBJECTOUT': objout, 'DEPFILE': depfile})
        n.build(outputs=objout, rule='cxx_compile', inputs=f'../{basename}.cpp', variables={'ARGS': ARGS, 'DEPFILE': depfile}, dyndep='all_moddeps', order_only=['all_moddeps'])
        n.newline()

        objects.append(objout)
        moddeps.append(moddep)

    n.newline()
    n.build(outputs='main', rule='cxx_link', inputs=objects)
    n.build(outputs='all_moddeps', rule='combine_module_deps', inputs=moddeps)

    n.close()

