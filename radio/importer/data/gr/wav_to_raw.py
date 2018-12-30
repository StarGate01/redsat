#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: REDSAT converter
# Author: Christoph Honal, Alexander Ulanowski
# Generated: Sun Dec 30 02:52:40 2018
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import gr, blocks
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class wav_to_raw(gr.top_block):

    def __init__(self, meta_input_file="/app/import/input.wav", meta_output_file="/app/input/input.raw", meta_samp_rate=128000):
        gr.top_block.__init__(self, "REDSAT converter")

        ##################################################
        # Parameters
        ##################################################
        self.meta_input_file = meta_input_file
        self.meta_output_file = meta_output_file
        self.meta_samp_rate = meta_samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.blocks_wavfile_source_0 = blocks.wavfile_source(meta_input_file, False)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, meta_output_file, meta_samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, "", False)
        self.blocks_file_meta_sink_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_file_meta_sink_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_0, 1))

    def get_meta_input_file(self):
        return self.meta_input_file

    def set_meta_input_file(self, meta_input_file):
        self.meta_input_file = meta_input_file

    def get_meta_output_file(self):
        return self.meta_output_file

    def set_meta_output_file(self, meta_output_file):
        self.meta_output_file = meta_output_file
        self.blocks_file_meta_sink_0.open(self.meta_output_file)

    def get_meta_samp_rate(self):
        return self.meta_samp_rate

    def set_meta_samp_rate(self, meta_samp_rate):
        self.meta_samp_rate = meta_samp_rate


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--meta-input-file", dest="meta_input_file", type="string", default="/app/import/input.wav",
        help="Set meta_input_file [default=%default]")
    parser.add_option(
        "", "--meta-output-file", dest="meta_output_file", type="string", default="/app/input/input.raw",
        help="Set meta_output_file [default=%default]")
    parser.add_option(
        "", "--meta-samp-rate", dest="meta_samp_rate", type="intx", default=128000,
        help="Set meta_samp_rate [default=%default]")
    return parser


def main(top_block_cls=wav_to_raw, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(meta_input_file=options.meta_input_file, meta_output_file=options.meta_output_file, meta_samp_rate=options.meta_samp_rate)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
