#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *


if (len(sys.argv) != 2):
    print("no valid file address")
    sys.exit(1)
else:
    console_args = sys.argv[1]
    cpu = CPU()
    cpu.load(sys.argv[1])
    cpu.run()


console_args = sys.argv[1]
cpu = CPU()

cpu.load(console_args)
cpu.run()


# run python ls8.py examples/print8.ls8