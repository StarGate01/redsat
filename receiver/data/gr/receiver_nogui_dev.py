#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: REDSAT receiver (device)
# Author: Christoph Honal, Alexander Ulanowski
# Generated: Thu Dec 27 23:31:14 2018
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
import osmosdr
import pmt
import satnogs
import sys
import time


class receiver_nogui_dev(gr.top_block):

    def __init__(self, config_file='./default.ini', meta_dev='rtl=0', meta_samp_rate_dev=1536000):
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
        self.start_time = start_time = time.time()
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
        self._meta_gain_config = ConfigParser.ConfigParser()
        self._meta_gain_config.read(config_file)
        try: meta_gain = self._meta_gain_config.getfloat('main', 'gain')
        except: meta_gain = 38
        self.meta_gain = meta_gain
        self._meta_freq_config = ConfigParser.ConfigParser()
        self._meta_freq_config.read(config_file)
        try: meta_freq = self._meta_freq_config.getfloat('main', 'freq')
        except: meta_freq = 145950000
        self.meta_freq = meta_freq
        self.bandwidth_rtlsdr = bandwidth_rtlsdr = 100000

        ##################################################
        # Blocks
        ##################################################
        self.satnogs_waterfall_sink_0 = satnogs.waterfall_sink(meta_samp_rate, 0.0, 15, 2048, splitext(config_file)[0] + ".wf", 1)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=int(meta_samp_rate_dev/samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + meta_dev )
        self.osmosdr_source_0.set_sample_rate(meta_samp_rate_dev)
        self.osmosdr_source_0.set_center_freq(meta_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(1, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(meta_gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(bandwidth_rtlsdr, 0)
          
        self.blocks_tags_strobe_0 = blocks.tags_strobe(gr.sizeof_gr_complex*1, pmt.intern(str(time.time())), meta_samp_rate, pmt.intern("time"))
        self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, meta_output_file, samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, "", False)
        self.blocks_file_meta_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_file_meta_sink_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.satnogs_waterfall_sink_0, 0))    
        self.connect((self.blocks_tags_strobe_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_add_xx_0, 0))    

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
        self._meta_gain_config = ConfigParser.ConfigParser()
        self._meta_gain_config.read(self.config_file)
        if not self._meta_gain_config.has_section('main'):
        	self._meta_gain_config.add_section('main')
        self._meta_gain_config.set('main', 'gain', str(None))
        self._meta_gain_config.write(open(self.config_file, 'w'))
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
        self._meta_time_config.set('main', 'time', str(self.start_time))
        self._meta_time_config.write(open(self.config_file, 'w'))

    def get_meta_dev(self):
        return self.meta_dev

    def set_meta_dev(self, meta_dev):
        self.meta_dev = meta_dev

    def get_meta_samp_rate_dev(self):
        return self.meta_samp_rate_dev

    def set_meta_samp_rate_dev(self, meta_samp_rate_dev):
        self.meta_samp_rate_dev = meta_samp_rate_dev
        self.osmosdr_source_0.set_sample_rate(self.meta_samp_rate_dev)

    def get_meta_samp_rate(self):
        return self.meta_samp_rate

    def set_meta_samp_rate(self, meta_samp_rate):
        self.meta_samp_rate = meta_samp_rate
        self.set_samp_rate(self.meta_samp_rate)
        self.blocks_tags_strobe_0.set_nsamps(self.meta_samp_rate)

    def get_start_time(self):
        return self.start_time

    def set_start_time(self, start_time):
        self.start_time = start_time
        self._meta_time_config = ConfigParser.ConfigParser()
        self._meta_time_config.read(self.config_file)
        if not self._meta_time_config.has_section('main'):
        	self._meta_time_config.add_section('main')
        self._meta_time_config.set('main', 'time', str(self.start_time))
        self._meta_time_config.write(open(self.config_file, 'w'))

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

    def get_meta_gain(self):
        return self.meta_gain

    def set_meta_gain(self, meta_gain):
        self.meta_gain = meta_gain
        self.osmosdr_source_0.set_gain(self.meta_gain, 0)

    def get_meta_freq(self):
        return self.meta_freq

    def set_meta_freq(self, meta_freq):
        self.meta_freq = meta_freq
        self.osmosdr_source_0.set_center_freq(self.meta_freq, 0)

    def get_bandwidth_rtlsdr(self):
        return self.bandwidth_rtlsdr

    def set_bandwidth_rtlsdr(self, bandwidth_rtlsdr):
        self.bandwidth_rtlsdr = bandwidth_rtlsdr
        self.osmosdr_source_0.set_bandwidth(self.bandwidth_rtlsdr, 0)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--config-file", dest="config_file", type="string", default='./default.ini',
        help="Set config_file [default=%default]")
    parser.add_option(
        "", "--meta-dev", dest="meta_dev", type="string", default='rtl=0',
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
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
