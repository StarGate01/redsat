#!/bin/bash

NETWORKS="frontend monitor"
STACKS="frontend monitor radio"

if [ "$1" == "up" ]; then
    echo "Starting REDSAT"
    for NETWORK in $NETWORKS; do docker network create $NETWORK; done
    for STACK in $STACKS; do cd $STACK && docker-compose up -d && cd ..; done
elif [ "$1" == "down" ]; then
    echo "Stopping REDSAT"
    for STACK in $STACKS; do cd $STACK && docker-compose down && cd ..; done
    for NETWORK in $NETWORKS; do docker network remove $NETWORK; done
elif [ "$1" == "build" ]; then
    echo "Building REDSAT"
    for STACK in $STACKS; do cd $STACK && docker-compose build && cd ..; done
fi