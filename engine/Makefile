.PHONY: sync config build install

ARGS     =
ROOT     = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
RUNTIME  = debug
DART_SDK = $(PREFIX)/lib/dart-sdk

PYTHON = $(PREFIX)/bin/python3
NINJA  = $(PREFIX)/bin/ninja
GIT    = $(PREFIX)/bin/git
GN     = $(PREFIX)/bin/gn

ifeq ($(strip $(DART_SDK)),)
override DART_SDK = $(error 'dart-sdk not found.')
else
$(DART_SDK):;$(error '`dart-sdk` not found at `$(DART_SDK)`')
endif

ifeq ($(filter "$(RUNTIME)", "debug" "profile" "release"),)
$(error Invalid runtime mode `$(RUNTIME)`, possible values are [debug|profile|release])
endif

ifeq ($(shell command -v vpython3),)
$(error env `PATH` not set. Consider running `export PATH=$$(pwd):$$PATH`)
endif

override CONFIGURE += 						\
	--target-os linux 						\
	--linux-cpu arm64 						\
	--embedder-for-target 					\
	--enable-fontconfig 					\
	--target-triple aarch64-linux-android 	\
	--clang --no-goma --no-backtrace 		\
	--no-enable-unittests 					\
	--no-prebuilt-dart-sdk 					\
	--no-build-embedder-examples 			\
	--target-toolchain $$PREFIX 			\
	--target-sysroot $$PREFIX/.. 			\
	--enable-impeller-3d --no-lto 			\
	--runtime-mode $(RUNTIME)

override GN_ARGS += 							\
	toolchain_prefix="aarch64-linux-android-" 	\
	use_default_linux_sysroot=false				\
	is_desktop_linux=false 						\
	test_enable_vulkan=false 					\
	skia_use_vulkan=false 						\
	shell_enable_vulkan=false 					\
	embedder_enable_vulkan=false 				\
	dart_platform_sdk=false

OUTPUT  = $(ROOT)src/out/linux_$(RUNTIME)_arm64
CONFIG  = $(OUTPUT)/build.ninja
VERSION = $(OUTPUT)/engine.version
FLUTTER = $(ROOT)src/flutter
INSTALL = $(ROOT)..

PREBUILT = $(PREBUILT.clang) $(PREBUILT.ninja) $(PREBUILT.gn) $(PREBUILT.dart)
PREBUILT.clang := $(addprefix src/buildtools/linux-arm64/clang/bin/,analyze-build clang clang++ clang-apply-replacements clang-cl clang-cpp clang-doc clang-format clang-include-fixer clang-refactor clang-scan-deps clang-tidy clangd dsymutil find-all-symbols git-clang-format intercept-build ld.lld ld64.lld lld lld-link llvm-ar llvm-bcanalyzer llvm-bitcode-strip llvm-cov llvm-cxxfilt llvm-debuginfod-find llvm-dlltool llvm-dwarfdump llvm-dwp llvm-gsymutil llvm-ifs llvm-install-name-tool llvm-lib llvm-libtool-darwin llvm-lipo llvm-ml llvm-mt llvm-nm llvm-objcopy llvm-objdump llvm-otool llvm-pdbutil llvm-profdata llvm-ranlib llvm-rc llvm-readelf llvm-readobj llvm-size llvm-strip llvm-symbolizer llvm-undname llvm-windres llvm-xray run-clang-tidy sancov scan-build-py wasm-ld)
PREBUILT.ninja := $(addprefix src/flutter/third_party/ninja/,ninja)
PREBUILT.gn    := $(addprefix src/flutter/third_party/gn/,gn)
PREBUILT.dart  := $(addprefix src/third_party/dart/tools/sdks/,dart-sdk)

define link
mkdir -p "$(dir $(2))" && ln -sf "$(abspath $(1))" "$(2)" > /dev/null 2>&1
endef

build: $(CONFIG) $(VERSION) $(NINJA)
	$(NINJA) -C $(OUTPUT) $(ARGS)

sync: $(PREBUILT)
	$(PYTHON) gclient.py sync $(ARGS) -DR --with_branch_heads --with_tags --no-history

install: install.engine install.dart-sdk

install.engine: $(VERSION)
	@$(PYTHON) $(ROOT)engine-install.py -v $(VERSION) --$(RUNTIME) $(OUTPUT) -o $(INSTALL)/engine.tar.gz

install.dart-sdk: $(VERSION)
	@$(PYTHON) $(ROOT)dart-sdk-install.py $(OUTPUT) -v $(VERSION) -o $(INSTALL)/dart-sdk.tar.gz

config: $(CONFIG)

$(CONFIG): $(FLUTTER)
	@$(PYTHON) $(FLUTTER)/tools/gn $(CONFIGURE) --gn-args '$(GN_ARGS)'

$(VERSION): $(FLUTTER)
	$(GIT) -C $(FLUTTER) rev-parse HEAD > $@

#$(FLUTTER): sync

$(dir $(firstword $(PREBUILT.clang)))%: $(PREFIX)/bin/%
	@$(call link,$<,$@)
$(PREBUILT.ninja): $(NINJA)
	@$(call link,$<,$@)
$(PREBUILT.gn): $(GN)
	@$(call link,$<,$@)
$(PREBUILT.dart): $(DART_SDK)
	@$(call link,$<,$@)
$(PREFIX)/bin/%:
	@$(error '`$(notdir $@)` not found.')
