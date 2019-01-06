#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import os
import ephem
import math
import datetime
from time import gmtime, strftime

nowdate = strftime('%Y/%m/%d %H:%M:%S', gmtime())

myloc = ephem.Observer()
myloc.lon = os.environ['LON']
myloc.lat = os.environ['LAT']
myloc.elevation = int(os.environ['ELV'])

for subdir, dirs, files in os.walk('/app/config/elements'):
    for file in files:
        print file
        with open(os.path.join(subdir, file), 'r') as f:
            data = f.readlines()
            mysat = ephem.readtle(data[0], data[1], data[2])

            myloc.date = nowdate
            for i in range(3):
                start_time, aos_az, mid_time, max_elv, end_time, los_az = myloc.next_pass(mysat)
                print "%s - %s - %s" % (start_time, mid_time, end_time)
                print "  AOS Az: %4.2f° LOS Az: %4.2f° Max Elv: %4.2f°" % \
                    (math.degrees(aos_az), math.degrees(los_az), math.degrees(max_elv))
                myloc.date = end_time + ephem.minute
            print
