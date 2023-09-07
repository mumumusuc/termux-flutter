## 安装(施工中)
***推荐使用[sony/flutter-elinux](https://github.com/sony/flutter-elinux)，以下此为例***

1. 安装flutter-elinux
   
   
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
   
   重新运行`flutter-elinux doctor`看到输出结果
   ```bash
   flutter-elinux doctor
    
   # output
   Doctor summary (to see all details, run flutter doctor -v):
   [!] Flutter (Channel [user-branch], 3.13.2, on Linux, locale en_US.UTF-8)
   ...
   ```

2. todo
   
   
