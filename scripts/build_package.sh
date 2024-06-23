#!/bin/bash

set -e

rm -rf ./build/
rm -rf ./dist/
python3 -m build
