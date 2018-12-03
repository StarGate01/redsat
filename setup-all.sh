#!/bin/bash

for dir in $(find . -maxdepth 1 -mindepth 1 -not -iwholename '*.git' -type d); do
    cd $dir
    [ -e setup.sh ] && ./setup.sh && echo "Executed $(basename $dir) setup"
    cd ..
done
