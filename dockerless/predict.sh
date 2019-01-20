cd $(dirname "${BASH_SOURCE[0]}")/..
source persistent-data/config/station.config
python radio/scheduler/data/predict.py --path persistent-data/config/elements/ --local | grep "$1"
