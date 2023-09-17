#!/bin/env fish

#DEPOT_TOOLS_UPDATE=0 gclient sync -DR --with_branch_heads --with_tags -v

python3 ./flutter/tools/gn  \
    --target-os linux \
    --linux-cpu arm64 \
    --runtime-mode debug \
    --embedder-for-target \
    #--disable-desktop-embeddings \
    --no-build-embedder-examples \
    --enable-fontconfig \
    --target-triple aarch64-linux-android \
    --full-dart-sdk \
    --clang \
    --lto \
    --no-goma \
    --no-backtrace \
    #--no-stripped \
    --no-enable-unittests \
    --target-toolchain $PREFIX \
    --target-sysroot $PREFIX \
    --no-prebuilt-dart-sdk \
    --gn-args '
        toolchain_prefix="aarch64-linux-android-"
        use_default_linux_sysroot=false
        is_desktop_linux=false
        shell_enable_vulkan=false
        skia_use_vulkan=false
        embedder_enable_vulkan=false
        test_enable_vulkan=false
    '
