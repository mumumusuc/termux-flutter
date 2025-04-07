#!/usr/bin/env python3

import os
import utils
import pathlib
import asyncio
import aiohttp
import tempfile
import itertools
import subprocess
import urllib.parse
from loguru import logger


async def _download(sess, url, dst):
    path = urllib.parse.urlparse(url).path
    name = pathlib.Path(path).name
    path = pathlib.Path(dst, name)
    try:
        async with sess.get(url) as resp:
            resp.raise_for_status()
            with open(path, 'wb') as f:
                async for chunk in resp.content.iter_chunked(8192):
                    f.write(chunk)
            return path
    except Exception:
        raise RuntimeError(f'✗ 下载失败 {name}')


async def _spawn(tasks):
    if not tasks:
        return []
    tasks = [asyncio.create_task(t) for t in tasks]
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_EXCEPTION)
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)
    return [r.result() for r in done]


async def _download_packages(out, arch, *src):
    timeout = aiohttp.ClientTimeout(total=500)
    async with aiohttp.ClientSession(timeout=timeout) as sess:
        urls = await _spawn([
            _resolve_packages(sess, arch, **it) for it in src
        ])
        urls = itertools.chain(*urls)
        return await _spawn([
            _download(sess, url, out) for url in urls
        ])


async def _resolve_packages(sess, arch, repo, dist, pkgs):
    if not repo or not pkgs:
        return {}

    bin = f'dists/{dist}/main/binary-{arch}/Packages'
    url = urllib.parse.urljoin(repo, bin)

    current = None
    package = {}

    async with sess.get(url) as resp:
        resp.raise_for_status()
        async for line in resp.content:
            line = line.decode().strip()

            if line.startswith('Package:'):
                current = line.split(':')[1].strip()
            elif current in pkgs and line.startswith('Filename:'):
                urlpath = line.split(':')[1].strip()
                package[current] = urllib.parse.urljoin(repo, urlpath)

            if len(package) == len(pkgs):
                break

    remains = [it for it in pkgs if it not in package]
    if remains:
        raise FileNotFoundError(f'packages{remains} not found.')
    return package.values()


def _extract(out, deb):
    subprocess.run(['dpkg', '-x', str(deb), str(out)], check=True, stderr=True)
    logger.info(f'✓ 成功安装 {deb.name}')


async def _work(out, arch, *src):
    with tempfile.TemporaryDirectory() as tmp:
        for deb in await _download_packages(tmp, arch, *src):
            _extract(out, deb)

    usr = out/'usr'
    dst = 'data/data/com.termux/files/usr'

    assert os.path.isdir(out/dst)

    try:
        usr.symlink_to(dst, True)
    except FileExistsError:
        if not usr.samefile(out/dst):
            raise

    pthread = out/'usr/lib/libpthread.a'
    pthread.write_bytes(b'INPUT(-lc)')


@utils.record
class Sysroot:
    def __init__(self, path: str, **kwargs):
        self.path = pathlib.Path(path).expanduser().resolve()
        self.data = {}

        if not self.path.exists():
            self.path.mkdir()
        assert self.path.is_dir(), f'bad sysroot path: "{path}"'

        for k, v in kwargs.items():
            if isinstance(v, dict):
                self.__include__(k, **v)

    def __include__(self, name, repo, dist, pkgs):
        assert name and repo and dist and pkgs

        self.data[name] = {'repo': repo, 'dist': dist, 'pkgs': pkgs}

    def __call__(self, arch: str):
        arch = utils.termux_arch(arch)

        if self.data:
            asyncio.run(_work(self.path, arch, *self.data.values()))
        else:
            logger.info('no work to do.')

    def __str__(self):
        return str(self.path)


if __name__ == '__main__':
    import fire
    import tomllib

    with open('build.toml', 'rb') as f:
        src = tomllib.load(f)

    fire.Fire(Sysroot(**src['sysroot']))
