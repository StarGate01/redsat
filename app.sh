#!/bin/bash

NETWORKS="frontend monitor"
STACKS_COMMON="frontend radio"
STACKS_SERVER="frontend monitor"
STACKS="frontend monitor radio"

if [ "$1" == "up" ]; then
    echo "Starting REDSAT"
    echo "Creating networks"
    for NETWORK in $NETWORKS; do docker network create $NETWORK; done
    echo "Starting stacks"
    cd frontend && docker-compose up -d && cd ..
    WSL=`uname -r | grep "Microsoft"`
    if [ -z "$WSL" ]; then
        echo "Building monitoring for $ARCH"
        cd monitor && docker-compose up -d && cd ..
    else
        echo "Building monitoring for $ARCH (WSL)"
        cd monitor && docker-compose -f docker-compose-wsl.yml up -d && cd ..
    fi
    cd radio && docker-compose up -d scheduler && cd ..
elif [ "$1" == "down" ]; then
    echo "Stopping REDSAT"
    echo "Stopping stacks"
    for STACK in $STACKS; do cd $STACK && docker-compose down && cd ..; done
    echo "Removing networks"
    for NETWORK in $NETWORKS; do docker network remove $NETWORK; done
elif [ "$1" == "build" ]; then
    ARCH=`uname -m`
    echo "Building REDSAT for $ARCH"
    for STACK in $STACKS; do cd $STACK && docker-compose build && cd ..; done
elif [ "$1" == "radio" ]; then
    echo "Running radio component: $2"
    cd radio && docker-compose run --rm $2 /app/run.sh "${@:3}" && cd ..
fi