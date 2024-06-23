#!/bin/bash

set -e

twine upload --repository pypi dist/* --verbose
