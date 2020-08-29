# Usage rx_auto.sh [satellite] [start timestamp] [duration=1200]

# for testing: ./rx_auto.sh MOVEII $((`date +%s`+5)) 60

cd $(dirname "${BASH_SOURCE[0]}")

CURRENT_TIME=`date +%s`
START_TIME=$2

date

if [ -z "$3" ]; then
	DURATION=$((60*12))
else
	DURATION=$3
fi

DELTA=$((${START_TIME}-${CURRENT_TIME}))
DELTA_END=$((${DELTA}+${DURATION}))

echo "delta: $DELTA $DELTA_END"
if (( $DELTA_END >= 0 )); then
	sleep $DELTA
	timeout "${DURATION}s" ./rx_run.sh "$1"
else
	echo "already over. doing nothing"
fi

sleep 5
rtl_biast -b 0

# TODO read rtl device from config file
python ../radio/receiver/data/gr/disable_bias.py -d rtl_tcp=10.0.0.101
echo "done."
