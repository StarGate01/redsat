FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=Europe/Berlin

# Package dependencies

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install git wget cmake build-essential g++ pkg-config doxygen \
    python-dev swig python-wxgtk3.0 python-numpy python-cheetah python-lxml \
    python-sip python-sip-dev python-qt4 python-sphinx python-gtk2 python-mako \
    libfftw3-dev libcppunit-dev libgsl-dev libusb-dev libsdl1.2-dev \
    libxi-dev libqt4-opengl-dev libqwt-dev libfontconfig1-dev libxrender-dev \
    libusb-1.0-0-dev libcomedi-dev libzmq3-dev \
    libcurl4-openssl-dev libcurlpp-dev pulseaudio alsa-base alsa-utils \
    libogg-dev libvorbis-dev libpng-dev libpng++-dev swig gnuplot-qt socat python-pip

RUN pip install pyephem
    
# Library dependencies

WORKDIR /app/deps/boost
RUN wget -q https://dl.bintray.com/boostorg/release/1.67.0/source/boost_1_67_0.tar.gz
RUN tar -xzf boost_1_67_0.tar.gz
WORKDIR /app/deps/boost/boost_1_67_0
RUN ./bootstrap.sh --exec-prefix=/usr/local
RUN ./b2
RUN ./b2 install

# GNURadio

WORKDIR /app/deps/gnuradio
RUN git clone --recursive https://github.com/gnuradio/gnuradio.git
WORKDIR /app/deps/gnuradio/gnuradio
RUN git checkout v3.7.13.4
RUN git reset --hard
WORKDIR /app/deps/gnuradio/gnuradio/build
RUN cmake -DENABLE_DOXYGEN=0 ..
RUN make
RUN make install

# GNURadio Plugins

WORKDIR /app/deps/gr-osmosdr
RUN git clone https://github.com/osmocom/gr-osmosdr
WORKDIR /app/deps/gr-osmosdr/gr-osmosdr
RUN git checkout v0.1.4
RUN git reset --hard
WORKDIR /app/deps/gr-osmosdr/gr-osmosdr/build
RUN cmake ..
RUN make
RUN make install

WORKDIR /app/deps/gr-satnogs
RUN git clone https://gitlab.com/librespacefoundation/satnogs/gr-satnogs
WORKDIR /app/deps/gr-satnogs/gr-satnogs
RUN git checkout v1.5
RUN git reset --hard
WORKDIR /app/deps/gr-satnogs/gr-satnogs/build
RUN cmake ..
RUN make
RUN make install

WORKDIR /app/deps/gr-gpredict-doppler
RUN git clone https://github.com/wnagele/gr-gpredict-doppler
WORKDIR /app/deps/gr-gpredict-doppler/gr-gpredict-doppler
RUN git checkout 8392f6442fd1fbeb307a315474c83688f29817a7
RUN git reset --hard
WORKDIR /app/deps/gr-gpredict-doppler/gr-gpredict-doppler/build
RUN cmake ..
RUN make
RUN make install

# Audio

COPY gnuradio/data/.asoundrc /home/root/.asoundrc

RUN ldconfig