FROM radio_gnuradio:latest

# GNURadio flowcharts

COPY common/data/gr/ /app/gr-common/
COPY decoder/data/gr/ /app/gr/

# Compile flowcharts

COPY common/scripts/compile_grc.sh /tmp/
RUN chmod +x /tmp/compile_grc.sh
RUN /tmp/compile_grc.sh /app/gr-common
RUN /tmp/compile_grc.sh /app/gr

# Entrypoint

COPY importer/run.sh /app/
RUN chmod +x /app/run.sh
WORKDIR /app
CMD ["/app/run.sh"]