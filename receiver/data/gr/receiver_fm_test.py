#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: REDSAT test FM listener
# Author: Christoph Honal
# Generated: Wed Dec 26 21:19:02 2018
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time


class receiver_fm_test(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "REDSAT test FM listener")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_rtlsdr = samp_rate_rtlsdr = 1536000
        self.samp_rate_0 = samp_rate_0 = 128000
        self.samp_rate = samp_rate = 128000
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
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'rtl_tcp=127.0.0.1:7373' )
        self.osmosdr_source_0.set_sample_rate(samp_rate_rtlsdr)
        self.osmosdr_source_0.set_center_freq(103200000, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(50, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(100000, 0)

        self.audio_sink_0 = audio.sink(samp_rate, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=500000,
        	audio_decimation=1,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.audio_sink_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_wfm_rcv_0, 0))

    def get_samp_rate_rtlsdr(self):
        return self.samp_rate_rtlsdr

    def set_samp_rate_rtlsdr(self, samp_rate_rtlsdr):
        self.samp_rate_rtlsdr = samp_rate_rtlsdr
        self.osmosdr_source_0.set_sample_rate(self.samp_rate_rtlsdr)

    def get_samp_rate_0(self):
        return self.samp_rate_0

    def set_samp_rate_0(self, samp_rate_0):
        self.samp_rate_0 = samp_rate_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_bandwidth_rtlsdr(self):
        return self.bandwidth_rtlsdr

    def set_bandwidth_rtlsdr(self, bandwidth_rtlsdr):
        self.bandwidth_rtlsdr = bandwidth_rtlsdr


def main(top_block_cls=receiver_fm_test, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
