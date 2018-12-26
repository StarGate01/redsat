#!/bin/bash

mkdir -p /app/TLE/elements
cd /app/TLE/elements && wget -i /app/TLE/sources.list -O all.tmp

while read p; do
    FNAME=${p// /-}
    sed -n "/$p\\s*$/{p;n;p;n;p;q}" /app/TLE/elements/all.tmp > "/app/TLE/elements/$FNAME.txt"
    cat "/app/TLE/elements/$FNAME.txt"
done </app/TLE/sats.list

rm /app/TLE/elements/all.tmp