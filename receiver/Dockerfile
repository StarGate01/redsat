FROM redsat_gnuradio:latest

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

WORKDIR /app/deps/rtl_mus
RUN git clone https://github.com/simonyiszk/rtl_mus
WORKDIR /app/deps/rtl_mus/rtl_mus
RUN git checkout 13c3ea1defa5ed74255414374c5ffff2ff136df8
RUN git reset --hard

RUN ldconfig

# GNURadio flowcharts

COPY data/gr/ /app/gr/

# Entrypoint

COPY run.sh /app/
RUN chmod +x /app/run.sh
WORKDIR /app
CMD ["/app/run.sh"]