#!/bin/env bash

function get_url() {
    name="$1"
    repo=$(apt show "$name" 2>/dev/null | grep -m1 "APT-Sources:" | awk '{print $2}')
    if [ -z "$repo" ]; then
        echo "错误: 无法找到包 '$name' 的仓库地址。请确认包名正确且已更新APT缓存。"
        exit 1
    fi
    path=$(apt-cache show "$name" 2>/dev/null | grep -m1 "Filename:" | awk '{print $2}')
    if [ -z "$path" ]; then
        echo "错误: 无法找到包 '$name' 的Filename信息。"
        exit 1
    fi
    echo "$repo/$path"
}

function get_repo() {
    name="$1"
    repo=$(apt show "$name" 2>/dev/null | grep -m1 "APT-Sources:" | awk '{print $2}')
    if [ -z "$repo" ]; then
        echo "错误: 无法找到包 '$name' 的仓库地址。请确认包名正确且已更新APT缓存。"
        exit 1
    fi
    echo $repo@$name
}

while IFS= read pkg; do
    get_repo $pkg
done < /dev/stdin
