#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from skyfield.api import load, Topos, EarthSatellite
from time import gmtime, localtime, strftime
import datetime
import re

loc = Topos(latitude_degrees=float(os.environ['LAT']),
            longitude_degrees=float(os.environ['LON']),
            elevation_m=int(os.environ['ELV']))
ts = load.timescale()


TLE_path = ""

class TLE():
    def __init__(self, filename=None, sat_name=None):
        if (filename is None) == (sat_name is None):
            raise ValueError()

        if sat_name:
            filename = "{}.txt".format(sat_name)

        filename = os.path.join(TLE_path, filename)
        with open(filename, 'r') as f:
            lines = f.readlines()
            if len(lines) != 3:
                raise ValueError("TLE file {} does not contain three lines".format(filename))

        self._tle = lines
        self._sat = EarthSatellite(self._tle[1], self._tle[2], self.get_name(), ts)
        self._diff = self._sat - loc

    def get_name(self):
        return self._tle[0].strip()

    def get_sat(self):
        return self._sat

    def get_diff(self):
        return self._diff


def get_overpass_id(tle, mid_ts):
    """
    Unique identifier of an satellite overpass. Identification string contains the satellite name,
    UTC date of the overpass in the format "yyyymmdd" and a number indicating the recurrence on the respective day.
    Note: The identifier does not respect the location of the observer.
    """
    mid_dt = datetime.datetime.utcfromtimestamp(mid_ts)
    t0_dt = datetime.datetime(year=mid_dt.year, month=mid_dt.month, day=mid_dt.day, tzinfo=datetime.timezone.utc)
    t1_dt = t0_dt + datetime.timedelta(days=1)

    t, events = tle.get_sat().find_events(loc, ts.from_datetime(t0_dt), ts.from_datetime(t1_dt))
    mid_ts_list = [abs(ti.utc_datetime().timestamp() - mid_ts) for ti, event in zip(t, events) if event == 1]
    return "{}:{}{:02d}{:02d}:{}".format(
        tle.get_name(),
        mid_dt.year, mid_dt.month, mid_dt.day,
        mid_ts_list.index(min(mid_ts_list))
    )


def get_position(tle, ti):
   alt, az, distance = tle.get_diff().at(ti).altaz()
   pos = dict(alt=alt.degrees, az=az.degrees, distance=distance.km)
   return pos


def get_overpasses(tle, t_range, backsearch=3600*2):
    """
    Returns dict of overpasses for a satellite in the time window t_range.
    Example: {
        'rise timestamp': [
            ('rise timestamp','position')
            ('max eleveation timestamp', 'position')
            ('set timestamp', 'position')
        ]
    The position is described by a dict containing the altitude (alt), azimuth (az) in degrees and distance in kilometers.
    """

    overpasses = {None: {}}
    current = None
    t, events = tle.get_sat().find_events(loc, *t_range)
    for ti, event in zip(t, events):
        _ts = ti.utc_datetime().timestamp()
        pos = get_position(tle, ti)
        if event == 0:
            current = _ts
            overpasses[_ts] = {}

        overpasses[current][event] = _ts, pos

    # if there is an ongoing overpass, it is necessary to look in the past to find the missing events:
    # TODO: maybe there is a more efficient way to narrow down the time window
    if len(overpasses[None]):
       t0_p = t_range[0].utc_datetime() - datetime.timedelta(seconds=backsearch)
       #print("missing events:", t0_p, t_range[0].utc_datetime())

       t0_p = ts.from_datetime(t0_p)
       # find events between t0_p and t0, iterate in reversed order:
       for ti, event in reversed(list(zip(*tle.get_sat().find_events(loc, t0_p, t_range[0])))):
           #print("missing event:", ti.utc_datetime(), event)
           _ts = ti.utc_datetime().timestamp()
           pos = get_position(tle, ti)
           overpasses[None][event] = _ts, pos
           if event == 0:
               overpasses[events[None][0][0]] = overpasses[None]
               del overpasses[None]
               break

    return overpasses


