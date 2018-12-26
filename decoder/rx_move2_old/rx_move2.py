#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: MOVE II
# Author: alu
# Generated: Mon Dec 24 19:40:19 2018
##################################################

from datetime import datetime
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import gpredict
import osmosdr
import satnogs
import sys
import time


class rx_move2(gr.top_block):

    def __init__(self, freq=145.95e6, gain=38):
        gr.top_block.__init__(self, "MOVE II")

        ##################################################
        # Parameters
        ##################################################
        self.freq = freq
        self.gain = gain

        ##################################################
        # Variables
        ##################################################
        self.doppler_freq = doppler_freq = freq
        self.samp_rate_rtlsdr = samp_rate_rtlsdr = 1536000
        self.samp_rate = samp_rate = 128000
        self.filename = filename = "iq_{0}_f{1}_g{2}".format(time.strftime("%Y-%m-%d_%H-%M-%S"), int(freq), gain)
        self.doppler_shift = doppler_shift = doppler_freq-freq
        self.decim = decim = 8

        ##################################################
        # Blocks
        ##################################################
        self.satnogs_waterfall_sink_0 = satnogs.waterfall_sink(samp_rate, 0.0, 5, 2048, filename + ".wf", 1)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=int(samp_rate_rtlsdr/samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(samp_rate_rtlsdr)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.gpredict_doppler_0 = gpredict.doppler(self.set_doppler_freq, "0.0.0.0", 4532, True)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_gr_complex*1, '127.0.0.1', 12345, 1472, False)
        self.blocks_streams_to_vector_0 = blocks.streams_to_vector(gr.sizeof_gr_complex*1, 2)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*2, filename + ".raw_dpl", False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, doppler_shift, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_streams_to_vector_0, 1))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_udp_sink_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.satnogs_waterfall_sink_0, 0))    
        self.connect((self.blocks_streams_to_vector_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_streams_to_vector_0, 0))    

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_filename("iq_{0}_f{1}_g{2}".format(time.strftime("%Y-%m-%d_%H-%M-%S"), int(self.freq), self.gain))
        self.set_doppler_shift(self.doppler_freq-self.freq)
        self.osmosdr_source_0.set_center_freq(self.freq, 0)
        self.set_doppler_freq(self.freq)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.set_filename("iq_{0}_f{1}_g{2}".format(time.strftime("%Y-%m-%d_%H-%M-%S"), int(self.freq), self.gain))
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_doppler_freq(self):
        return self.doppler_freq

    def set_doppler_freq(self, doppler_freq):
        self.doppler_freq = doppler_freq
        self.set_doppler_shift(self.doppler_freq-self.freq)

    def get_samp_rate_rtlsdr(self):
        return self.samp_rate_rtlsdr

    def set_samp_rate_rtlsdr(self, samp_rate_rtlsdr):
        self.samp_rate_rtlsdr = samp_rate_rtlsdr
        self.osmosdr_source_0.set_sample_rate(self.samp_rate_rtlsdr)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_file_sink_0_0.open(self.filename + ".raw_dpl")

    def get_doppler_shift(self):
        return self.doppler_shift

    def set_doppler_shift(self, doppler_shift):
        self.doppler_shift = doppler_shift
        self.analog_sig_source_x_1.set_frequency(self.doppler_shift)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-f", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(145.95e6),
        help="Set freq [default=%default]")
    parser.add_option(
        "-g", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(38),
        help="Set gain [default=%default]")
    return parser


def main(top_block_cls=rx_move2, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(freq=options.freq, gain=options.gain)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
