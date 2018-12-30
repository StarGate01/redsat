#!/usr/bin/env python2

import ephem
import socket
import sys
from contextlib import contextmanager

from datetime import datetime
from os import chdir
from os.path import dirname, abspath

C = 299792458.
F0 = 145.95e6 #30.0e6

LATITUDE  = '48.27102185402348'    # changeme (degrees)
LONGITUDE = '11.589301402282672'   # changeme (degrees)
ALTITUDE  = 0                    # changeme (meters)

TLE_DATA = "MOVE-II;1 43774U 18099S   18340.66044376  .00001644  00000-0  15648-3 0  9996;2 43774  97.7715  49.7845 0011035 250.7436 273.4950 14.94768966   423;".split(";")

myloc = ephem.Observer()
myloc.lon = LONGITUDE
myloc.lat = LATITUDE
myloc.elevation = ALTITUDE

mysat = ephem.readtle(TLE_DATA[0], TLE_DATA[1], TLE_DATA[2])

start_time = 1545855703.0

def dopplercalc(offset):
    t = datetime.utcfromtimestamp(start_time + offset).strftime('%Y-%m-%d %H:%M:%S.%f')
    myloc.date = t
    print(t, myloc.date, type(myloc.date))
    mysat.compute(myloc)
    doppler = int(F0 - mysat.range_velocity * F0 / C)
    return doppler

doppler = dopplercalc(0)
for i in range(0,1000,1):
    new_doppler = dopplercalc(float(i)/1000.)
    if new_doppler != doppler:
        print(gmtime(start_time + i), i , new_doppler)
        
