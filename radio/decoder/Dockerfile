FROM radio_gnuradio:latest

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

COPY decoder/data/nonfree/AR4JA_r12_k1024n.a /tmp/
COPY decoder/data/nonfree/lib/* /usr/local/lib/
COPY decoder/data/nonfree/ccsds/* /usr/local/lib/python2.7/dist-packages/ccsds/
COPY decoder/data/nonfree/blocks/* /usr/local/share/gnuradio/grc/blocks/
RUN ldconfig

# GNURadio flowcharts

COPY common/data/gr/ /app/gr-common/
COPY decoder/data/gr/ /app/gr/

# Compile flowcharts

COPY common/scripts/compile_grc.sh /tmp/
RUN chmod +x /tmp/compile_grc.sh
RUN /tmp/compile_grc.sh /app/gr-common
RUN /tmp/compile_grc.sh /app/gr

# COPY decoder/data/ /app/data-temp/

# Fake MOVEII server (local blackhole)

COPY decoder/data/fakeserver/ /app/fakeserver/

# Entrypoint

COPY decoder/run.sh /app/
RUN chmod +x /app/run.sh
WORKDIR /app
CMD ["/app/run.sh"]