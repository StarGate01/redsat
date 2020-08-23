cd $(dirname "${BASH_SOURCE[0]}")/..
source persistent-data/config/station.config
./radio/scheduler/data/predict_skyfield.py --path persistent-data/config/elements/ --local | grep "$1 "
