#!/usr/bin/env python3

# Usage: server.py [path to data directory]

from tornado.web import RequestHandler 
from bokeh.server.server import Server
from functools import partial
from sys import argv
from os.path import isdir, join, basename
from glob import glob

from waterfall import create_doc

## Options
address = '0.0.0.0'

class MainHandler(RequestHandler):
    def get(self):
        file_list = [glob(join(data_dir, pattern)) for pattern in ['*.meta', '*.raw', '*.raw2']]
        file_list = sum(file_list, []) # flatten list
        self.render("list.html", title="Recordings", items=map(basename, file_list))

if len(argv) >= 2:
    if isdir(argv[1]):
        data_dir = argv[1]
    else:
        raise Error("Directory not found.")
else:
    data_dir = '.'
                 
server = Server(
    address=address, num_procs=1,
    applications={'/waterfall': partial(create_doc, data_dir=data_dir)}, extra_patterns=[('/', MainHandler)])
server.start()

if __name__ == '__main__':
    print('Running at http://{}:5006/'.format(address))    
    server.io_loop.start()