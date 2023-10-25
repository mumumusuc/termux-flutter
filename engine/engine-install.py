#!/bin/env python3

import argparse
import tarfile
import sys
import os


def parse_args(args):
    args = args[1:]
    parser = argparse.ArgumentParser(description='pack Flutter engine')
    parser.add_argument(
        '-o', '--output',
        help='install destination',
        default=os.getcwd())
    parser.add_argument(
        '-v', '--version',
        help='engine.version',
        required=True)
    parser.add_argument(
        '-d', '--debug',
        help='path to linux_debug_arm64')
    parser.add_argument(
        '-p', '--profile',
        help='parh to linux_profile_arm64')
    parser.add_argument(
        '-r', '--release',
        help='path to linux_release_arm64')

    return parser.parse_args(args)


def install(files):
    def wrapper(tar, src, dst=''):
        if src is None:
            tar.add('.', dst, recursive=False)
            return
        for file in files():
            tar.add(
                os.path.join(src, file),
                os.path.join(dst, os.path.basename(file)))
    return wrapper


@install
def flutter_sdk(): return [
    'shader_lib',
    'flutter_tester',
    'font-subset',
    'scenec',
    'icudtl.dat',
    'impellerc',
    'libpath_ops.so',
    'libtessellator.so',
    'frontend_server.dart.snapshot',
    'gen/const_finder.dart.snapshot',
    'gen/flutter/lib/snapshot/isolate_snapshot.bin',
    'gen/flutter/lib/snapshot/vm_isolate_snapshot.bin']


@install
def linux_gtk(): return [
    'flutter_linux',
    'gen_snapshot',
    'libflutter_engine.so',
    'libflutter_linux_gtk.so']


@install
def linux_common(): return [
    'flutter_patched_sdk/platform_strong.dill',
    'flutter_patched_sdk/vm_outline_strong.dill']


@install
def sky_engine(): return [
    'gen/dart-pkg/sky_engine']


ENGINE = 'bin/cache/artifacts/engine/'


def main(argv):
    args = parse_args(argv)
    dest = os.path.abspath(args.output)
    if not os.path.basename(args.output):
        dest = os.path.join(dest, 'engine.tar.gz')

    path = os.path.dirname(dest)
    if not os.path.isdir(path):
        os.mkdir(path)

    vers = os.path.abspath(args.version)
    assert os.path.isfile(vers)

    debug, profile, release = args.debug, args.profile, args.release
    with tarfile.open(
        dest, 'w:gz', dereference=True, format=tarfile.GNU_FORMAT,
    ) as tar:
        tar.add(vers, 'engine.version')
        sky_engine(tar, release or debug or profile)
        flutter_sdk(tar, release or debug or profile, 'linux-arm64')
        linux_gtk(tar, debug, 'linux-arm64')
        linux_gtk(tar, profile, 'linux-arm64-profile')
        linux_gtk(tar, release, 'linux-arm64-release')
        linux_common(tar, debug or profile, 'common/flutter_patched_sdk')
        linux_common(tar, release, 'common/flutter_patched_sdk_product')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
