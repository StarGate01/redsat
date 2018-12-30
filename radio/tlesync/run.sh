#!/bin/bash

rm -rf /app/TLE/elements
mkdir -p /app/TLE/elements
cd /app/TLE/elements && wget -i /app/TLE/sources.list -O all.tmp

while read p; do
    SAT=`echo $p | cut -d, -f1`
    FNAME=`echo $p | cut -d, -f2`
    sed -n "/$SAT\\s*$/{p;n;p;n;p;q}" /app/TLE/elements/all.tmp >> "/app/TLE/elements/$FNAME.txt"
    cat "/app/TLE/elements/$FNAME.txt"
done </app/TLE/sats.list

rm /app/TLE/elements/all.tmp