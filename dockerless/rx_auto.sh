# Usage rx_auto.sh [satellite] [start timestamp] [duration=1200]

# for testing: ./rx_auto.sh MOVEII $((`date +%s`+5)) 60

CURRENT_TIME=`date +%s`
START_TIME=$2

date

if [ -z "$3" ]; then
	DURATION=$((60*12))
else
	DURATION=$3
fi

DELTA=$((${START_TIME}-${CURRENT_TIME}))

echo "delta: $DELTA"
if (( $DELTA > 0 )); then
	sleep $DELTA
        cd $(dirname "${BASH_SOURCE[0]}")
	timeout "${DURATION}s" ./rx_run.sh $1
else
	echo "already over. doing nothing"
fi

echo "done."
