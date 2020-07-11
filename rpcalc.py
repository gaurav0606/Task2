#!/usr/bin/env python3
# rpcalc exceution script
# for more info, see github.com/qguv/rpcalc

VERSION = '0.7.1'

import sys, rpcalc, argparse

parser = argparse.ArgumentParser(prog='rpcalc',
    description="A reverse polish notation calculator written in Python 3.",
    epilog="For more information, see qguv.github.io/rpcalc")

parser.add_argument("-s", "--stack-size",
    help="Limits the stack to a certain number of entries",
    type=int,
    metavar='N',
    default=None)

parser.add_argument("-i", "--initial-values",
    help="Initializes the stack with certain values already pushed. Accepts numbers separated by spaces. Values are pushed in order.",
    # The type is a string here to enable both int and float input. It will be
    # converted later, and throw an error if appropriate.
    type=str,
    nargs='+',
    metavar="X",
    default=None)

parser.add_argument("-e", "--exclusive",
    help="Sets the stack length to the amount of initialized values given with -i.",
    action="store_true")

parser.add_argument("--version",
    help="Prints the program version and exits.",
    action="store_true")

args = parser.parse_args()

def panic(code, message):
    '''Gives a pretty error message and exits with an error code.'''
    print("\nerror!", message, "\n")
    sys.exit(code)

# Get version and exit if --version is called
if args.version:
    print(VERSION)
    sys.exit()

# Complain if -e given without -i or with -s
if args.exclusive and not args.initial_values:
    panic(2, "-e (--exclusive) can only be used with -i (--initial-values)")
elif args.exclusive and args.stack_size:
    panic(2, "-e (--exclusive) can not be used with -s (--stack-size)")

# Complain if length of stack is less than amount of initial values
if args.stack_size and args.initial_values:
    if args.stack_size < len(args.initial_values):
        panic(2, "too many initial values for allocated stack size")

# Determining length of stack
if args.exclusive:
    stackLength = len(args.initial_values)
else:
    stackLength = args.stack_size or None

# Determining stack values
if args.initial_values:
    try:
        values = [ float(x) for x in args.initial_values ]
    except ValueError:
        panic(2, "-i (--initial-values) only accepts numbers")
else:
    values = []

# If the stack is limited, pad the values we found above with zeroes to make
# the stack of the desired length
if stackLength:
    if len(values) < stackLength:
        padding = stackLength - len(values)
        padding *= [0.0]
        values = padding + values

sys.exit(rpcalc.main(limit=stackLength, values=values))

