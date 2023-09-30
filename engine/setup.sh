cd src/flutter
git rev-parse HEAD > ../../engine.version
cd -

ln -sf $PREFIX/bin/gn src/flutter/third_party/gn/gn
ln -sf $PREFIX/bin/ninja src/flutter/third_party/ninja/ninja

dart_sdk_dir='src/third_party/dart/tools/sdks/dart-sdk'
if [ -d $dart_sdk_dir ]; then
    rm -r $dart_sdk_dir
fi
ln -s $PREFIX/opt/dart-sdk $dart_sdk_dir

clang_dir='src/buildtools/linux-arm64/clang/bin'
mkdir -p $clang_dir
# ls src/buildtools/linux-arm64/clang/bin |  awk '{print "ln -sf $(which " $0") " "$clang_dir/"$0}'
ln -sf $(which analyze-build) $clang_dir/analyze-build
ln -sf $(which clang) $clang_dir/clang
ln -sf $(which clang++) $clang_dir/clang++
ln -sf $(which clang-apply-replacements) $clang_dir/clang-apply-replacements
ln -sf $(which clang-cl) $clang_dir/clang-cl
ln -sf $(which clang-cpp) $clang_dir/clang-cpp
ln -sf $(which clang-doc) $clang_dir/clang-doc
ln -sf $(which clang-format) $clang_dir/clang-format
ln -sf $(which clang-include-fixer) $clang_dir/clang-include-fixer
ln -sf $(which clang-refactor) $clang_dir/clang-refactor
ln -sf $(which clang-scan-deps) $clang_dir/clang-scan-deps
ln -sf $(which clang-tidy) $clang_dir/clang-tidy
ln -sf $(which clangd) $clang_dir/clangd
ln -sf $(which dsymutil) $clang_dir/dsymutil
ln -sf $(which find-all-symbols) $clang_dir/find-all-symbols
ln -sf $(which git-clang-format) $clang_dir/git-clang-format
ln -sf $(which intercept-build) $clang_dir/intercept-build
ln -sf $(which ld.lld) $clang_dir/ld.lld
ln -sf $(which ld64.lld) $clang_dir/ld64.lld
ln -sf $(which lld) $clang_dir/lld
ln -sf $(which lld-link) $clang_dir/lld-link
ln -sf $(which llvm-ar) $clang_dir/llvm-ar
ln -sf $(which llvm-bcanalyzer) $clang_dir/llvm-bcanalyzer
ln -sf $(which llvm-bitcode-strip) $clang_dir/llvm-bitcode-strip
ln -sf $(which llvm-cov) $clang_dir/llvm-cov
ln -sf $(which llvm-cxxfilt) $clang_dir/llvm-cxxfilt
ln -sf $(which llvm-debuginfod-find) $clang_dir/llvm-debuginfod-find
ln -sf $(which llvm-dlltool) $clang_dir/llvm-dlltool
ln -sf $(which llvm-dwarfdump) $clang_dir/llvm-dwarfdump
ln -sf $(which llvm-dwp) $clang_dir/llvm-dwp
ln -sf $(which llvm-gsymutil) $clang_dir/llvm-gsymutil
ln -sf $(which llvm-ifs) $clang_dir/llvm-ifs
ln -sf $(which llvm-install-name-tool) $clang_dir/llvm-install-name-tool
ln -sf $(which llvm-lib) $clang_dir/llvm-lib
ln -sf $(which llvm-libtool-darwin) $clang_dir/llvm-libtool-darwin
ln -sf $(which llvm-lipo) $clang_dir/llvm-lipo
ln -sf $(which llvm-ml) $clang_dir/llvm-ml
ln -sf $(which llvm-mt) $clang_dir/llvm-mt
ln -sf $(which llvm-nm) $clang_dir/llvm-nm
ln -sf $(which llvm-objcopy) $clang_dir/llvm-objcopy
ln -sf $(which llvm-objdump) $clang_dir/llvm-objdump
ln -sf $(which llvm-otool) $clang_dir/llvm-otool
ln -sf $(which llvm-pdbutil) $clang_dir/llvm-pdbutil
ln -sf $(which llvm-profdata) $clang_dir/llvm-profdata
ln -sf $(which llvm-ranlib) $clang_dir/llvm-ranlib
ln -sf $(which llvm-rc) $clang_dir/llvm-rc
ln -sf $(which llvm-readelf) $clang_dir/llvm-readelf
ln -sf $(which llvm-readobj) $clang_dir/llvm-readobj
ln -sf $(which llvm-size) $clang_dir/llvm-size
ln -sf $(which llvm-strip) $clang_dir/llvm-strip
ln -sf $(which llvm-symbolizer) $clang_dir/llvm-symbolizer
ln -sf $(which llvm-undname) $clang_dir/llvm-undname
ln -sf $(which llvm-windres) $clang_dir/llvm-windres
ln -sf $(which llvm-xray) $clang_dir/llvm-xray
ln -sf $(which run-clang-tidy) $clang_dir/run-clang-tidy
ln -sf $(which sancov) $clang_dir/sancov
ln -sf $(which scan-build-py) $clang_dir/scan-build-py
ln -sf $(which wasm-ld) $clang_dir/wasm-ld
