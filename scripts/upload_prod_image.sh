#!/bin/bash

set -e

docker tag hemse:$PACKAGE_VERSION klawikj/hemse:$PACKAGE_VERSION
docker push klawikj/hemse:$PACKAGE_VERSION

docker tag hemse:latest klawikj/hemse:latest
docker push klawikj/hemse:latest
