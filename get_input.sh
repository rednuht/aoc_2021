#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

mkdir -p "$DIR/day$1"
curl -s https://adventofcode.com/2021/day/$1/input \
  -H "cookie: session=$(cat ~/.aoc_session_cookie)" >"$DIR/day$1/input.txt"
