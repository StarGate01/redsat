#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: REDSAT receiver
# Author: Christoph Honal
# Generated: Wed Dec 26 11:25:26 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import calendar
import osmosdr
import sip
import sys
import time
from gnuradio import qtgui


class receiver(gr.top_block, Qt.QWidget):

    def __init__(self, meta_dev='rtl_tcp=host.docker.internal:1234', meta_freq=145950000, meta_gain=20, meta_output_file='/app/input/test.raw', meta_rec_udp=1, meta_samp=128000, meta_rec_udp_port=7575, meta_rec_udp_host='127.0.0.1'):
        gr.top_block.__init__(self, "REDSAT receiver")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("REDSAT receiver")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "receiver")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.meta_dev = meta_dev
        self.meta_freq = meta_freq
        self.meta_gain = meta_gain
        self.meta_output_file = meta_output_file
        self.meta_rec_udp = meta_rec_udp
        self.meta_samp = meta_samp
        self.meta_rec_udp_port = meta_rec_udp_port
        self.meta_rec_udp_host = meta_rec_udp_host

        ##################################################
        # Variables
        ##################################################
        self.unix_now = unix_now = str(calendar.timegm(time.gmtime()))
        self.samp_rate_rtlsdr = samp_rate_rtlsdr = 1536000
        self.samp_rate = samp_rate = meta_samp
        self.gain = gain = meta_gain
        self.freq_real = freq_real = meta_freq
        self.bandwidth_rtlsdr = bandwidth_rtlsdr = 100000

        ##################################################
        # Blocks
        ##################################################
        self._gain_range = Range(0, 200, 1, meta_gain, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'RF Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_win)
        self._freq_real_range = Range(100000000, 200000000, 5000, meta_freq, 200)
        self._freq_real_win = RangeWidget(self._freq_real_range, self.set_freq_real, 'Frequency', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_real_win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=int(samp_rate_rtlsdr/samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	samp_rate, #fc
        	bandwidth_rtlsdr, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	False, #plottime
        	False, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + meta_dev )
        self.osmosdr_source_0.set_sample_rate(samp_rate_rtlsdr)
        self.osmosdr_source_0.set_center_freq(freq_real, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(bandwidth_rtlsdr, 0)

        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_gr_complex*1, meta_rec_udp_host, meta_rec_udp_port, 1472, True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, meta_output_file, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blks2_selector_1 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=meta_rec_udp,
        	output_index=0,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_selector_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blks2_selector_1, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_udp_source_0, 0), (self.blks2_selector_1, 1))
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blks2_selector_1, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "receiver")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_meta_dev(self):
        return self.meta_dev

    def set_meta_dev(self, meta_dev):
        self.meta_dev = meta_dev

    def get_meta_freq(self):
        return self.meta_freq

    def set_meta_freq(self, meta_freq):
        self.meta_freq = meta_freq
        self.set_freq_real(self.meta_freq)

    def get_meta_gain(self):
        return self.meta_gain

    def set_meta_gain(self, meta_gain):
        self.meta_gain = meta_gain
        self.set_gain(self.meta_gain)

    def get_meta_output_file(self):
        return self.meta_output_file

    def set_meta_output_file(self, meta_output_file):
        self.meta_output_file = meta_output_file
        self.blocks_file_sink_0.open(self.meta_output_file)

    def get_meta_rec_udp(self):
        return self.meta_rec_udp

    def set_meta_rec_udp(self, meta_rec_udp):
        self.meta_rec_udp = meta_rec_udp
        self.blks2_selector_1.set_input_index(int(self.meta_rec_udp))

    def get_meta_samp(self):
        return self.meta_samp

    def set_meta_samp(self, meta_samp):
        self.meta_samp = meta_samp
        self.set_samp_rate(self.meta_samp)

    def get_meta_rec_udp_port(self):
        return self.meta_rec_udp_port

    def set_meta_rec_udp_port(self, meta_rec_udp_port):
        self.meta_rec_udp_port = meta_rec_udp_port

    def get_meta_rec_udp_host(self):
        return self.meta_rec_udp_host

    def set_meta_rec_udp_host(self, meta_rec_udp_host):
        self.meta_rec_udp_host = meta_rec_udp_host

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
        self.qtgui_sink_x_0.set_frequency_range(self.samp_rate, self.bandwidth_rtlsdr)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_freq_real(self):
        return self.freq_real

    def set_freq_real(self, freq_real):
        self.freq_real = freq_real
        self.osmosdr_source_0.set_center_freq(self.freq_real, 0)

    def get_bandwidth_rtlsdr(self):
        return self.bandwidth_rtlsdr

    def set_bandwidth_rtlsdr(self, bandwidth_rtlsdr):
        self.bandwidth_rtlsdr = bandwidth_rtlsdr
        self.qtgui_sink_x_0.set_frequency_range(self.samp_rate, self.bandwidth_rtlsdr)
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
        "", "--meta-rec-udp", dest="meta_rec_udp", type="intx", default=1,
        help="Set meta_rec_udp [default=%default]")
    parser.add_option(
        "", "--meta-samp", dest="meta_samp", type="intx", default=128000,
        help="Set meta_samp [default=%default]")
    parser.add_option(
        "", "--meta-rec-udp-port", dest="meta_rec_udp_port", type="intx", default=7575,
        help="Set meta_rec_udp_port [default=%default]")
    parser.add_option(
        "", "--meta-rec-udp-host", dest="meta_rec_udp_host", type="string", default='127.0.0.1',
        help="Set meta_rec_udp_host [default=%default]")
    return parser


def main(top_block_cls=receiver, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(meta_dev=options.meta_dev, meta_freq=options.meta_freq, meta_gain=options.meta_gain, meta_output_file=options.meta_output_file, meta_rec_udp=options.meta_rec_udp, meta_samp=options.meta_samp, meta_rec_udp_port=options.meta_rec_udp_port, meta_rec_udp_host=options.meta_rec_udp_host)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
