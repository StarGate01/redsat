#!/bin/bash

NETWORKS="frontend monitor"
STACKS_COMMON="frontend radio"
STACKS_SERVER="frontend monitor"
STACKS="frontend monitor radio"

WSL=`uname -r | grep "Microsoft"`
ARCH=`uname -m`
if [ -z "$WSL" ]; then
    if [ "$ARCH" == "armv7l" ]; then
        echo "System: Raspberry"
        SYSC="-rpi"
    else
        echo "System: Default"
        SYSC=""
    fi
else
    echo "System: WSL"
    SYSC="-wsl"
fi

if [ "$1" == "up" ]; then
    echo "Starting REDSAT"
    echo "Creating networks"
    for NETWORK in $NETWORKS; do docker network create $NETWORK; done
    echo "Starting stacks"
    cd frontend && docker-compose up -d && cd ..
    cd monitor && docker-compose -f docker-compose$SYSC.yml up -d && cd ..
    cd radio && docker-compose up -d scheduler && cd ..
elif [ "$1" == "down" ]; then
    echo "Stopping REDSAT"
    echo "Stopping stacks"
    for STACK in $STACKS_COMMON; do cd $STACK && docker-compose down && cd ..; done
    cd monitor && docker-compose -f docker-compose$SYSC.yml down && cd ..
    echo "Removing networks"
    for NETWORK in $NETWORKS; do docker network remove $NETWORK; done
elif [ "$1" == "build" ]; then
    ARCH=`uname -m`
    echo "Building REDSAT for $ARCH$SYSC"
    for STACK in $STACKS_COMMON; do cd $STACK && docker-compose build && cd ..; done
    cd monitor && docker-compose -f docker-compose$SYSC.yml build && cd ..
elif [ "$1" == "radio" ]; then
    echo "Running radio component: $2"
    cd radio && docker-compose run --rm $2 /app/run.sh "${@:3}" && cd ..
fi