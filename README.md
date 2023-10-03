# Flutter-Termux

Run Flutter on Termux !

<p align="middle" float="left">
    <img src="https://raw.githubusercontent.com/mumumusuc/Flutter-Termux/main/image/screenshot.jpg" width="40%"/>
    <img src="https://raw.githubusercontent.com/mumumusuc/termux-flutter-impeller-demo/main/preview.webp" width="40%"/>
</p>


## Install

```bash
# flutter-3.13.6 as example
$ git clone https://github.com/flutter/flutter -b 3.13.6

# install patched engine & dart-sdk
$ ./install.py --engine engine.tar.gz --dart-sdk dart-sdk.tar.gz flutter

# install dependence
$ apt install gtk3 fontconfig

# create & run
$ flutter create hello_world && cd hello_world
$ export DISPLAY=:0
$ termux-x11 :0 &
$ flutter run
```

## Note

- `impeller3d` is enabled but it doesn't work with `gtk3` currently. You can build a `glfw` application using `libflutter_engine.so` like this [demo](https://github.com/mumumusuc/termux-flutter-impeller-demo)

- [How to build flutter engine on Termux](https://github.com/mumumusuc/termux-flutter/wiki/How-to-build-flutter-engine-on-Termux)

