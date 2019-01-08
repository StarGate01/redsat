FROM radio_gnuradio:latest

# Package dependencies

RUN apt-get -y update
RUN apt-get -y install automake libtool wget

# Library dependencies

WORKDIR /app/deps/rtl-sdr
RUN git clone https://git.osmocom.org/rtl-sdr
WORKDIR /app/deps/rtl-sdr/rtl-sdr
RUN git checkout 0.6.0
RUN git reset --hard
WORKDIR /app/deps/rtl-sdr/rtl-sdr/build
RUN cmake ..
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

WORKDIR /app/deps/rtl_mus
RUN git clone https://github.com/simonyiszk/rtl_mus
WORKDIR /app/deps/rtl_mus/rtl_mus
RUN git checkout 13c3ea1defa5ed74255414374c5ffff2ff136df8
RUN git reset --hard

WORKDIR /app/deps/fftw3
RUN wget http://fftw.org/fftw-3.3.8.tar.gz
RUN tar -xzvf fftw-3.3.8.tar.gz
WORKDIR /app/deps/fftw3/fftw-3.3.8
RUN ./configure --enable-shared
RUN make
RUN make install


WORKDIR /app/deps/kalibrate-rtl
RUN git clone https://github.com/steve-m/kalibrate-rtl.git
WORKDIR /app/deps/kalibrate-rtl/kalibrate-rtl
RUN git checkout aae11c8a8dc79692a94ccfee39ba01e8c8c05d38
RUN git reset --hard
RUN ./bootstrap
RUN ./configure
RUN make
RUN make install

RUN ldconfig

# GNURadio flowcharts

COPY common/data/gr/ /app/gr-common/
COPY receiver/data/gr/ /app/gr/

# Compile flowcharts

COPY common/scripts/compile_grc.sh /tmp/
RUN chmod +x /tmp/compile_grc.sh
RUN /tmp/compile_grc.sh /app/gr-common
RUN /tmp/compile_grc.sh /app/gr

# Entrypoint

COPY receiver/run.sh /app/
RUN chmod +x /app/run.sh
WORKDIR /app
CMD ["/app/run.sh"]
