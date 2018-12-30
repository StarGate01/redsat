#!/bin/bash

NETWORKS="frontend monitor"
STACKS_SERVER="frontend monitor"
STACKS="frontend monitor radio"

if [ "$1" == "up" ]; then
    echo "Starting REDSAT"
    echo "Creating networks"
    for NETWORK in $NETWORKS; do docker network create $NETWORK; done
    echo "Starting stacks"
    for STACK in $STACKS_SERVER; do cd $STACK && docker-compose up -d && cd ..; done
    cd radio && docker-compose up -d scheduler && cd ..
elif [ "$1" == "down" ]; then
    echo "Stopping REDSAT"
    echo "Stopping stacks"
    for STACK in $STACKS; do cd $STACK && docker-compose down && cd ..; done
    echo "Removing networks"
    for NETWORK in $NETWORKS; do docker network remove $NETWORK; done
elif [ "$1" == "build" ]; then
    echo "Building REDSAT"
    for STACK in $STACKS; do cd $STACK && docker-compose build && cd ..; done
elif [ "$1" == "radio" ]; then
    echo "Running radio component: $2"
    cd radio && docker-compose run --rm $2 /app/run.sh "${@:3}" && cd ..
fi

# ./app.sh radio tlesync
# ./app.sh radio importer MOVEII 10-48-52_145950kHz.wav 1546080532