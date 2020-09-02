#!/usr/bin/env python3

# Usage: server.py [path to data directory]

from tornado.web import RequestHandler, StaticFileHandler
from bokeh.server.server import Server
from bokeh.util.logconfig import basicConfig

from functools import partial
from sys import argv
from os.path import isdir, join, dirname, basename, splitext, getsize
from glob import glob
from configparser import ConfigParser
from datetime import datetime
import re

from utils import dotdict

from waterfall import create_doc
from polar_plot import PolarPlot

## Options
address = '0.0.0.0'


class Observation:
    def __init__(self, file):
        self.file = basename(file)
        self.object = None
        self.time = None
        self.duration = None
        self.location = None
        if file.endswith(".meta"):
            try:
                self.file_basename = splitext(file)[0]
                config = ConfigParser()
                config.read(file)

                self.raw_file = self.file_basename + ".raw"
                try:
                    self.size = getsize(self.raw_file)
                except:
                    self.size = None
                self.samp_rate = int(config['main']['samp_rate'])
                self.freq = float(config['main']['freq'])
                self.time = datetime.fromtimestamp(float(config['main']['time']))
                self.duration = self.size / (self.samp_rate * 8) if self.size else None
                self.tle = config['tle']['tle'].split(",")
                self.object = self.tle[0].strip()
                try:
                    self.position = {k:float(v) for k,v in config['position'].items()}
                except:
                    pass
            except Exception as e:
                print(self.file, e)

    def polar_plot(self):
        return PolarPlot(tle=self.tle, location=self.position, start_time=self.time, duration=self.duration)

    def __repr__(self):
        if self.time:
            return self.time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return self.file


class MainHandler(RequestHandler):
    def get(self):

        file_list = [glob(join(data_dir, pattern)) for pattern in ['*.meta', '*.raw', '*.wav']]
        file_list = sum(file_list, [])  # flatten list
        file_list = sorted(file_list)   # sort list
        if not self.get_query_argument("f_all", None):
            file_list = [file for file in file_list if (not file.endswith(".raw")) or (file.endswith(".raw") and "{}.meta".format(splitext(file)[0]) not in file_list)]

        observations = [Observation(file) for file in file_list]
        sat_list = set(map(lambda o: o.object, observations))

        sat_filter = self.get_query_argument("filter", "")
        if sat_filter != "None":
            pattern = re.compile("^{}".format(sat_filter or ".*"))
            observations = list(filter(lambda o: pattern.match(o.object or ""), observations))
        else:
            observations = list(filter(lambda o: not o.object, observations))

        sort_down = False if self.get_query_argument("down", "1") == "0" else True
        sort_map = {"s": "object", "t": "time", "d": "duration"}
        sort_default = {"s": "", "t": datetime.fromtimestamp(0), "d": 0}
        sort_key = self.get_query_argument("sort", "t")
        if sort_key not in sort_map:
            sort_key = "s"

        observations = list(sorted(observations, key=lambda o: getattr(o, sort_map[sort_key]) or sort_default[sort_key], reverse=sort_down))

        self.render("observations.html",
                    observations=observations,
                    sat_filter=sat_filter,
                    sat_list=sat_list,
                    sort=dotdict(key=sort_key, down=sort_down, options=[("s", "Satellite"), ("t", "Time"), ("d", "Duration")]),
                    url=self.request.uri
                    )


class PolarPlotHandler(RequestHandler):
    def prepare(self):
        self.set_header("Content-Type", "image/svg+xml")

    def get(self):
        file = self.get_query_argument("file", None)
        if not file:
            raise Exception("no file set")

        if not file.endswith(".meta"):
            raise Exception("unsupported file type")

        file = basename(file)
        observation = Observation(join(data_dir, file))

        self.finish(observation.polar_plot().generate_svg())


if len(argv) >= 2:
    if isdir(argv[1]):
        data_dir = argv[1]
    else:
        raise RuntimeError("Directory {} not found.".format(argv[1]))
else:
    data_dir = '.'

basicConfig(level="warn")

server = Server(
    address=address, allow_websocket_origin=['*'], num_procs=1,
    applications={'/waterfall': partial(create_doc, data_dir=data_dir)}, extra_patterns=[
        ('/', MainHandler),
        ('/polar_plot/', PolarPlotHandler),
        # /static route is already used by bokeh server
        ('/static_2/(.*)', StaticFileHandler, dict(path=join(dirname(__file__), "static"))),
        ('/data/(.*)', StaticFileHandler, dict(path=data_dir))])
server.start()

if __name__ == '__main__':
    print('Running at http://{}:5006/'.format(address))    
    server.io_loop.start()
