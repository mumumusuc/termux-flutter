#!/bin/env fish

python3 ./flutter/tools/gn  \
    --target-os linux \
    --linux-cpu arm64 \
    --runtime-mode debug \
    --embedder-for-target \
    --no-build-embedder-examples \
    --enable-fontconfig \
    --target-triple aarch64-linux-android \
    --clang \
    --no-lto \
    --no-goma \
    --no-backtrace \
    --no-enable-unittests \
    --enable-impeller-3d \
    --enable-impeller-opengles \
    --target-toolchain $PREFIX \
    --target-sysroot $PREFIX \
    --no-prebuilt-dart-sdk \
    --gn-args '
        toolchain_prefix="aarch64-linux-android-"
        use_default_linux_sysroot=false
        is_desktop_linux=false
        test_enable_vulkan=false
        skia_use_vulkan=false
        skia_use_egl=true
        shell_enable_vulkan=false
        embedder_enable_vulkan=false
        dart_platform_sdk=false
        impeller_enable_vulkan=true
        impeller_enable_compute=false
    '
