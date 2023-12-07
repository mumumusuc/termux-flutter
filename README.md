# Flutter-Termux

Run Flutter on Termux !

<p align="middle" float="left">
    <img src="https://raw.githubusercontent.com/mumumusuc/Flutter-Termux/main/image/screenshot.jpg" width="40%"/>
    <img src="https://raw.githubusercontent.com/mumumusuc/termux-flutter-impeller-demo/main/preview.webp" width="40%"/>
</p>


## Install 
1. clone this repo or just download the [`install.py`](https://github.com/mumumusuc/termux-flutter/blob/main/install.py).


2. download `dart-sdk.tar.gz` and `engine.tar.gz` from [release](https://github.com/mumumusuc/termux-flutter/releases) page.
   
3. run
   ```bash
    # flutter-3.13.6 as example
    $ git clone https://github.com/flutter/flutter -b 3.13.6

    # install patched engine & dart-sdk
    $ path/to/install.py --engine path/to/engine.tar.gz --dart-sdk path/to/dart-sdk.tar.gz path/to/flutter

    # set flutter path
    $ export PATH=$PATH:$(pwd)/flutter/bin

    # install dependence
    $ apt install gtk3 fontconfig xorgproto ninja cmake clang pkg-config

    # create & run
    $ flutter create hello_world && cd hello_world
    $ export DISPLAY=:0 && termux-x11 :0 &
    $ flutter run
    ```
4. a [video](https://github.com/mumumusuc/termux-flutter/issues/7#issuecomment-1790704873) example using `fish`

## Note

- `impeller3d` is enabled but it doesn't work with `gtk3` currently. You can build a `glfw` application using `libflutter_engine.so` like this [demo](https://github.com/mumumusuc/termux-flutter-impeller-demo)

- [How to build flutter engine on Termux](https://github.com/mumumusuc/termux-flutter/wiki/How-to-build-flutter-engine-on-Termux)

