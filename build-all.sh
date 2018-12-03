#!/bin/bash

for dir in $(find . -maxdepth 1 -mindepth 1 -not -iwholename '*.git' -type d); do
    cd $dir
    docker-compose build
    cd ..
done
