#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv
import os
from skyfield.api import load, Topos, EarthSatellite
import math
from time import gmtime, localtime, strftime, strptime
import datetime
from calendar import timegm
import argparse

parser = argparse.ArgumentParser(description='Predicts next satellite overpasses.')
parser.add_argument('--path', type=str, default="/app/config/elements", help='Path to TLE directory')
parser.add_argument('--local', dest='local', action='store_const', const=True, default=False, help='Show local times')
args = parser.parse_args()


ts = load.timescale()
dt_now = datetime.datetime.now(datetime.timezone.utc)
t0 = ts.from_datetime(dt_now)
t1 = ts.from_datetime(dt_now + datetime.timedelta(days=1))

ts_now = dt_now.timestamp()

loc = Topos(latitude_degrees=float(os.environ['LAT']), longitude_degrees=float(os.environ['LON']), elevation_m=int(os.environ['ELV']))
#print("loc:", loc)

fmt_date = lambda ts: strftime("%Y/%m/%d %H:%M:%S", localtime(ts) if args.local else gmtime(ts)) if ts else "."

for subdir, dirs, files in os.walk(args.path):
    for file in files:
        with open(os.path.join(subdir, file), 'r') as f:
            data = f.readlines()
            if len(data) < 3:
                print("warning: TLE file {} does not contain three lines and will not be used for prediction".format(file))
                continue

            name = data[0].strip().replace(' ','')

            sat = EarthSatellite(data[1], data[2], name, ts)
            diff = sat - loc
            #print("sat:", sat)

            overpasses = {None:{}}
            current = None
            t, events = sat.find_events(loc, t0, t1)
            for ti, event in zip(t, events):
                _ts = ti.utc_datetime().timestamp()
                alt, az, distance = diff.at(ti).altaz()
                pos = dict(alt=alt.degrees, az=az.degrees)
                if event == 0:
                    current = _ts
                    overpasses[_ts] = {}

                overpasses[current][event] = _ts, pos

            for start_ts in sorted(overpasses.keys(), key=lambda x: x if x else 0):
                o = overpasses[start_ts]

                mid_ts, mid_pos = o[1] if 1 in o else (None, None)
                end_ts, end_pos = o[2] if 2 in o else (None, None)

                if end_ts is None:
                   continue

                if start_ts is None:
                    start_ts = ts_now
                    alt, az, distance = diff.at(t0).altaz()
                    start_pos = dict(alt=alt.degrees, az=az.degrees)
                else:
                    start_pos = o[0][1]

                duration = end_ts - start_ts
                print("%s %d %d \n | %s - %s - %s" % (name.strip().replace(' ',''), start_ts, duration, fmt_date(start_ts), fmt_date(mid_ts), fmt_date(end_ts)))
                fmt_angle = lambda v: "{:5.1f}°".format(v) if v else "?°"
                print("   AOS Az: {} LOS Az: {} Max Elv: {}".format(
                    fmt_angle(start_pos["az"]),
                    fmt_angle(end_pos["az"]),
                    fmt_angle(mid_pos["alt"] if mid_pos else None)))
