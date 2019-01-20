#!/bin/bash

: "${REDSAT_CONFIG_DIR:=/app/config}"

rm -rf ${REDSAT_CONFIG_DIR}/elements
mkdir -p $REDSAT_CONFIG_DIR/elements
cd $REDSAT_CONFIG_DIR/elements && wget -i $REDSAT_CONFIG_DIR/sources.list -O all.tmp

while read p; do
    SAT=`echo $p | cut -d, -f1`
    FNAME=`echo $p | cut -d, -f2`
    sed -n "/$SAT\\s*$/{p;n;p;n;p;q}" $REDSAT_CONFIG_DIR/elements/all.tmp >> "$REDSAT_CONFIG_DIR/elements/$FNAME.txt"
    cat "$REDSAT_CONFIG_DIR/elements/$FNAME.txt"
done <$REDSAT_CONFIG_DIR/sats.list

rm $REDSAT_CONFIG_DIR/elements/all.tmp
