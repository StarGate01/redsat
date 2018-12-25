#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: C Waterfall
# Generated: Tue Dec 25 20:25:32 2018
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import satnogs


class c_waterfall(gr.top_block):

    def __init__(self, filename=""):
        gr.top_block.__init__(self, "C Waterfall")

        ##################################################
        # Parameters
        ##################################################
        self.filename = filename

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 128e3

        ##################################################
        # Blocks
        ##################################################
        self.satnogs_waterfall_sink_0_0 = satnogs.waterfall_sink(samp_rate, 0.0, 15, 4096, filename + ".nd.wf", 0)
        self.satnogs_waterfall_sink_0 = satnogs.waterfall_sink(samp_rate, 0.0, 15, 4096, filename + ".d.wf", 0)
        self.blocks_vector_to_streams_0 = blocks.vector_to_streams(gr.sizeof_gr_complex*1, 2)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*2, filename + ".raw_dpl", False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_vector_to_streams_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.satnogs_waterfall_sink_0, 0))    
        self.connect((self.blocks_vector_to_streams_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_vector_to_streams_0, 1), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_vector_to_streams_0, 0), (self.satnogs_waterfall_sink_0_0, 0))    

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_file_source_0.open(self.filename + ".raw_dpl", False)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "-f", "--filename", dest="filename", type="string", default="",
        help="Set filename [default=%default]")
    return parser


def main(top_block_cls=c_waterfall, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(filename=options.filename)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
