#!/bin/bash

# Usage:
# run.sh satellite output_basename gui|nogui tcp|notcp
#   satellite: Satellite TLE file base name
#   output_basename: Capture file base name
#   gui|nogui: Enable/disable QT GUI
#   tcp|notcp: Enable/disable rtl_tcp on port 7373
# Note: This script respects device "rtl_tcp" and "audio" in station.config 

: "${REDSAT_TLE_DIR:=/app/TLE}"
: "${REDSAT_INPUT_DIR:=/app/input}"
: "${REDSAT_GR_DIR:=/app/gr}"
: "${REDSAT_DEPS_DIR:=/app/deps}"
: "${REDSAT_OS:=linux}"

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
    KIND="gui"
    echo "Info: No gui flag specified, defaulting to QT GUI"
else
    KIND="$3"
fi

if [ -z "$4" ]; then
    NETKIND="notcp"
    echo "Warning: No rtl_tcp choice specified, defaulting to disabled"
else
    NETKIND = $4
fi
if [[ $SDRDEV == *"audio"* ]]; then
    echo "Info: Using audio input"
    RECUDP="1"
    RECADDR=${SDRDEV#"audio="}
    if [ "$NETKIND" == "tcp" ]; then
        echo "Warning: Cannot enable rtl_tcp server in audio receive mode"
    fi
    echo "Info: Using Audio input on interface $RECADDR"
else
    echo "Info: Using Osmocom input"
    RECUDP="0"
    if [ "$NETKIND" == "tcp" ]; then
        echo "Info: Enabling rtl_tcp server on port 7373"
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
        GRDEV="rtl_tcp=127.0.0.1:7373"
    else
        echo "Info: Disabling rtl_tcp server"
        GRDEV=$SDRDEV
    fi
    echo "Info: Using $SDRDEV via $GRDEV"
fi

FREQ=`grep $SAT $REDSAT_TLE_DIR/sats.list | cut -d, -f3`
TLE="$REDSAT_TLE_DIR/elements/$SAT.txt"
TLEALL=`cat $TLE | sed 's/\r$//' | awk '{$1=$1};1' | paste -sd "," -`

META=${REDSAT_INPUT_DIR}/${OUTPUT_BASE}.meta
cat > $META <<-EOF
[main]
creation_time=$(date +%s)
samp_rate=$SDRSAMP
freq=$FREQ
gain=$SDRGAIN
[tle]
tle=$TLEALL
[position]
lat=$LAT
lon=$LON
elv=$ELV
EOF

if [ "$REDSAT_OS" == "linux" ]; then
    if [ "$RECUDP" == "0" ]; then
        python $REDSAT_GR_DIR/receiver_${KIND}_dev.py --config-file=$META --meta-dev=$GRDEV --meta-samp-rate-dev=$SDRSAMPDEV
    else
        python $REDSAT_GR_DIR/receiver_${KIND}_audio.py --config-file=$META --meta-rec-audio-dev=$RECADDR
    fi
else
    echo "Running native on windows..."
    META_WIN="${REDSAT_INPUT_DIR_WIN}\\${OUTPUT_BASE}.meta"
    if [ "$RECUDP" == "0" ]; then
        CMD_WIN="\"$REDSAT_GR_BIN_WIN\" \"$REDSAT_GR_DIR_WIN\\receiver_${KIND}_dev.py\" --config-file=\"$META_WIN\" --meta-dev=\"$GRDEV\" --meta-samp-rate-dev=\"$SDRSAMPDEV\""
    else
        CMD_WIN="\"$REDSAT_GR_BIN_WIN\" \"$REDSAT_GR_DIR_WIN\\receiver_${KIND}_audio.py\" --config-file=\"$META_WIN\" --meta-rec-audio-dev=\"$RECADDR\""
    fi
    echo "$CMD_WIN" > launch_win.bat
    cmd.exe /c launch_win.bat
fi

# gnuradio-companion