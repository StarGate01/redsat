FROM redsat_gnuradio:latest

# Library dependencies

WORKDIR /app/deps/libfec
RUN git clone https://github.com/quiet/libfec
WORKDIR /app/deps/libfec/libfec
RUN git checkout 9750ca0a6d0a786b506e44692776b541f90daa91
RUN git reset --hard
RUN ./configure
RUN make
RUN make install

# Nonfree blobs

COPY data/nonfree/AR4JA_r12_k1024n.a /tmp/
COPY data/nonfree/lib/* /usr/local/lib/
COPY data/nonfree/ccsds/* /usr/local/lib/python2.7/dist-packages/ccsds/
COPY data/nonfree/blocks/* /usr/local/share/gnuradio/grc/blocks/
RUN ldconfig

# GNURadio flowcharts and scripts

COPY data/gr/ /app/gr/

COPY data/ /app/data-temp/

# Entrypoint

COPY run.sh /app/
RUN chmod +x /app/run.sh
WORKDIR /app
CMD ["/app/run.sh"]