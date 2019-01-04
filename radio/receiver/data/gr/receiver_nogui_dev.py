#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: REDSAT receiver (device)
# Author: Christoph Honal, Alexander Ulanowski
# Generated: Fri Jan  4 20:44:31 2019
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import gr, blocks
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
from os.path import splitext
import ConfigParser
import SimpleXMLRPCServer
import osmosdr
import sys
import threading
import time
import time_tagger


class receiver_nogui_dev(gr.top_block):

    def __init__(self, config_file='./default.meta', meta_dev='rtl_tcp=10.0.0.219:1234', meta_samp_rate_dev=1536000):
        gr.top_block.__init__(self, "REDSAT receiver (device)")

        ##################################################
        # Parameters
        ##################################################
        self.config_file = config_file
        self.meta_dev = meta_dev
        self.meta_samp_rate_dev = meta_samp_rate_dev

        ##################################################
        # Variables
        ##################################################
        self._meta_samp_rate_config = ConfigParser.ConfigParser()
        self._meta_samp_rate_config.read(config_file)
        try: meta_samp_rate = self._meta_samp_rate_config.getint('main', 'samp_rate')
        except: meta_samp_rate = 128000
        self.meta_samp_rate = meta_samp_rate
        self._meta_gain_config = ConfigParser.ConfigParser()
        self._meta_gain_config.read(config_file)
        try: meta_gain = self._meta_gain_config.getfloat('main', 'gain')
        except: meta_gain = 38
        self.meta_gain = meta_gain
        self.samp_rate = samp_rate = meta_samp_rate
        self._meta_time_config = ConfigParser.ConfigParser()
        self._meta_time_config.read(config_file)
        try: meta_time = self._meta_time_config.getfloat('main', 'time')
        except: meta_time = 0
        self.meta_time = meta_time
        self._meta_output_file_config = ConfigParser.ConfigParser()
        self._meta_output_file_config.read(config_file)
        try: meta_output_file = self._meta_output_file_config.get('main', 'output_file')
        except: meta_output_file = splitext(config_file)[0] + ".raw"
        self.meta_output_file = meta_output_file
        self._meta_freq_config = ConfigParser.ConfigParser()
        self._meta_freq_config.read(config_file)
        try: meta_freq = self._meta_freq_config.getfloat('main', 'freq')
        except: meta_freq = 145950000
        self.meta_freq = meta_freq
        self.gain = gain = meta_gain
        self.bandwidth_rtlsdr = bandwidth_rtlsdr = 100000

        ##################################################
        # Blocks
        ##################################################
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', 8080), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.time_tagger = time_tagger.blk(rate=meta_samp_rate)
        self.src = osmosdr.source( args="numchan=" + str(1) + " " + meta_dev )
        self.src.set_sample_rate(meta_samp_rate_dev)
        self.src.set_center_freq(meta_freq, 0)
        self.src.set_freq_corr(0, 0)
        self.src.set_dc_offset_mode(0, 0)
        self.src.set_iq_balance_mode(1, 0)
        self.src.set_gain_mode(False, 0)
        self.src.set_gain(gain, 0)
        self.src.set_if_gain(20, 0)
        self.src.set_bb_gain(20, 0)
        self.src.set_antenna('', 0)
        self.src.set_bandwidth(bandwidth_rtlsdr, 0)

        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=int(meta_samp_rate_dev/samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_gr_complex*1, '127.0.0.1', 4321, 1472, True)
        self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, meta_output_file, samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, "", False)
        self.blocks_file_meta_sink_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.time_tagger, 0))
        self.connect((self.src, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.time_tagger, 0), (self.blocks_file_meta_sink_0, 0))
        self.connect((self.time_tagger, 0), (self.blocks_udp_sink_0, 0))

    def get_config_file(self):
        return self.config_file

    def set_config_file(self, config_file):
        self.config_file = config_file
        self._meta_samp_rate_config = ConfigParser.ConfigParser()
        self._meta_samp_rate_config.read(self.config_file)
        if not self._meta_samp_rate_config.has_section('main'):
        	self._meta_samp_rate_config.add_section('main')
        self._meta_samp_rate_config.set('main', 'samp_rate', str(None))
        self._meta_samp_rate_config.write(open(self.config_file, 'w'))
        self.set_meta_output_file(splitext(self.config_file)[0] + ".raw")
        self._meta_output_file_config = ConfigParser.ConfigParser()
        self._meta_output_file_config.read(self.config_file)
        if not self._meta_output_file_config.has_section('main'):
        	self._meta_output_file_config.add_section('main')
        self._meta_output_file_config.set('main', 'output_file', str(None))
        self._meta_output_file_config.write(open(self.config_file, 'w'))
        self._meta_freq_config = ConfigParser.ConfigParser()
        self._meta_freq_config.read(self.config_file)
        if not self._meta_freq_config.has_section('main'):
        	self._meta_freq_config.add_section('main')
        self._meta_freq_config.set('main', 'freq', str(None))
        self._meta_freq_config.write(open(self.config_file, 'w'))
        self._meta_time_config = ConfigParser.ConfigParser()
        self._meta_time_config.read(self.config_file)
        if not self._meta_time_config.has_section('main'):
        	self._meta_time_config.add_section('main')
        self._meta_time_config.set('main', 'time', str(None))
        self._meta_time_config.write(open(self.config_file, 'w'))
        self._meta_gain_config = ConfigParser.ConfigParser()
        self._meta_gain_config.read(self.config_file)
        if not self._meta_gain_config.has_section('main'):
        	self._meta_gain_config.add_section('main')
        self._meta_gain_config.set('main', 'gain', str(None))
        self._meta_gain_config.write(open(self.config_file, 'w'))

    def get_meta_dev(self):
        return self.meta_dev

    def set_meta_dev(self, meta_dev):
        self.meta_dev = meta_dev

    def get_meta_samp_rate_dev(self):
        return self.meta_samp_rate_dev

    def set_meta_samp_rate_dev(self, meta_samp_rate_dev):
        self.meta_samp_rate_dev = meta_samp_rate_dev
        self.src.set_sample_rate(self.meta_samp_rate_dev)

    def get_meta_samp_rate(self):
        return self.meta_samp_rate

    def set_meta_samp_rate(self, meta_samp_rate):
        self.meta_samp_rate = meta_samp_rate
        self.set_samp_rate(self.meta_samp_rate)
        self.time_tagger.rate = self.meta_samp_rate

    def get_meta_gain(self):
        return self.meta_gain

    def set_meta_gain(self, meta_gain):
        self.meta_gain = meta_gain
        self.set_gain(self.meta_gain)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_meta_time(self):
        return self.meta_time

    def set_meta_time(self, meta_time):
        self.meta_time = meta_time

    def get_meta_output_file(self):
        return self.meta_output_file

    def set_meta_output_file(self, meta_output_file):
        self.meta_output_file = meta_output_file
        self.blocks_file_meta_sink_0.open(self.meta_output_file)

    def get_meta_freq(self):
        return self.meta_freq

    def set_meta_freq(self, meta_freq):
        self.meta_freq = meta_freq
        self.src.set_center_freq(self.meta_freq, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.src.set_gain(self.gain, 0)

    def get_bandwidth_rtlsdr(self):
        return self.bandwidth_rtlsdr

    def set_bandwidth_rtlsdr(self, bandwidth_rtlsdr):
        self.bandwidth_rtlsdr = bandwidth_rtlsdr
        self.src.set_bandwidth(self.bandwidth_rtlsdr, 0)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--config-file", dest="config_file", type="string", default='./default.meta',
        help="Set config_file [default=%default]")
    parser.add_option(
        "", "--meta-dev", dest="meta_dev", type="string", default='rtl_tcp=10.0.0.219:1234',
        help="Set meta_dev [default=%default]")
    parser.add_option(
        "", "--meta-samp-rate-dev", dest="meta_samp_rate_dev", type="intx", default=1536000,
        help="Set meta_samp_rate_dev [default=%default]")
    return parser


def main(top_block_cls=receiver_nogui_dev, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(config_file=options.config_file, meta_dev=options.meta_dev, meta_samp_rate_dev=options.meta_samp_rate_dev)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
