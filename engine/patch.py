#!/bin/env python3

import argparse
import subprocess
import sys
import os


def parse_args(args):
    args = args[1:]
    parser = argparse.ArgumentParser(description='pack dart-sdk')
    parser.add_argument(
        'target',
        type=str,
        help='source path')
    parser.add_argument(
        '-p', '--patches',
        help='patches directory',
        default=os.getcwd())

    return parser.parse_args(args)


WORKS = {
    'src.patch': '',
    'dart.patch': 'third_party/dart',
    'skia.patch': 'third_party/skia',
}


def main(argv):
    args = parse_args(argv)

    target = os.path.abspath(args.target)
    assert os.path.isdir(target)

    patches = os.path.abspath(args.patches)
    assert os.path.isdir(patches)

    for patch, dir in WORKS.items():
        patch = os.path.join(patches, patch)
        assert os.path.isfile(patch)
        dir = os.path.join(target, dir)
        assert os.path.isdir(dir)

        subprocess.run(
            ['git', 'apply', patch, '--reject'],
            stdout=subprocess.PIPE,
            check=True,
            cwd=dir,
        )

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
