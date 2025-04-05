import os
import sys
import git
import inspect
from loguru import logger
from functools import wraps

__MARK__ = '/data/data/com.termux/files/usr'
__ARCH__ = dict(arm='arm', arm64='aarch64', x86_64='x86_64', x86='i686')
__MODE__ = ('release', 'debug', 'profile')


def is_termux():
    return os.environ.get('PREFIX') == __MARK__


def termux_arch(arch: str):
    if arch in __ARCH__:
        return __ARCH__[arch]
    if arch in __ARCH__.values():
        return arch

    raise ValueError(f'unknown arch: "{arch}"')


def target_triple(arch: str, api: int):
    if arch in __ARCH__:
        prefix = __ARCH__[arch]
    elif arch in __ARCH__.values():
        prefix = arch
    else:
        raise ValueError(f'unknown arch: "{arch}"')
    suffix = f'eabi{api}' if arch == 'arm' else api

    return f'{prefix}-linux-android{suffix}'


def target_output(root: str, arch: str, mode: str):
    root = os.path.abspath(os.path.expanduser(root))
    dest = f'linux_{mode}_{arch}'
    return os.path.join(root, 'engine', 'src', 'out', dest)


def flutter_tag(root: str):
    if not os.path.isdir(root):
        return None
    try:
        return git.Repo(root).git.describe('--tag', '--abbrev=0')
    except git.exc.GitCommandError:
        return None


# TODO: see bin/internal/update_engine_version.sh
def engine_version(root: str):
    root = os.path.join(root, 'bin/internal/engine.version')

    with open(root) as f:
        return f.read()


def recordm(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args and inspect.isclass(type(args[0])):
            class_name = args[0].__class__.__name__
            logged_args = args[1:]
        else:
            class_name = ''
            logged_args = args

        method = func.__name__
        if class_name:
            method = f'{class_name}.{method}'

        logged_args = [str(it) for it in logged_args]
        for k, v in kwargs.items():
            logged_args.append(f'{k}={v}')
        logged_args = ', '.join(logged_args)

        logger.debug(f'{method}({logged_args})')
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            sys.exit(1)
    return wrapper


def record(cls):
    for name, method in vars(cls).items():
        if callable(method) and not name.startswith('__'):
            setattr(cls, name, recordm(method))
    return cls


if __name__ == '__main__':
    import fire
    fire.Fire()
