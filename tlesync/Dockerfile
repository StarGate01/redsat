FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=Europe/Berlin

# Package dependencies

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install wget

# Entrypoint

COPY run.sh /app/
RUN chmod +x /app/run.sh
WORKDIR /app
CMD ["/app/run.sh"]