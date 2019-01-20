#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sys import argv
import os
import ephem
import math
from time import gmtime, localtime, strftime, strptime
from calendar import timegm
import argparse

parser = argparse.ArgumentParser(description='Predicts next satellite overpasses.')
parser.add_argument('--path', type=str, default="/app/config/eleme", help='Path to TLE directory')
parser.add_argument('--local', dest='local', action='store_const', const=True, default=False, help='Show local times')
args = parser.parse_args()

nowdate = strftime('%Y/%m/%d %H:%M:%S', gmtime())

myloc = ephem.Observer()
myloc.lon = os.environ['LON']
myloc.lat = os.environ['LAT']
myloc.elevation = int(os.environ['ELV'])

fmt_date = lambda ts: strftime("%Y/%m/%d %H:%M:%S", localtime(ts) if args.local else gmtime(ts))

for subdir, dirs, files in os.walk(args.path):
    for file in files:
#        print file
        with open(os.path.join(subdir, file), 'r') as f:
            data = f.readlines()
            if len(data) < 3:
                print("warning: TLE file {} does not contain three lines and will not be used for prediction".format(file))
                continue

            name = data[0]
            mysat = ephem.readtle(name, data[1], data[2])

            myloc.date = nowdate
            for i in range(3):
                start_time, aos_az, mid_time, max_elv, end_time, los_az = myloc.next_pass(mysat)
		start_ts = timegm(strptime(str(start_time), '%Y/%m/%d %H:%M:%S'))
                mid_ts = timegm(strptime(str(mid_time), '%Y/%m/%d %H:%M:%S'))
                end_ts = timegm(strptime(str(end_time), '%Y/%m/%d %H:%M:%S'))
                duration = end_ts - start_ts
                print "%s, %d, %d \n | %s - %s - %s" % (name.strip(), start_ts, duration, fmt_date(start_ts), fmt_date(mid_ts), fmt_date(end_ts))
                #print mktime(\
                #    datetime.strptime(str(start_time), '%Y/%m/%d %H:%M:%S').timetuple())
	        print "   AOS Az: %4.2f° LOS Az: %4.2f° Max Elv: %4.2f°" % \
                    (math.degrees(aos_az), math.degrees(los_az), math.degrees(max_elv))
                myloc.date = end_time + ephem.minute
            print
