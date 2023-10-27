#!/bin/env python3

import argparse
import tarfile
import shutil
import sys
import os


def parse_args(args):
    args = args[1:]
    parser = argparse.ArgumentParser(description='patch Flutter on Termux')
    parser.add_argument(
        'target',
        help='path to flutter')
    parser.add_argument(
        '-c', '--check',
        action='store_true',
        help='enable version check',
        default=True)
    parser.add_argument(
        '-n', '--no-check',
        action='store_false',
        dest='check',
        help='disable version check')
    parser.add_argument(
        '-d', '--dart-sdk',
        help='path to dart-sdk')
    parser.add_argument(
        '-e', '--engine',
        help='path to engine')

    return parser.parse_args(args)


def check_version(flutter, version, name):
    if not os.path.isfile(flutter) and version != flutter:
        print(
            'inconsisdent engine version:\n'
            '  flutter:\n'
            '  {} \n'
            '  {}:\n'
            '  {} \n'
            'you may checkout the correct branch of flutter '
            'or run with option "--no-check" to disable version check.'
            .format(flutter, name, version))
        exit(1)


def valid_version(dest, check):
    ver = os.path.join(dest, 'bin', 'internal', 'engine.version')
    try:
        with open(ver) as f:
            return f.read() if check else ver
    except OSError:
        print(
            'missing "engine.version",',
            'is it the correct flutter path(%s)?\n' % dest)
        exit(1)


def enter(path):
    os.makedirs(path, exist_ok=True)
    os.chdir(path)


def copy_engine(dst, src, ver):
    file = 'engine.version'
    dest = os.path.join(dst, 'bin', 'cache', 'artifacts', 'engine')

    enter(dest)
    with tarfile.open(src) as tar:
        check_version(
            ver,
            tar.extractfile(file).read().decode('utf8'),
            os.path.basename(src))
        tar.extractall()

    if not os.path.isfile(ver):
        ver = file

    pkg = os.path.join(dst, 'bin', 'cache', 'pkg')
    os.makedirs(pkg, exist_ok=True)
    if os.path.isdir(os.path.join(pkg, 'sky_engine')):
        shutil.rmtree(os.path.join(pkg, 'sky_engine'))
    shutil.move('sky_engine', pkg)
    shutil.copy(ver, os.path.join(dst, 'bin', 'cache', 'linux-sdk.stamp'))
    shutil.copy(ver, os.path.join(dst, 'bin', 'cache', 'flutter_sdk.stamp'))
    shutil.copy(ver, os.path.join(dst, 'bin', 'cache', 'font-subset.stamp'))
    os.remove(file)


def copy_dart_sdk(sdk, dst, ver):
    file = 'engine-dart-sdk.stamp'
    dest = os.path.join(dst, 'bin', 'cache')

    enter(dest)
    with tarfile.open(sdk) as tar:
        check_version(
            ver,
            tar.extractfile(file).read().decode('utf8'),
            os.path.basename(sdk))
        tar.extractall()

    if os.path.isfile(ver):
        shutil.copy(ver, os.path.join(dest, file))

    try:
        os.remove(os.path.join(dest, 'dart-sdk-linux-arm64.zip'))
        os.remove(os.path.join(dest, 'dart-sdk.old'))
    except OSError:
        pass


def main(argv):
    root = os.getcwd()
    args = parse_args(argv)
    dest = os.path.abspath(args.target)
    vers = valid_version(dest, args.check)

    if args.engine:
        engine = os.path.abspath(args.engine)
        assert tarfile.is_tarfile(engine)
        copy_engine(dest, engine, vers)

    os.chdir(root)

    if args.dart_sdk:
        dart = os.path.abspath(args.dart_sdk)
        assert tarfile.is_tarfile(dart)
        copy_dart_sdk(dart, dest, vers)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
