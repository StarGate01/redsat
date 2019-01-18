source persistent-data/config/station.config
python radio/scheduler/data/predict.py persistent-data/config/elements/ | grep "$1"
