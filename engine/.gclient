solutions = [
  {
    "managed": False,
    "name": "src/flutter",
    "url": "https://github.com/flutter/engine",
    "deps_file": "DEPS",
    "safesync_url": "",
    "custom_deps": {
      "src/third_party/dart/tools/sdks/dart-sdk": None,
      "src/flutter/third_party/gn": None,
      "src/flutter/third_party/ninja": None,
      "src/buildtools/linux-arm64/clang": None,
      "src/flutter/buildtools/linux-x64/clang": None,
      "src/flutter/buildtools/linux-arm64/clang": None,
      "src/fuchsia/sdk/linux": None,
      "src/flutter/third_party/dart/tools/sdks/dart-sdk": None,
      "src/third_party/google_fonts_for_unit_tests": None,
    },
    "custom_vars" : {
      "setup_githooks" : False,
      "use_cipd_goma" : False,
      "download_emsdk" : False,
      "download_dart_sdk" : False,
      "download_linux_deps" : False,
      "download_fuchsia_sdk" : False,
      "download_android_deps" : False,
      "download_windows_deps" : False,
      "download_fuchsia_deps" : False,
    },
    "custom_hooks" : [
    ],
  },
]
