# Flutter-Termux

Run Flutter on Termux !

<img src="https://raw.githubusercontent.com/mumumusuc/Flutter-Termux/main/image/screenshot.jpg" alt="screenshot" width="200" align=center />


## [安装]

```bash
# flutter-3.13.6 as example
$ git clone https://github.com/flutter/flutter -b 3.13.6
$ ./install.py --engine engine.tar.gz --dart-sdk dart-sdk.tar.gz flutter

$ flutter create hello_world && cd hello_world
$ export DISPLAY=:0
$ termux-x11 :0 &
$ LD_LIBRARY_PATH=$PREFIX/lib flutter run
```

install.py
---

```
./install.py -h

usage: install.py [-h] [-c] [-n] [-d DART_SDK] [-e ENGINE] target

patch Flutter on Termux

positional arguments:
  target                path to flutter

options:
  -h, --help            show this help message and exit
  -c, --check           enable version check
  -n, --no-check        disable version check
  -d DART_SDK, --dart-sdk DART_SDK
                        path to dart-sdk
  -e ENGINE, --engine ENGINE
                        path to engine
```

依赖
---

```bash
$ apt install gtk3 fontconfig
```

## [编译]

[Setting up the Engine development environment](https://github.com/flutter/flutter/wiki/Setting-up-the-Engine-development-environment)

```bash
$ cd engine
$ DEPOT_TOOLS_UPDATE=0 gclient sync
$ cd src/flutter
$ git reset --hard <engine.version>
$ git apply ../../patches/flutter.patch --reject
$ cd -
$ DEPOT_TOOLS_UPDATE=0 gclient sync -DR --with_branch_heads --with_tags -v

$ cd src
$ ../patch.py -p ../patches .
$ ../configure.py
$ ninja -C out/linux_debug_arm64
```

## [打包]

```bash
$ ./engine-install.py -h
usage: engine-install.py [-h] -v VERSION  [-d DEBUG]  [-p PROFILE] [-r RELEASE] output

pack Flutter engine

positional arguments:
  output                install destination

options:
  -h, --help            show this help message
                        and exit
  -v VERSION, --version VERSION
                        engine.version
  -d DEBUG, --debug DEBUG
                        path to
                        linux_debug_arm64
  -p PROFILE, --profile PROFILE
                        parh to
                        linux_profile_arm64
  -r RELEASE, --release RELEASE
                        path to
                        linux_release_arm64
```

```bash
$ ./dart-sdk-install.py
usage: dart-sdk-install.py [-h] [-o OUTPUT] -v VERSION target

pack dart-sdk

positional arguments:
  target                source path

options:
  -h, --help            show this help message
                        and exit
  -o OUTPUT, --output OUTPUT
                        install destination
  -v VERSION, --version VERSION
                        engine.version
