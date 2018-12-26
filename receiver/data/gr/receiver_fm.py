#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: REDSAT test FM listener
# Author: Christoph Honal
# Generated: Wed Dec 26 11:24:08 2018
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class receiver_fm(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "REDSAT test FM listener")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 128000

        ##################################################
        # Blocks
        ##################################################
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_gr_complex*1, '127.0.0.1', 7474, 1472, True)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=500000,
        	audio_decimation=1,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_udp_source_0, 0), (self.analog_wfm_rcv_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def main(top_block_cls=receiver_fm, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
