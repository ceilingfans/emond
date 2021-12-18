#!/usr/local/bin/python3.10

import glob
import sys
import argparse
from os import path
from core.lexer import lex
from core.interpreter import interpret
from core.test import run_test

VERSION = "emond language interpreter version 0.1"


class Colorizer:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main() -> None:
    argparser = argparse.ArgumentParser(
        description=VERSION,
        epilog="https://github.com/ceilingfans/emond",
    )
    argparser.add_argument("file", help="File to read code from", nargs="?")
    argparser.add_argument(
        "-v", "--version", help="prints version and exit", action="store_true"
    )
    argparser.add_argument(
        "-t", "--test", help="run internal tests", action="store_true"
    )
    argparser.add_argument(
        "-l",
        "--length",
        help="cell array length (default: 1000)",
        type=int,
        default=1000,
    )
    args = argparser.parse_args()

    if args.version:
        print("emond language interpreter version 0.1")
        exit(0)

    if args.test:
        files = glob.glob("test/*.test.em")
        passed = []
        failed = []
        print(f"Found {len(files)} test files in `test`")
        for file in files:
            print(f"Running {file}: ", end="")
            error = run_test(file)
            if error:
                print(f"{Colorizer.FAIL}FAILED{Colorizer.ENDC}")
                failed.append((file, error))
            else:
                print(f"{Colorizer.OKGREEN}✔{Colorizer.ENDC}")
                passed.append(file)
        print()
        print(f"Summary:\n\r    Passed: {Colorizer.OKGREEN}{len(passed)}{Colorizer.ENDC}, Failed: {Colorizer.FAIL}{len(failed)}{Colorizer.ENDC}")
        print()

        print(f"{Colorizer.OKGREEN}PASSED:{Colorizer.ENDC}")
        if not passed:
            print("    Nothing passed, oh no")
        else:
            for i, test in enumerate(passed):
                print(f"    {i + 1}: {test} {Colorizer.OKGREEN}✔{Colorizer.ENDC}")
        print()

        print(f"{Colorizer.FAIL}FAILED:{Colorizer.ENDC}")
        if not failed:
            print(f"    Nothing failed, good job")
        else:
            for i, test in enumerate(failed):
                print(f"    {i + 1}: {test[0]} -> {test[1]} {Colorizer.FAIL}✗{Colorizer.ENDC}")
        exit()

    if not args.file:
        sys.stderr.write("emond: error: no input file\n\r")
        exit(1)

    if not path.exists(args.file):
        sys.stderr.write(f"emond: error: invalid file path: {args.file}\n\r")
        exit(1)

    if args.length < 1:
        sys.stderr.write(
            f"emond: error: cell array length must be at least 1, received: {args.length}\n\r"
        )
        exit(1)

    src = open(args.file).read().strip()
    interpret(*lex(src), args.length)


if __name__ == "__main__":
    main()
