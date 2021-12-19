#!/usr/local/bin/python3.10

import argparse
from core.parser import parse
from core.interpreter import Interpreter
from core.error import print_error
from os import path

VERSION = "emond lang interpreter v0.2"


def print_version():
    print(VERSION)


def main():
    parser = argparse.ArgumentParser(
        description=VERSION,
        epilog="https://github.com/ceilingfans/emond"
    )
    parser.add_argument(
        "file",
        help="file to get source code",
        nargs="?"
    )
    parser.add_argument(
        "-v",
        "--version",
        help="prints version information and exits (defualt: false)",
        action="store_true"
    )
    parser.add_argument(
        "-e",
        "--exit_on_fail",
        help="dont exit when an error is occured (default: true)",
        action="store_false"
    )
    parser.add_argument(
        "-s",
        "--silent",
        help="silence output (default: false)",
        action="store_true"
    )
    parser.add_argument(
        "-p",
        "--print_to_string",
        help="send output to string instead of stdout (default: false)",
        action="store_true"
    )
    parser.add_argument(
        "-a",
        "--args",
        help="prints out the arguments provided and exits",
        action="store_true"
    )
    parser.add_argument(
        "-l",
        "--length",
        help="set length of cell array (default: 1000)",
        default=1000,
        type=int
    )
    parser.add_argument(
        "-i",
        "--input",
        help="set input variable (default: \"\")",
        default="",
        type=str
    )
    args = parser.parse_args()

    if args.version:
        print_version()
        exit(0)

    if args.args:
        print(args)
        exit(0)

    if not args.file:
        print_error("emond: no input files\n")
        exit(1)

    if not path.exists(args.file):
        print_error(f"emond: invalid filepath: {args.file}")
        exit(1)

    if args.length < 1:
        print_error(f"emond: cell array length must be at least 1, received: {args.length}")
        exit(1)

    src = open(args.file).read().strip()
    tree = parse(src, args.file, args.exit_on_fail)
    interpreter = Interpreter(
        tree=tree,
        cell_array_size=args.length,
        filepath=args.file,
        silent=args.silent,
        print_to_string=args.print_to_string,
        exit_on_fail=args.exit_on_fail,
        input_text=args.input
    )

    interpreter.interpret()


if __name__ == "__main__":
    main()