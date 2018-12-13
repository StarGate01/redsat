#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Downlink from TVAC (This should run all the time)
# Author: Sebastian Rückerl
# Generated: Thu Dec 13 05:10:57 2018
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
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import digital;import cmath
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import ccsds
import math
import osmosdr
import sip
import sys
from gnuradio import qtgui


class downlink(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Downlink from TVAC (This should run all the time)")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Downlink from TVAC (This should run all the time)")
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

        self.settings = Qt.QSettings("GNU Radio", "downlink")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.block_len_enc = block_len_enc = 1024/8*2

        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 4, 1).base()

        self.samp_rate_factor = samp_rate_factor = 5
        self.samp_rate = samp_rate = 250000
        self.rgain = rgain = 0
        self.payload = payload = block_len_enc+4
        self.freq_offset_flag = freq_offset_flag = 0
        self.freq_offset = freq_offset = 0

        ##################################################
        # Blocks
        ##################################################
        self._rgain_range = Range(0, 11, 1, 0, 200)
        self._rgain_win = RangeWidget(self._rgain_range, self.set_rgain, 'RX Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rgain_win)
        self._freq_offset_range = Range(-400e3, 400e3, 1.5e3, 0, 200)
        self._freq_offset_win = RangeWidget(self._freq_offset_range, self.set_freq_offset, 'Frequency Offset', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_offset_win)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=5,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_sink_x_1 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	False, #plotfreq
        	False, #plotwaterfall
        	False, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_1_win)

        self.qtgui_sink_x_1.enable_rf_freq(False)



        self.qtgui_sink_x_0_0_1 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"Vor Sync", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0_0_1.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_sink_x_0_0_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_0_1_win)

        self.qtgui_sink_x_0_0_1.enable_rf_freq(False)



        self.qtgui_sink_x_0_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate*samp_rate_factor, #bw
        	"Vor Sync", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_0_win)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)



        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'rtl_tcp=10.0.0.51:1234' )
        self.osmosdr_source_0.set_sample_rate(samp_rate*samp_rate_factor)
        self.osmosdr_source_0.set_center_freq(145.95, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rgain, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(0, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self._freq_offset_flag_range = Range(0, 1, 1, 0, 200)
        self._freq_offset_flag_win = RangeWidget(self._freq_offset_flag_range, self.set_freq_offset_flag, 'Enable flatsat freq', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_offset_flag_win)
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(samp_rate_factor, (1, ))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_mpsk_receiver_cc_0_0 = digital.mpsk_receiver_cc(2, 0, cmath.pi/100.0, -0.05, 0.05, 0.25, 0.05, 4, 4, 0.005)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(variable_constellation_0)
        self.ccsds_softbits_msg_to_bytes_b_0 = ccsds.softbits_msg_to_bytes_b()
        self.ccsds_randomiser_softbits_0 = ccsds.randomiser_softbits(0x95,0xFF)
        self.ccsds_mpsk_ambiguity_resolver_f_0 = ccsds.mpsk_ambiguity_resolver_f(2,'49E0DCC7',32,1,0.8,block_len_enc,0)
        self.ccsds_message_info_0 = ccsds.message_info("Block received and sent to Nanolink: ", 10)
        self.ccsds_ldpc_decoder_0 = ccsds.ldpc_decoder('/tmp/AR4JA_r12_k1024n.a', ccsds.LDPC_SYS_FRONT, ccsds.LDPC_PUNCT_BACK, 512, tuple(([])))
        self.ccsds_blob_msg_sink_b_0 = ccsds.blob_msg_sink_b(256/2)
        self.blocks_udp_sink_0_1 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 5431, 256, True)
        self.blocks_udp_sink_0_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 5433, 1472, True)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_gr_complex*1, '127.0.0.1', 5435, 1472, True)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 0.5)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-1, ))
        self.band_pass_filter_0 = filter.fir_filter_ccc(1, firdes.complex_band_pass(
        	1, samp_rate*samp_rate_factor, 40e3, 60e3, 6e3, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate*samp_rate_factor, analog.GR_COS_WAVE, -freq_offset, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -50000, 1, 0)
        self.analog_agc_xx_0 = analog.agc_cc(1e-4, 0.5, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ccsds_blob_msg_sink_b_0, 'out'), (self.ccsds_message_info_0, 'in'))
        self.msg_connect((self.ccsds_ldpc_decoder_0, 'out'), (self.ccsds_softbits_msg_to_bytes_b_0, 'in'))
        self.msg_connect((self.ccsds_mpsk_ambiguity_resolver_f_0, 'out'), (self.ccsds_randomiser_softbits_0, 'in'))
        self.msg_connect((self.ccsds_randomiser_softbits_0, 'out'), (self.ccsds_ldpc_decoder_0, 'in'))
        self.connect((self.analog_agc_xx_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.ccsds_mpsk_ambiguity_resolver_f_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_sink_x_0_0_1, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.ccsds_softbits_msg_to_bytes_b_0, 0), (self.blocks_null_sink_1, 0))
        self.connect((self.ccsds_softbits_msg_to_bytes_b_0, 0), (self.blocks_udp_sink_0_1, 0))
        self.connect((self.ccsds_softbits_msg_to_bytes_b_0, 0), (self.ccsds_blob_msg_sink_b_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_udp_sink_0_0, 0))
        self.connect((self.digital_mpsk_receiver_cc_0_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_mpsk_receiver_cc_0_0, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.digital_mpsk_receiver_cc_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "downlink")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_block_len_enc(self):
        return self.block_len_enc

    def set_block_len_enc(self, block_len_enc):
        self.block_len_enc = block_len_enc
        self.set_payload(self.block_len_enc+4)

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0

    def get_samp_rate_factor(self):
        return self.samp_rate_factor

    def set_samp_rate_factor(self, samp_rate_factor):
        self.samp_rate_factor = samp_rate_factor
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samp_rate*self.samp_rate_factor)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate*self.samp_rate_factor)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate*self.samp_rate_factor, 40e3, 60e3, 6e3, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate*self.samp_rate_factor)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_0_0_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samp_rate*self.samp_rate_factor)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate*self.samp_rate_factor)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate*self.samp_rate_factor, 40e3, 60e3, 6e3, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate*self.samp_rate_factor)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_rgain(self):
        return self.rgain

    def set_rgain(self, rgain):
        self.rgain = rgain
        self.osmosdr_source_0.set_gain(self.rgain, 0)

    def get_payload(self):
        return self.payload

    def set_payload(self, payload):
        self.payload = payload

    def get_freq_offset_flag(self):
        return self.freq_offset_flag

    def set_freq_offset_flag(self, freq_offset_flag):
        self.freq_offset_flag = freq_offset_flag

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.analog_sig_source_x_0_0.set_frequency(-self.freq_offset)


def main(top_block_cls=downlink, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start(2080)
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
