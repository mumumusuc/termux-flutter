# Flutter-Termux

Run Flutter on Termux !

<p align="middle" float="left">
    <img src="https://raw.githubusercontent.com/mumumusuc/Flutter-Termux/main/image/screenshot.jpg" width="40%"/>
    <img src="https://raw.githubusercontent.com/mumumusuc/termux-flutter-impeller-demo/main/preview.webp" width="40%"/>
</p>

## Install 

For the latest version, run

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/mumumusuc/termux-flutter/main/install)"
```
or a specific version if you are interested in

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/mumumusuc/termux-flutter/main/install)" - <version>
```

>[!WARNING]
>the script will download latest release assets and clone *flutter* into your **CURRENT** directory

Before `flutter run` please remember to install these dependencies and set `DISPLAY` env.
```bash
apt install which gtk3 fontconfig xorgproto ninja cmake clang pkg-config

export DISPLAY=:0
termux-x11 :0 >/dev/null 2>&1 &
```

Now create a project then run it. 
```bash
flutter create hello_world && cd hello_world
flutter run
```

Open [Termux:X11](https://github.com/termux/termux-x11/releases) and enjoy the *flutter* on Termux.

## Flavors 

+ **Linux**(default)
  
  *Termux* is treated as *Linux* by default, use [Termux:X11](https://github.com/termux/termux-x11/releases) to preview your *flutter* app.

  ```bash
  export DISPLAY=:0 && termux-x11 :0 >/dev/null 2>&1 &
  flutter run
  ```

  In addition, edit `linux/my_application.cc` to make preview fit to your screen.

  ```diff
  - gtk_window_set_default_size(window, 1280, 720);
  // '500x740' is my choice.
  + gtk_window_set_default_size(window, 500, 740);
  ```

+ **Android**
  
  - [Install android-sdk](https://github.com/AndroidIDEOfficial/androidide-tools/?tab=readme-ov-file)

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

