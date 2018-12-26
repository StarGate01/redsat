#!/bin/bash

source /app/TLE/station.config

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
        CONFIG=/app/deps/rtl_mus/rtl_mus/config_rtl_custom.py
        cp -f /app/deps/rtl_mus/rtl_mus/config_rtl.py $CONFIG
        echo "rtl_tcp_host = '$HOST'" >> $CONFIG
        echo "rtl_tcp_port = $PORT" >> $CONFIG
        echo "Info: Attaching to $HOST:$PORT"
        cd /app/deps/rtl_mus/rtl_mus && python rtl_mus.py config_rtl_custom &
    else
        rtl_tcp -a 127.0.0.1 &
        cd /app/deps/rtl_mus/rtl_mus && python rtl_mus.py &
    fi
    GRDEV="rtl_tcp=localhost:7373"
else
    echo "Info: Disabling rtl_tcp server"
    GRDEV=$SDRDEV
fi

FREQ=`grep $SAT /app/TLE/sats.list | cut -d, -f3`
TLE="/app/TLE/elements/$SAT.txt"

META=/app/input/$OUTPUT_BASE.meta
echo `date +%s` >> $META
cat $TLE >> $META
echo $SDRSAMP >> $META
echo $FREQ >> $META
echo $LAT >> $META
echo $LON >> $META
echo $ELV >> $META

python /app/gr/$KIND.py --meta-output-file=/app/input/$OUTPUT_BASE.raw --meta-freq=$FREQ --meta-gain=$SDRGAIN --meta-dev=$GRDEV --meta-samp=$SDRSAMP

#gnuradio-companion /app/gr/receiver.grc