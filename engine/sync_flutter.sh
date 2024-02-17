#/bin/env bash

ENGINE_DIR="$1/src/flutter"
FLUTTER_DIR="$1/../flutter"

ENGINE_TAG=$(git -C $ENGINE_DIR describe --tags)

if [ -d $FLUTTER_DIR ]; then
    FLUTTER_TAG=$(git -C $FLUTTER_DIR describe --tags)

    if [ "$FLUTTER_TAG" == "$ENGINE_TAG" ]; then 
        exit 0
    else
        rm -rf $FLUTTER_DIR
    fi
fi

git clone https://github.com/flutter/flutter -b $ENGINE_TAG $FLUTTER_DIR
