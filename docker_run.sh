#!/usr/bin/env bash

docker run -p 8888:8888 -it --rm \
       -v "$(pwd):/notebooks/local" \
       stat570:latest \
       "$@"
