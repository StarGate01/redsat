#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: REDSAT receiver
# Author: Christoph Honal
# Generated: Wed Dec 26 08:41:40 2018
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import calendar
import osmosdr
import sys
import time


class receiver_nogui(gr.top_block):

    def __init__(self, meta_dev='rtl_tcp=host.docker.internal:1234', meta_freq=145950000, meta_gain=20, meta_output_file='/app/input/test.raw', meta_samp=128000):
        gr.top_block.__init__(self, "REDSAT receiver")

        ##################################################
        # Parameters
        ##################################################
        self.meta_dev = meta_dev
        self.meta_freq = meta_freq
        self.meta_gain = meta_gain
        self.meta_output_file = meta_output_file
        self.meta_samp = meta_samp

        ##################################################
        # Variables
        ##################################################
        self.unix_now = unix_now = str(calendar.timegm(time.gmtime()))
        self.samp_rate_rtlsdr = samp_rate_rtlsdr = 1536000
        self.samp_rate = samp_rate = meta_samp
        self.bandwidth_rtlsdr = bandwidth_rtlsdr = 100000

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=int(samp_rate_rtlsdr/samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + meta_dev )
        self.osmosdr_source_0.set_sample_rate(samp_rate_rtlsdr)
        self.osmosdr_source_0.set_center_freq(meta_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(meta_gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(bandwidth_rtlsdr, 0)

        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, meta_output_file, False)
        self.blocks_file_sink_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_file_sink_0, 0))

    def get_meta_dev(self):
        return self.meta_dev

    def set_meta_dev(self, meta_dev):
        self.meta_dev = meta_dev

    def get_meta_freq(self):
        return self.meta_freq

    def set_meta_freq(self, meta_freq):
        self.meta_freq = meta_freq
        self.osmosdr_source_0.set_center_freq(self.meta_freq, 0)

    def get_meta_gain(self):
        return self.meta_gain

    def set_meta_gain(self, meta_gain):
        self.meta_gain = meta_gain
        self.osmosdr_source_0.set_gain(self.meta_gain, 0)

    def get_meta_output_file(self):
        return self.meta_output_file

    def set_meta_output_file(self, meta_output_file):
        self.meta_output_file = meta_output_file
        self.blocks_file_sink_0.open(self.meta_output_file)

    def get_meta_samp(self):
        return self.meta_samp

    def set_meta_samp(self, meta_samp):
        self.meta_samp = meta_samp
        self.set_samp_rate(self.meta_samp)

    def get_unix_now(self):
        return self.unix_now

    def set_unix_now(self, unix_now):
        self.unix_now = unix_now

    def get_samp_rate_rtlsdr(self):
        return self.samp_rate_rtlsdr

    def set_samp_rate_rtlsdr(self, samp_rate_rtlsdr):
        self.samp_rate_rtlsdr = samp_rate_rtlsdr
        self.osmosdr_source_0.set_sample_rate(self.samp_rate_rtlsdr)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_bandwidth_rtlsdr(self):
        return self.bandwidth_rtlsdr

    def set_bandwidth_rtlsdr(self, bandwidth_rtlsdr):
        self.bandwidth_rtlsdr = bandwidth_rtlsdr
        self.osmosdr_source_0.set_bandwidth(self.bandwidth_rtlsdr, 0)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--meta-dev", dest="meta_dev", type="string", default='rtl_tcp=host.docker.internal:1234',
        help="Set meta_dev [default=%default]")
    parser.add_option(
        "", "--meta-freq", dest="meta_freq", type="intx", default=145950000,
        help="Set meta_freq [default=%default]")
    parser.add_option(
        "", "--meta-gain", dest="meta_gain", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set meta_gain [default=%default]")
    parser.add_option(
        "", "--meta-output-file", dest="meta_output_file", type="string", default='/app/input/test.raw',
        help="Set meta_output_file [default=%default]")
    parser.add_option(
        "", "--meta-samp", dest="meta_samp", type="intx", default=128000,
        help="Set meta_samp [default=%default]")
    return parser


def main(top_block_cls=receiver_nogui, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(meta_dev=options.meta_dev, meta_freq=options.meta_freq, meta_gain=options.meta_gain, meta_output_file=options.meta_output_file, meta_samp=options.meta_samp)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
