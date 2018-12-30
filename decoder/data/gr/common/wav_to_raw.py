#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Wav To Raw
# Generated: Sun Dec 30 01:49:21 2018
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import gr, blocks
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
from os.path import splitext
from range_selector import range_selector  # grc-generated hier_block
import ConfigParser


class wav_to_raw(gr.top_block):

    def __init__(self, skip=0, keep=0, filename=""):
        gr.top_block.__init__(self, "Wav To Raw")

        ##################################################
        # Parameters
        ##################################################
        self.skip = skip
        self.keep = keep
        self.filename = filename

        ##################################################
        # Variables
        ##################################################
        self._meta_samp_rate_config = ConfigParser.ConfigParser()
        self._meta_samp_rate_config.read(filename)
        try: meta_samp_rate = self._meta_samp_rate_config.getfloat("main", "samp_rate")
        except: meta_samp_rate = 0
        self.meta_samp_rate = meta_samp_rate
        self.filename_base = filename_base = splitext(filename)[0]

        ##################################################
        # Blocks
        ##################################################
        self.range_selector_0 = range_selector(
            keep=0,
            samp_rate=0,
            skip=0,
        )
        self.blocks_wavfile_source_0 = blocks.wavfile_source(filename_base + ".wav", False)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, filename_base + ".c.raw", meta_samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, "", False)
        self.blocks_file_meta_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.range_selector_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_0, 1))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.range_selector_0, 0), (self.blocks_file_meta_sink_0, 0))    

    def get_skip(self):
        return self.skip

    def set_skip(self, skip):
        self.skip = skip

    def get_keep(self):
        return self.keep

    def set_keep(self, keep):
        self.keep = keep

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.set_filename_base(splitext(self.filename)[0])
        self._meta_samp_rate_config = ConfigParser.ConfigParser()
        self._meta_samp_rate_config.read(self.filename)
        if not self._meta_samp_rate_config.has_section("main"):
        	self._meta_samp_rate_config.add_section("main")
        self._meta_samp_rate_config.set("main", "samp_rate", str(None))
        self._meta_samp_rate_config.write(open(self.filename, 'w'))

    def get_meta_samp_rate(self):
        return self.meta_samp_rate

    def set_meta_samp_rate(self, meta_samp_rate):
        self.meta_samp_rate = meta_samp_rate

    def get_filename_base(self):
        return self.filename_base

    def set_filename_base(self, filename_base):
        self.filename_base = filename_base
        self.blocks_file_meta_sink_0.open(self.filename_base + ".c.raw")


def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "-s", "--skip", dest="skip", type="intx", default=0,
        help="Set skip [default=%default]")
    parser.add_option(
        "-k", "--keep", dest="keep", type="intx", default=0,
        help="Set keep [default=%default]")
    parser.add_option(
        "-f", "--filename", dest="filename", type="string", default="",
        help="Set filename [default=%default]")
    return parser


def main(top_block_cls=wav_to_raw, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(skip=options.skip, keep=options.keep, filename=options.filename)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
