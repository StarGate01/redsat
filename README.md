# REDSAT
Raspberry Pi satellite SDR base station for weather &amp; telemetry.

## Supported satellites
- [NOAA](https://www.ospo.noaa.gov/Operations/POES/status.html)
    - NOAA-15
    - NOAA-18
    - NOAA-19
- [Roscosmos](https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=2014-037A)
    - METEOR-M 2
- [TUM](https://www.move2space.de/MOVE-II/)
    - MOVE-II

## Setup
Run ```docker-compose up tlesync``` to pull fresh TLE data from the internet.

Run ```docker-compose build``` to build and ```docker-compose up -d``` to run the full stack.

## Containers
- Radio
    - gnuradio: Base image for radio related software, builds gnuradio from source.
    - receiver: Receives a signal from a SDR device and saves it to a file, along with TLE and geodata.
    - decoder: Decodes a saved signal into usable data (weather maps or telemetry dumps)
    - tlesync: Loads the newest TLEs from the internet
- Frontend
    - nginx: Front-facing reverse proxy
    - apache: Front-facing web server
    - portainer: Internal docker monitoring
