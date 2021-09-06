#!/usr/bin/env python
import os
import argparse as argpar
import json
import subprocess


def prepLabextensionBundle():
    subprocess.run(["jlpm", "clean:slate"])


def nexus(dryrun=False):
    """release on nexus"""
    # build the source (sdist) and binary wheel (bdist_wheel) releases
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


def package(dryrun=False):
    """Package app"""
    # build the source (sdist) and binary wheel (bdist_wheel) releases
    subprocess.run(["python", "setup.py", "clean", "sdist", "bdist_wheel"])


def doRelease(dryrun=False):
    # prep the build area for the labextension bundle
    prepLabextensionBundle()

    package(dryrun)
    nexus(dryrun)


def main():
    parser = argpar.ArgumentParser()

    parser.add_argument(
        "--dryrun",
        action="store_true",
        help="Perform a dryrun build of all other release actions",
    )

    parsed = vars(parser.parse_args())

    doRelease(dryrun=parsed["dryrun"])


if __name__ == "__main__":
    main()