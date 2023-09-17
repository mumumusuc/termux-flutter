#!/bin/env python3

import argparse
import tarfile
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
        '-o', '--output',
        help='install destination',
        default=os.getcwd())
    parser.add_argument(
        '-v', '--version',
        type=str,
        help='engine.version',
        required=True)

    return parser.parse_args(args)


def main(argv):
    args = parse_args(argv)
    vers = os.path.abspath(args.version)
    assert os.path.isfile(vers)
    dest = os.path.abspath(args.output)
    if not os.path.basename(args.output):
        dest = os.path.join(dest, '{{NAME}}')
    path = os.path.dirname(dest)
    if not os.path.isdir(path):
        os.mkdir(path)

    version = os.path.abspath(args.version)
    assert os.path.isfile(version)

    target = os.path.abspath(args.target)
    assert os.path.isdir(target)

    os.chdir(target)
    assert os.path.isdir('dart-sdk')

    dest = dest.replace('{{NAME}}', 'dart-sdk.tar.gz')
    with tarfile.open(dest, 'w:gz', format=tarfile.GNU_FORMAT) as tar:
        tar.add(vers, 'engine-dart-sdk.stamp')
        tar.add('dart-sdk')

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
