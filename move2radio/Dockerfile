FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=Europe/Berlin

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install git wget cmake build-essential g++ pkg-config doxygen \
    python-dev swig python-wxgtk3.0 python-numpy python-cheetah python-lxml \
    python-sip python-sip-dev python-qt4 python-sphinx python-gtk2 python-mako \
    libfftw3-dev libcppunit-dev libgsl-dev libusb-dev libsdl1.2-dev \
    libxi-dev libqt4-opengl-dev libqwt-dev libfontconfig1-dev libxrender-dev \
    libusb-1.0-0-dev libcomedi-dev libzmq3-dev
    
WORKDIR /app/deps/boost
RUN wget -q https://dl.bintray.com/boostorg/release/1.67.0/source/boost_1_67_0.tar.gz
RUN tar -xzf boost_1_67_0.tar.gz
WORKDIR /app/deps/boost/boost_1_67_0
RUN ./bootstrap.sh --exec-prefix=/usr/local
RUN ./b2
RUN ./b2 install

WORKDIR /app/deps/gnuradio
RUN git clone --recursive https://github.com/gnuradio/gnuradio.git
WORKDIR /app/deps/gnuradio/gnuradio
RUN git checkout v3.7.13.4
RUN git reset --hard
WORKDIR /app/deps/gnuradio/gnuradio/build
RUN cmake -DENABLE_DOXYGEN=0 ..
RUN make
RUN make install

WORKDIR /app/deps/gr-osmosdr
RUN git clone https://github.com/osmocom/gr-osmosdr
WORKDIR /app/deps/gr-osmosdr/gr-osmosdr
RUN git checkout v0.1.4
RUN git reset --hard
WORKDIR /app/deps/gr-osmosdr/gr-osmosdr/build
RUN cmake ..
RUN make
RUN make install

WORKDIR /app/deps/libfec
RUN git clone https://github.com/quiet/libfec
WORKDIR /app/deps/libfec/libfec
RUN git checkout 9750ca0a6d0a786b506e44692776b541f90daa91
RUN git reset --hard
RUN ./configure
RUN make
RUN make install

RUN apt-get -y install libcurl4-openssl-dev libcurlpp-dev

COPY data/move-ii-gr/file_gui/* /app/move-ii-gr/file_gui/
COPY data/move-ii-gr/file_nogui/* /app/move-ii-gr/file_nogui/
COPY data/move-ii-gr/tcp_gui/* /app/move-ii-gr/tcp_gui/
COPY data/move-ii-gr/tcp_nogui/* /app/move-ii-gr/tcp_nogui/

COPY data/AR4JA_r12_k1024n.a /tmp/
COPY data/lib/* /usr/local/lib/
COPY data/ccsds/* /usr/local/lib/python2.7/dist-packages/ccsds/
COPY data/blocks/* /usr/local/share/gnuradio/grc/blocks/

RUN ldconfig

COPY run.sh /app/
RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]