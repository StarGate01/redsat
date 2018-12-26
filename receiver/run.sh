#!/bin/bash

# TODO document usage here 
# 

# 
: "${REDSAT_TLE_DIR:=/app/TLE}"
: "${REDSAT_INPUT_DIR:=/app/input}"
: "${REDSAT_GR_DIR:=/app/gr}"
: "${REDSAT_DEPS_DIR:=/app/input}"

source ${REDSAT_TLE_DIR}/station.config

if [ -z "$1" ]; then
    SAT="MOVEII"
    echo "Warning: No satellite specified, defaulting to MOVE-II"
else
    SAT=$1
fi

if [ -z "$2" ]; then
    OUTPUT_BASE=`date +%s`
    echo "Warning: No output file specified, defaulting to current unix time stamp"
else
    OUTPUT_BASE=$2
fi

if [ -z "$3" ]; then
    KIND="receiver"
    echo "Info: No gui flag specified, defaulting to QT GUI"
else
    KIND="receiver_nogui"
fi

if [ -z "$4" ]; then
    echo "Info: Enabling rtl_tcp server on localhost:7373"
    if [[ $SDRDEV == *"rtl_tcp"* ]]; then
        ADDR=${SDRDEV#"rtl_tcp="}
        HOST=`echo $ADDR | cut -d':' -f1`
        PORT=`echo $ADDR | cut -d':' -f2`
        CONFIG=$REDSAT_DEPS_DIR/rtl_mus/rtl_mus/config_rtl_custom.py
        cp -f $REDSAT_DEPS_DIR/rtl_mus/rtl_mus/config_rtl.py $CONFIG
        echo "rtl_tcp_host = '$HOST'" >> $CONFIG
        echo "rtl_tcp_port = $PORT" >> $CONFIG
        echo "Info: Attaching to $HOST:$PORT"
        cd $REDSAT_DEPS_DIR/rtl_mus/rtl_mus && python rtl_mus.py config_rtl_custom &
    else
        rtl_tcp -a 127.0.0.1 &
        cd $REDSAT_DEPS_DIR/rtl_mus/rtl_mus && python rtl_mus.py &
    fi
    GRDEV="rtl_tcp=localhost:7373"
else
    echo "Info: Disabling rtl_tcp server"
    GRDEV=$SDRDEV
fi

FREQ=`grep $SAT $REDSAT_TLE_DIR/sats.list | cut -d, -f3`
TLE="$REDSAT_TLE_DIR/elements/$SAT.txt"

META=${REDSAT_INPUT_DIR}/${OUTPUT_BASE}.meta
cat > $META <<-EOF
[main]
creation_time=$(date +%s)
samp_rate=$SDRSAMP
freq=$FREQ
gain=$GAIN
dev=$GRDEV
[tle]
tle=$(tr '\n' ';' < $TLE)
[position]
lat=$LAT
lon=$LON
elv=$ELV
EOF

python $REDSAT_GR_DIR/$KIND.py -c $META

#gnuradio-companion $REDSAT_GR_DIR/receiver.grc