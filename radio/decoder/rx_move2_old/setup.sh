sudo apt-get install libogg-dev libvorbis-dev libpng-dev libpng++-dev swig gnuplot-qt socat
# ? python-pip

git clone https://gitlab.com/librespacefoundation/satnogs/gr-satnogs.git
cd gr-satnogs
mkdir build
cmake ..
make
sudo make install
sudo ldconfig
cd ../..

git clone https://github.com/wnagele/gr-gpredict-doppler.git
cd gr-gpredict-doppler
mkdir build
cd build
cmake ../
make
sudo make install
cd ../..

pip install pyephem