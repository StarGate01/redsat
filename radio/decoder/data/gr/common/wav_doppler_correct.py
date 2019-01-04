#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Wav Doppler Correct
# Generated: Fri Jan  4 18:03:09 2019
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from doppler_correction import doppler_correction  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
from os.path import splitext
from range_selector import range_selector  # grc-generated hier_block
import ConfigParser


class wav_doppler_correct(gr.top_block):

    def __init__(self, filename="", freq_offset=10e3, keep=0, skip=0):
        gr.top_block.__init__(self, "Wav Doppler Correct")

        ##################################################
        # Parameters
        ##################################################
        self.filename = filename
        self.freq_offset = freq_offset
        self.keep = keep
        self.skip = skip

        ##################################################
        # Variables
        ##################################################
        self._meta_samp_rate_config = ConfigParser.ConfigParser()
        self._meta_samp_rate_config.read(filename)
        try: meta_samp_rate = self._meta_samp_rate_config.getfloat('main', 'samp_rate')
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
        self.doppler_correction_0 = doppler_correction(
            p_doppler_correct=1000,
            p_offset=freq_offset,
            p_realtime=False,
            v_meta_file=filename,
        )
        self.blocks_wavfile_source_0 = blocks.wavfile_source(filename_base + ".wav", False)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(filename_base + ".d.wav", 2, int(meta_samp_rate), 16)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_wavfile_sink_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.range_selector_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_0, 1))
        self.connect((self.doppler_correction_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.range_selector_0, 0), (self.doppler_correction_0, 0))

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self._meta_samp_rate_config = ConfigParser.ConfigParser()
        self._meta_samp_rate_config.read(self.filename)
        if not self._meta_samp_rate_config.has_section('main'):
        	self._meta_samp_rate_config.add_section('main')
        self._meta_samp_rate_config.set('main', 'samp_rate', str(None))
        self._meta_samp_rate_config.write(open(self.filename, 'w'))
        self.set_filename_base(splitext(self.filename)[0])
        self.doppler_correction_0.set_v_meta_file(self.filename)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.doppler_correction_0.set_p_offset(self.freq_offset)

    def get_keep(self):
        return self.keep

    def set_keep(self, keep):
        self.keep = keep

    def get_skip(self):
        return self.skip

    def set_skip(self, skip):
        self.skip = skip

    def get_meta_samp_rate(self):
        return self.meta_samp_rate

    def set_meta_samp_rate(self, meta_samp_rate):
        self.meta_samp_rate = meta_samp_rate

    def get_filename_base(self):
        return self.filename_base

    def set_filename_base(self, filename_base):
        self.filename_base = filename_base
        self.blocks_wavfile_sink_0.open(self.filename_base + ".d.wav")


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-f", "--filename", dest="filename", type="string", default="",
        help="Set filename [default=%default]")
    parser.add_option(
        "-o", "--freq-offset", dest="freq_offset", type="eng_float", default=eng_notation.num_to_str(10e3),
        help="Set Freq Offset [default=%default]")
    parser.add_option(
        "-k", "--keep", dest="keep", type="intx", default=0,
        help="Set keep [default=%default]")
    parser.add_option(
        "-s", "--skip", dest="skip", type="intx", default=0,
        help="Set skip [default=%default]")
    return parser


def main(top_block_cls=wav_doppler_correct, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(filename=options.filename, freq_offset=options.freq_offset, keep=options.keep, skip=options.skip)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
