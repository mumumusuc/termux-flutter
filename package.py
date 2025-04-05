#!/usr/bin/env python3

import io
import utils
import string
import tarfile
import tempfile
import subprocess
from git import Repo
from loguru import logger
from pathlib import Path


def explore_file(src: Path):
    assert src.exists()

    if src.is_dir():
        for root, dirs, files in src.walk():
            rel = root.relative_to(src)
            for it in dirs:
                yield rel/it
            for it in files:
                yield rel/it


def explore_git(src: Path):
    assert src.is_dir()

    for it in Repo(src).tree().traverse():
        yield it.path
    git = src/'.git'
    for it in explore_file(git):
        yield '.git'/it


def emit(out, src, git):
    assert isinstance(src, (Path, bytes, list)), src

    if isdir := isinstance(src, list):
        yield {'out': out}
    if isinstance(src, bytes):
        yield {'out': out, 'src': src}
        return
    for src, it in explore(src, git):
        yield {
            'out': out/src.name/it if isdir else out/it,
            'src': src/it}


def explore(src, git):
    explore = explore_git if git else explore_file

    if not isinstance(src, list):
        src = [src]
    for src in src:
        src = src.absolute()
        if not src.exists():
            logger.warning(f'source not found: "{src}"')
            continue
        yield src, Path('.')
        for it in explore(src):
            yield src, it


def reset(info):
    info.uid = 0
    info.gid = 0
    info.mtime = 0
    info.uname = 'root'
    info.gname = 'root'
    info.mode |= 0o200


def add_bin(tar, out, src, mod=None):
    assert tar, out and isinstance(src, bytes)

    info = tarfile.TarInfo(str(out))
    info.mode = mod or 0o644
    info.size = len(src)
    reset(info)
    tar.addfile(info, io.BytesIO(src))


def add_file(tar, out, src, mod=None):
    assert tar, out and src.exists()

    info = tar.gettarinfo(src, out)
    info.mode = mod or info.mode
    reset(info)

    with open(src, 'rb') as f:
        tar.addfile(info, f)


def add_dir(tar, out, mod=None):
    assert tar, out

    cache = getattr(tar, '__cache__', set())
    tar.__cache__ = cache

    if out.parent == Path('.') or out in cache:
        return

    add_dir(tar, out.parent)
    info = tarfile.TarInfo(f'{out}/')
    info.type = tarfile.DIRTYPE
    info.mode = mod or 0o755
    reset(info)
    tar.addfile(info)
    cache.add(out)


def tar(path, data):
    if not data:
        logger.warning('no work to do.')
        return
    if isinstance(data, dict):
        data = [data]
    assert hasattr(data, '__iter__'), f'bad data format: "{data}"'

    with tarfile.open(path, mode='w:xz', format=tarfile.GNU_FORMAT, dereference=True) as tar:
        for it in data:
            out = it.get('out')
            src = it.get('src')
            mod = it.get('mod')
            assert out, f'bad out field: "{out}"'
            out = Path(out)
            assert mod is None or isinstance(mod, int)

            if isinstance(src, bytes):
                add_bin(tar, out, src, mod)
            elif not src or src.is_dir():
                add_dir(tar, out, mod)
            elif src.exists():
                add_file(tar, out, src, mod)
            else:
                raise FileNotFoundError(src)


class Output(object):
    def __init__(self, root, arch):
        self.any = None
        for it in utils.__MODE__:
            out = utils.target_output(root, arch, it)
            self.__dict__[it] = out
            if not self.any and Path(out).is_dir():
                self.any = out

        assert self.any, 'no valid out path found.'


@utils.record
class Package(object):
    def __init__(self, root, arch, control, resource, define=None):
        root = Path(root).resolve()
        assert root.is_dir(), f'bad flutter root path: "{root}"'
        self.globals = {
            'tag': utils.flutter_tag(root),
            'root': root,
            'arch': arch,
            'output': Output(root, arch),
            'version': utils.engine_version(root),
            'architecture': utils.termux_arch(arch),
        }
        self.defines = {
            k: eval(v, self.globals) for k, v in define.items()
        }
        self.control = control
        self.resource = resource
        self.__dict__.update(self.globals)
        self.__dict__.update(self.defines)

    def __format__(self, s, **extra):
        return string.Template(s).safe_substitute(
            **self.globals,
            **self.defines,
            **extra)

    def gen_control(self):
        bin = io.BytesIO()
        for k, v in self.control.items():
            bin.write(self.__format__(f'{k}: {v}\n').encode('utf8'))
        return {'out': 'control', 'src': bin.getvalue()}

    def gen_resource(self, name=None):
        if isinstance(name, str):
            yield from self.gen_resource_internal(name)
        elif isinstance(name, list):
            for it in name:
                yield from self.gen_resource_internal(it)
        elif not name:
            for it in self.resource.keys():
                yield from self.gen_resource_internal(it)
        else:
            raise ValueError(f'bad name format: "{name}"')

    def gen_resource_internal(self, name=None):
        if not (data := self.resource.get(name)):
            raise ValueError(f'unknown resource name: "{name}"')

        git = data.get('git', False)
        src = data.get('source', [])
        out = data.get('output')
        bin = data.get('binary', False)
        mod = data.get('mode')
        dep = data.get('define', {})
        ext = {}

        for k, v in dep.items():
            dep[k] = eval(v, self.globals, self.defines)

        # expect None, str, int
        if isinstance(mod, str):
            mod = int(mod, 8)
        if isinstance(mod, int):
            ext['mod'] = mod
        elif mod is not None:
            raise ValueError(f'bad mode type: "{type(mod)}"')
        # expect str, list
        if isinstance(out, str):
            out = [out]
        if isinstance(out, list):
            out = (Path(self.__format__(it, **dep)) for it in out)
        else:
            raise ValueError(f'bad output type: "{type(out)}"')
        # expect None, str, list
        if isinstance(src, str):
            src = self.__format__(src, **dep)
            src = src.encode('utf8') if bin else Path(src)
        if isinstance(src, list) and not bin:
            src = [Path(self.__format__(it, **dep)) for it in src]
        elif not isinstance(src, (bytes, Path)):
            raise ValueError(f'bad source type: "{type(src)}"')

        for out in out:
            for it in emit(out, src, git):
                yield it | ext

    def debuild(self, output, section=None):
        output = Path(output or '.').expanduser().resolve()
        if not output.parent.is_dir() or output.is_dir():
            raise ValueError(f'bad output path: "{output}"')

        with tempfile.TemporaryDirectory() as tmp:
            info = Path(tmp, 'debian-binary')
            ctrl = Path(tmp, 'control.tar.xz')
            data = Path(tmp, 'data.tar.xz')

            with open(info, 'wb+') as f:
                f.write(b'2.0\n')
            tar(ctrl, self.gen_control())
            tar(data, self.gen_resource(section))

            subprocess.run(
                    ['ar', 'rc', output, info, ctrl, data],
                    check=True,
                    stderr=True,
                    stdout=True)

        logger.info(f'✓ 构建完成 {output}')


if __name__ == '__main__':
    import fire
    import yaml

    with open('package.yaml', 'rb') as f:
        src = yaml.safe_load(f)
    pkg = Package(root='flutter', arch='arm64', **src)
    fire.Fire(pkg)
