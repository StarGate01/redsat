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

## Configuration
Edit ```persistent-data/TLE/station.config``` to configure your groundstation.

Edit ```persistent-data/TLE/sats.list``` and ```persistent-data/TLE/sources.list``` to configure satellites and TLE sources.

## Setup
Run ```docker-compose up tlesync``` to pull fresh TLE data from the internet.

Run ```docker-compose build``` to build and ```docker-compose up -d``` to run the full stack.

## Containers and their sources
- Radio
    - gnuradio: Base image for radio related software, builds gnuradio from source.
        - [GNU Radio](https://www.gnuradio.org/)
        - [Boost](https://www.boost.org/)
    - receiver: Receives a signal from a SDR device or an audio interface (useful for piping a stream across system boundaries) and saves it to a file, along with TLE and geodata.
        - [osmocom GNU Radio Blocks](https://osmocom.org/projects/gr-osmosdr/wiki)
        - [Gpredict Doppler GNU Radio Blocks](https://github.com/wnagele/gr-gpredict-doppler)
        - [rtl-sdr](https://git.osmocom.org/rtl-sdr)
        - [rtl-mus](https://github.com/simonyiszk/rtl_mus)
    - decoder: Decodes a saved signal into usable data (weather maps or telemetry dumps)
        - [SatNOGS GNU Radio Blocks](https://gitlab.com/librespacefoundation/satnogs)
        - [libFEC](https://github.com/quiet/libfec)
        - [TUM WARR](https://www.warr.de/de/) closed source assets
    - scheduler:
        - [PyEphem](https://rhodesmill.org/pyephem/)
    - tlesync: Loads the newest TLEs from the internet
        - [Celestrak NORAD](https://www.celestrak.com)
- Frontend
    - [nginx](https://www.nginx.com/): Front-facing reverse proxy
    - [apache](https://httpd.apache.org/): Front-facing web server
    - [portainer](https://www.portainer.io/): Internal docker monitoring
