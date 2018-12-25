# change into the folder where the data files should be stored
cd /app/input/

# Print date to verify it set correctly
date
# Start dopplerscript as soon as first UDP packet arrives. This indicates that GNURadio is running.
socat -u udp-recvfrom:12345,reuseaddr system:"python /app/scripts/dopplerscript/doppler.py" & 
# Start GNURadio
python /app/gr/rx_move2/rx_move2.py

