#!/usr/bin/env bash

docker run -p 8888:8888 -p 6006:6006 -it --rm \
       -v "$(pwd):/local" \
       -w "/local" \
       stat570:latest \
       "$@"
