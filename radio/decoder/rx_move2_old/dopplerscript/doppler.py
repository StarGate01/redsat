#!/usr/bin/env python2

import ephem
import socket
import sys
from contextlib import contextmanager
from time import gmtime, strftime
from os import chdir
from os.path import dirname, abspath

C = 300000000.
C = 299792458.
F0 = 145.95e6 #30.0e6

LATITUDE  = '48.27102185402348'    # changeme (degrees)
LONGITUDE = '11.589301402282672'   # changeme (degrees)
ALTITUDE  = 476                    # changeme (meters)
TLEFILE   = './MOVE-II.txt'

chdir(dirname(abspath(__file__)))

@contextmanager
def socketcontext(*args, **kwargs):
    s = socket.socket(*args, **kwargs)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    yield s
    s.close()

with open(TLEFILE, 'r') as f:
    data = f.readlines()

myloc = ephem.Observer()
myloc.lon = LONGITUDE
myloc.lat = LATITUDE
myloc.elevation = ALTITUDE

mysat = ephem.readtle(data[0], data[1], data[2])

def dopplercalc():
    myloc.date = strftime('%Y/%m/%d %H:%M:%S', gmtime())
    mysat.compute(myloc)
    doppler = int(F0 - mysat.range_velocity * F0 / C)
    return doppler

try:
    with socketcontext(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 4532))
        doppler = F0
        while True:
            new_doppler = dopplercalc()
            if new_doppler != doppler:
                s.send('F' + str(new_doppler) + '\n')
            doppler = new_doppler
except socket.error as e:
    print(e)
    sys.exit()
