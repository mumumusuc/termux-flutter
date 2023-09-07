## 安装(施工中)
***推荐使用[sony/flutter-elinux](https://github.com/sony/flutter-elinux)，并以此为例***

### 1. 安装flutter-elinux

```bash
git clone https://github.com/sony/flutter-elinux.git
export PATH=$PATH:$(pwd)/flutter-elinux/bin
flutter-elinux doctor
    
# error message
```

下载[dart-sdk](https://github.com/mumumusuc/Flutter-Termux/releases/download/3.13.2/dart-sdk-aarch64.zip)并替换掉flutter自动下载的版本

```bash
unzip -od flutter-elinux/flutter/bin/cache/dart-sdk/ dart-sdk-aarch64.zip
   ```

重新运行`flutter-elinux doctor`看到正确输出
```bash
flutter-elinux doctor
    
# output
Doctor summary (to see all details, run flutter doctor -v):
[!] Flutter (Channel [user-branch], 3.13.2, on Linux, locale en_US.UTF-8)
   ...
   ```



### 2. 编译显示后端
[sony/flutter-embedded-linux](https://github.com/sony/flutter-embedded-linux) 提供`Wayland`、`X11`、`GBM`、`EGLStream`作为显示后端，这里选择编译`X11`
```bash
git clone https://github.com/sony/flutter-embedded-linux.git
cd flutter-embedded-linux
mkdir build && cd build
cmake -DBUILD_ELINUX_SO=ON -DBACKEND_TYPE=X11 -DCMAKE_BUILD_TYPE=Release \
        -DENABLE_ELINUX_EMBEDDER_LOG=OFF -DFLUTTER_RELEASE=ON ..
cmake --build .
```


编译产出`build/libflutter_elinux_x11.so`待用

```bash
ldd build/libflutter_elinux_x11.so         
# output
libxkbcommon.so => /data/data/com.termux/files/usr/lib/libxkbcommon.so
libEGL.so.1 => /data/data/com.termux/files/usr/lib/libEGL.so.1
libX11.so => /data/data/com.termux/files/usr/lib/libX11.so                                                
libflutter_engine.so => not found                 
libc++_shared.so => /data/data/com.termux/files/usr/lib/libc++_shared.so                                 
libdl.so => /data/data/com.termux/files/usr/lib/libdl.so
libm.so => /system/lib64/libm.so                
libc.so => /system/lib64/libc.so                   
ld-android.so => /system/lib64/ld-android.so
libdl.so => /system/lib64/libdl.so                 
libGLdispatch.so.0 => /data/data/com.termux/files/usr/lib/libGLdispatch.so.0                              
libxcb.so => /data/data/com.termux/files/usr/lib/libxcb.so                                                
libandroid-support.so => /data/data/com.termux/files/usr/lib/libandroid-support.so                        
libXau.so => /data/data/com.termux/files/usr/lib/libXau.so                                                libXdmcp.so => /data/data/com.termux/files/usr/lib/libXdmcp.so
```

TODO:
1. - [ ] 提供预编译文件
2. - [x] 更多[编译选项](https://github.com/sony/flutter-embedded-linux/wiki/Building-Embedded-Linux-embedding-for-Flutter#build-shared-library-for-flutter-elinux)


### 3. 替换Flutter预编译文件

在项目中执行`flutter-elinux run -d elinux-x11`时会下载无法运行的预编译的`impellerc`等文件，使用[engine-debug](https://github.com/mumumusuc/Flutter-Termux/releases/download/3.13.2/engine-aarch64-debug.zip)/[engine-release](https://github.com/mumumusuc/Flutter-Termux/releases/download/3.13.2/engine-aarch64-release.zip)替换它们

```bash
# {libflutter_engine.so, libflutter_elinux_x11.so} -> elinux-arm64-{debug, release}
# {other tools} -> linux-arm64-{, release}

# debug
cp engine-debug-aarch64/{impellerc, flutter_tester, font-subset, gen_snapshot, icudtl.dat, libflutter_engine.so, libpath_ops.so, libtessellator.so}  flutter-elinux/flutter/bin/cache/artifacts/engine/linux-arm64/
cp engine-debug-aarch64/libflutter_engine.so flutter-elinux/flutter/bin/cache/artifacts/elinux-arm64-debug/
cp flutter-embedded-linux/build/libflutter_elinux_x11.so flutter-elinux/flutter/bin/cache/artifacts/elinux-arm64-debug/
# release
cp engine-release-aarch64/{impellerc, flutter_tester, font-subset, gen_snapshot, icudtl.dat, libflutter_engine.so, libpath_ops.so, libtessellator.so}  flutter-elinux/flutter/bin/cache/artifacts/engine/linux-arm64-release/
cp engine-release-aarch64/libflutter_engine.so flutter-elinux/flutter/bin/cache/artifacts/elinux-arm64-release/
cp flutter-embedded-linux/build/libflutter_elinux_x11.so flutter-elinux/flutter/bin/cache/artifacts/elinux-arm64-release/
```



### 4. 运行项目
```
flutter-elinux create hello_world && cd hello_world
flutter-elinux pub get
# run debug
flutter-elinux run -d elinux-x11
# run release
fluttet-elinux run -d elinux-x11 --release
```


TODO:
1. - [ ] 依赖
2. - [ ] [窗口参数](https://github.com/sony/flutter-elinux/wiki/Running-flutter-apps#pass-custom-run-options-of-the-embedder)
3. - [ ] 源码编
