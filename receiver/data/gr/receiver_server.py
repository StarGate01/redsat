#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: REDSAT receiver server
# Author: Christoph Honal
# Generated: Wed Dec 26 18:13:28 2018
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
from optparse import OptionParser
import osmosdr
import sip
import sys
import time
from gnuradio import qtgui


class receiver_server(gr.top_block, Qt.QWidget):

    def __init__(self, meta_dev='rtl=1', meta_freq=103200000, meta_gain=40, meta_samp=128000):
        gr.top_block.__init__(self, "REDSAT receiver server")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("REDSAT receiver server")
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

        self.settings = Qt.QSettings("GNU Radio", "receiver_server")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.meta_dev = meta_dev
        self.meta_freq = meta_freq
        self.meta_gain = meta_gain
        self.meta_samp = meta_samp

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_rtlsdr = samp_rate_rtlsdr = 1536000
        self.samp_rate = samp_rate = meta_samp
        self.real_gain = real_gain = meta_gain
        self.real_freq = real_freq = meta_freq
        self.bandwidth_rtlsdr = bandwidth_rtlsdr = 100000

        ##################################################
        # Blocks
        ##################################################
        self._real_gain_range = Range(0, 100, 1, meta_gain, 200)
        self._real_gain_win = RangeWidget(self._real_gain_range, self.set_real_gain, 'RX Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._real_gain_win)
        self._real_freq_range = Range(50000000, 200000000, 10000, meta_freq, 200)
        self._real_freq_win = RangeWidget(self._real_freq_range, self.set_real_freq, 'Frequency', "counter_slider", float)
        self.top_grid_layout.addWidget(self._real_freq_win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=int(samp_rate_rtlsdr/samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
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
        self.osmosdr_source_0.set_center_freq(real_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(real_gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(bandwidth_rtlsdr, 0)

        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_gr_complex*1, '127.0.0.1', 7474, 1472, True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "receiver_server")
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
        self.set_real_freq(self.meta_freq)

    def get_meta_gain(self):
        return self.meta_gain

    def set_meta_gain(self, meta_gain):
        self.meta_gain = meta_gain
        self.set_real_gain(self.meta_gain)

    def get_meta_samp(self):
        return self.meta_samp

    def set_meta_samp(self, meta_samp):
        self.meta_samp = meta_samp
        self.set_samp_rate(self.meta_samp)

    def get_samp_rate_rtlsdr(self):
        return self.samp_rate_rtlsdr

    def set_samp_rate_rtlsdr(self, samp_rate_rtlsdr):
        self.samp_rate_rtlsdr = samp_rate_rtlsdr
        self.osmosdr_source_0.set_sample_rate(self.samp_rate_rtlsdr)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_real_gain(self):
        return self.real_gain

    def set_real_gain(self, real_gain):
        self.real_gain = real_gain
        self.osmosdr_source_0.set_gain(self.real_gain, 0)

    def get_real_freq(self):
        return self.real_freq

    def set_real_freq(self, real_freq):
        self.real_freq = real_freq
        self.osmosdr_source_0.set_center_freq(self.real_freq, 0)

    def get_bandwidth_rtlsdr(self):
        return self.bandwidth_rtlsdr

    def set_bandwidth_rtlsdr(self, bandwidth_rtlsdr):
        self.bandwidth_rtlsdr = bandwidth_rtlsdr
        self.osmosdr_source_0.set_bandwidth(self.bandwidth_rtlsdr, 0)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--meta-dev", dest="meta_dev", type="string", default='rtl=1',
        help="Set meta_dev [default=%default]")
    parser.add_option(
        "", "--meta-freq", dest="meta_freq", type="intx", default=103200000,
        help="Set meta_freq [default=%default]")
    parser.add_option(
        "", "--meta-gain", dest="meta_gain", type="eng_float", default=eng_notation.num_to_str(40),
        help="Set meta_gain [default=%default]")
    parser.add_option(
        "", "--meta-samp", dest="meta_samp", type="intx", default=128000,
        help="Set meta_samp [default=%default]")
    return parser


def main(top_block_cls=receiver_server, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(meta_dev=options.meta_dev, meta_freq=options.meta_freq, meta_gain=options.meta_gain, meta_samp=options.meta_samp)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
