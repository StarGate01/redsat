FROM radio_gnuradio:latest

# GNURadio flowcharts

COPY data/gr/ /app/gr/

# Entrypoint

COPY run.sh /app/
RUN chmod +x /app/run.sh
WORKDIR /app
CMD ["/app/run.sh"]