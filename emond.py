#!/usr/local/bin/python3.10

import glob
import sys
import argparse
from os import path
from core.lexer import lex
from core.interpreter import interpret
from core.test import run_test

VERSION = "emond language interpreter version 0.1"


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
        for file in files:
            err = run_test(file)
            if err:
                failed.append((file, err))
            else:
                passed.append(file)

        print(
            f"Test finished. Summary {{ passed: {len(passed)}, failed: {len(failed)} }}"
        )
        print()
        if not passed:
            print("0 test cases passed ;( oh no...")
        else:
            print("Passing")
            for i, test in enumerate(passed):
                print(f"{i+1}: {test}")

        print()

        if not failed:
            print("0 test cases failed :D yay!")
        else:
            print("Failing")
            for i, test in enumerate(failed):
                print(f"{i+1}: {test[0]} -> {test[1]}")
        exit(0)

    if not args.file:
        sys.stderr.write("emond: error: no input file\n")
        exit(1)

    if not path.exists(args.file):
        sys.stderr.write(f"emond: error: invalid file path: {args.file}\n")
        exit(1)

    if args.length < 1:
        sys.stderr.write(
            f"emond: error: cell array length must be at least 1, received: {args.length}\n"
        )
        exit(1)

    src = open(args.file).read().strip()
    interpret(*lex(src), args.length)


if __name__ == "__main__":
    main()
