# Flutter-Termux 
![GitHub Release](https://img.shields.io/github/v/release/mumumusuc/termux-flutter)
![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/mumumusuc/termux-flutter/latest/total)

Run Flutter on Termux !

<p align="middle" float="left">
    <img src="https://raw.githubusercontent.com/mumumusuc/Flutter-Termux/main/image/screenshot.jpg" width="40%"/>
    <img src="https://raw.githubusercontent.com/mumumusuc/termux-flutter-impeller-demo/main/preview.webp" width="40%"/>
</p>

> [!CAUTION] 
> This build is incompatible with **Android 14**

## Install 

Download `flutter.deb` from [release](https://github.com/mumumusuc/termux-flutter/releases) page, then run 
```
apt install x11-repo
apt install /path/to/flutter.deb
```

Now `flutter` has been installed to `$PREFIX/opt/flutter`, test it with `flutter doctor -v`.

To uninstall `flutter` run 
```
apt remove flutter
```

## Flavors 

+ **Linux**(default)
  
  Use [Termux:X11](https://github.com/termux/termux-x11/releases) to preview your *flutter* app.

  ```bash
  export DISPLAY=:0 && termux-x11 :0 >/dev/null 2>&1 &
  flutter run -d linux
  ```

  In addition, edit `linux/my_application.cc` to make preview fit to your screen.

  ```diff
  - gtk_window_set_default_size(window, 1280, 720);
  // '500x740' is my choice.
  + gtk_window_set_default_size(window, 500, 740);
  ```

+ **Android**
  
  - [Install android-sdk](https://github.com/mumumusuc/termux-android-sdk/releases)

  - [Connect android device](https://github.com/bdloser404/Fluttermux?tab=readme-ov-file#how-to-connect-adb-devices)

  ```bash
  # list conected devices
  flutter devices
  flutter run -d <device_id>
  ```

+ **Web server**
  
  ```
  flutter run -d web-server --web-port 8080
  ```
  Open your web app then enter `localhost:8080`

  <p align="middle"><img src="https://raw.githubusercontent.com/mumumusuc/Flutter-Termux/main/image/web-server.jpg" width="40%"/></p>

## Note

- `impeller3d` is enabled but it doesn't work with `gtk3` currently. You can build a `glfw` application using `libflutter_engine.so` like this [demo](https://github.com/mumumusuc/termux-flutter-impeller-demo)

- [How to build flutter engine on Termux](https://github.com/mumumusuc/termux-flutter/wiki/How-to-build-flutter-engine-on-Termux)

