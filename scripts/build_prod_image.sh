#!/bin/bash

set -e

docker build -t hemse:$PACKAGE_VERSION -t hemse:latest --build-arg PACKAGE_VERSION -f docker/prod.dockerfile .
