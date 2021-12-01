#!/usr/bin/env python
import argparse
from multiprocessing import Process
import os
import sys

import pytest


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.testing")
    sys.path.insert(0, "src")
    sys.path.insert(0, "examples/simple")

    parser = argparse.ArgumentParser(description="""\nTesting.\n""")
    parser.add_argument(
        "-t",
        "--threads",
        dest="threads",
        type=int,
        help="Number of threads",
        metavar="THREADS",
    )
    __args = parser.parse_args()
    __threads = 5
    if __args.threads:
        sys.argv = sys.argv[1:]
        __threads = __args.threads

    __processes = [Process(target=pytest.main) for __i in range(__threads)]
    for __process in __processes:
        __process.start()
    return [__process.join() for __process in __processes]


if __name__ == "__main__":
    sys.exit(main())
