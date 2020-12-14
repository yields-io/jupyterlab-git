#!/usr/bin/env python
import os
import argparse as argpar
import json
import subprocess
from packaging.version import parse

from setupbase import get_version

VERSION = os.environ.get("VERSION")


def prepLabextensionBundle():
    subprocess.run(["jlpm", "clean:slate"])


def nexus(dryrun=False):
    """release on nexus"""
    # build the source (sdist) and binary wheel (bdist_wheel) releases
    subprocess.run(["python", "setup.py", "clean", "sdist", "bdist_wheel"])
    if not dryrun:
        subprocess.run(
            [
                "twine",
                "upload",
                "--repository-url",
                "https://nexus.yields.io/repository/y-python-release/",
                "dist/*",
            ]
        )


def npmjs(dryrun=False):
    """release on npmjs"""
    subprocess.run(["npm", "pack"])


def doRelease(test=False):
    # prep the build area for the labextension bundle
    prepLabextensionBundle()

    # release to pypi and npmjs
    npmjs(test)
    nexus(test)


def main():
    parser = argpar.ArgumentParser()

    parser.add_argument(
        "--test",
        action="store_true",
        help="Release to Pypi test server; performs a dryrun of all other release actions",
    )

    parsed = vars(parser.parse_args())

    doRelease(test=parsed["test"])


if __name__ == "__main__":
    main()