def get_overpasses_24h(tle):
    """
    Returns the overpasses in the next 24 hours and the skyfield time objects.
    """

    dt_now = datetime.datetime.now(datetime.timezone.utc)
    t0 = ts.from_datetime(dt_now)
    t1 = ts.from_datetime(dt_now + datetime.timedelta(days=1))

    return get_overpasses(tle, (t0, t1))



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Predicts next satellite overpasses.')
    parser.add_argument('--path', type=str, default="/app/config/elements", help='Path to TLE directory')
    parser.add_argument('--sat', type=str, default=".*", help="Filters satellites by regex")
    parser.add_argument('-t', type=str, default=None, help='Time in format %Y-%m-%d %H:%M:%S')
    parser.add_argument('-w', type=str, default="1d", help='Time window in format <int>d<int>h<int>m<int>s')
    parser.add_argument('--local', dest='local', action='store_const', const=True, default=False, help='Show local times')
    args = parser.parse_args()

    def parse_timedelta(value):
        regex = re.compile(r'^((?P<days>[\.\d]+?)d)?((?P<hours>[\.\d]+?)h)?((?P<minutes>[\.\d]+?)m)?((?P<seconds>[\.\d]+?)s)?$')
        parts = regex.match(value)
        assert parts is not None, "Failed to parse timedelta".format(value)
        return datetime.timedelta(**{name: float(param) for name, param in parts.groupdict().items() if param})

    TLE_path = args.path

    fmt_date = lambda ts: strftime("%Y-%m-%d %H:%M:%S", localtime(ts) if args.local else gmtime(ts)) if ts else "."
    fmt_angle = lambda d,k: "{:5.1f}°".format(d[k]) if d else "?°"

    sat_pattern = re.compile("^{}$".format(args.sat))

    for file in os.listdir(args.path):
        try:
            tle = TLE(filename=file)
        except Exception as e:
            print("warning: TLE file {} cannot be loaded and will not be used for prediction: {}".format(file, e))
            continue

        if not sat_pattern.match(tle.get_name()):
           continue

        #overpasses = get_overpasses_24h(tle)
        if args.t:
            _t = datetime.datetime.strptime(args.t, '%Y-%m-%d %H:%M:%S')
            if args.local:
                _t = datetime.datetime.utcfromtimestamp(_t.timestamp()) 
            dt_t = _t.replace(tzinfo=datetime.timezone.utc)
        else:
            dt_t = datetime.datetime.now(datetime.timezone.utc)

        if args.w:
            dt_d = parse_timedelta(args.w)
        else:
            dt_d = datetime.timedelta(days=1)

        t0 = ts.from_datetime(dt_t)
        t1 = ts.from_datetime(dt_t + dt_d)

        overpasses = get_overpasses(tle, (t0, t1))

        for start_ts in sorted(overpasses.keys(), key=lambda x: x if x else 0):
            o = overpasses[start_ts]

            mid_ts, mid_pos = o[1] if 1 in o else (None, None)
            end_ts, end_pos = o[2] if 2 in o else (None, None)

            if end_ts is None:
                continue

            if start_ts is None:
                start_ts, start_pos = None, None
            else:
                start_ts, start_pos = o[0]

            if start_ts and end_ts:
                duration = end_ts - start_ts
            else:
                duration = None

            fmt_int = lambda v: str(int(round(v))) if v else "-"
            print("{name} {start} {duration} {id}".format(
                name=tle.get_name(), start=fmt_int(start_ts), duration=fmt_int(duration), id=get_overpass_id(tle, mid_ts) if mid_ts else '-'
            ))
            print("  | {} - {} - {}".format(
                fmt_date(start_ts), fmt_date(mid_ts), fmt_date(end_ts)
            ))
            print("  | AOS Az: {} LOS Az: {} TCA Alt: {} Az: {}".format(
                fmt_angle(start_pos, "az"),
                fmt_angle(end_pos, "az"),
                fmt_angle(mid_pos, "alt"),
                fmt_angle(mid_pos, "az")
            ))
        print("")
