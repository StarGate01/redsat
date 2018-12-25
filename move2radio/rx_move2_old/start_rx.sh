DIR=$(pwd)

# change into the folder where the data files should be stored
cd ../../../../persistent-data/move2radio/input/

# Print date to verify it set correctly
date
# Start dopplerscript as soon as first UDP packet arrives. This indicates that GNURadio is running.
socat -u udp-recvfrom:12345,reuseaddr system:"python $DIR/dopplerscript/doppler.py" & 
# Start GNURadio
python $DIR/rx_move2.py

