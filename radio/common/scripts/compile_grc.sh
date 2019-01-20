#!/bin/bash

if [ -z "$1" ]; then
    echo "Error: No target directory specified"
    exit 1
else
    TARGET=$1
fi

echo "Building all GNU Radio flowcharts in $1"

shopt -s globstar
for f in $1/**/*.grc; do
    DN=`dirname $f`
    echo "Building $f in $DN"
    grcc -d $DN $f
done