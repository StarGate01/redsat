#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Downlink for EM
# Author: Sebastian Rückerl
# Generated: Wed Nov 21 11:02:04 2018
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
import time
from gnuradio import qtgui

from os.path import splitext
from ConfigParser import ConfigParser


_meta_file = sys.argv[1] 
_file = splitext(_meta_file)[0] + ".wav"

config = ConfigParser()
config.read(_meta_file)
_samp_rate = int(config.get('main', 'samp_rate', None))


_repeat = False
if '-r' in sys.argv:
    _repeat = True

_submit = False
if '--submit' in sys.argv:
    _submit = True


class downlink_em(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Downlink for EM")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Downlink for EM")
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

        self.settings = Qt.QSettings("GNU Radio", "downlink_em")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.block_len_enc = block_len_enc = 1024/8*2

        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 4, 1).base()

        self.oversample = oversample = 4
        
        self.samp_rate = samp_rate = _samp_rate / oversample
        self.payload = payload = block_len_enc+4
        self.frequency_offset_correction = frequency_offset_correction = 60.0e3 

        ##################################################
        # Blocks
        ##################################################
        self._frequency_offset_correction_range = Range(-120000, 120000, 100, frequency_offset_correction, 200)
        self._frequency_offset_correction_win = RangeWidget(self._frequency_offset_correction_range, self.set_frequency_offset_correction, 'Frequency Correction', "counter_slider", float)
        self.top_grid_layout.addWidget(self._frequency_offset_correction_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=self.oversample,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_sink_x_0_0_1 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	145.79e6, #fc
        	samp_rate*oversample, #bw - 1??
        	"Vor Sync", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0_0_1.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_sink_x_0_0_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_0_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)


        self.qtgui_sink_x_0_0_1.enable_rf_freq(False)



        self.qtgui_sink_x_0_0_0_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate/oversample, #bw
        	"Vor Sync", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0_0_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_0_0_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)


        self.qtgui_sink_x_0_0_0_0.enable_rf_freq(False)



        self.qtgui_sink_x_0_0_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate/oversample, #bw
        	"Vor Sync", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_0_0_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)


        self.qtgui_sink_x_0_0_0.enable_rf_freq(False)


        # self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        # self.osmosdr_source_0.set_sample_rate(samp_rate*oversample)
        # self.osmosdr_source_0.set_center_freq(145.85e6, 0)
        # self.osmosdr_source_0.set_freq_corr(0, 0)
        # self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        # self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        # self.osmosdr_source_0.set_gain_mode(True, 0)
        # self.osmosdr_source_0.set_gain(30*1, 0)
        # self.osmosdr_source_0.set_if_gain(30*1, 0)
        # self.osmosdr_source_0.set_bb_gain(0, 0)
        # self.osmosdr_source_0.set_antenna('', 0)
        # self.osmosdr_source_0.set_bandwidth(0, 0)
        
        
        self.blocks_wavfile_source_0 = blocks.wavfile_source(_file, _repeat)
        
        
        self.blocks_message_debug_1_0_0 = blocks.message_debug()
        self.ccsds_message_info_0 = ccsds.message_info("Block received and sent to Nanolink: ", 20)

        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate*oversample,True)

        self.digital_mpsk_receiver_cc_0_0 = digital.mpsk_receiver_cc(2, 0, 31.41e-3, -0.01, 0.01, 0.25, 0.05, samp_rate/self.oversample/12.5e3, 0.01, 0.005)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(variable_constellation_0)
        self.ccsds_softbits_msg_to_bytes_b_0 = ccsds.softbits_msg_to_bytes_b()
        self.ccsds_send_nanolink_0 = ccsds.send_nanolink("http://move2radio.lrt.mw.tum.de" if _submit else "http://localhost:8000")
        self.ccsds_randomiser_softbits_0 = ccsds.randomiser_softbits(0x95,0xFF)
        self.ccsds_mpsk_ambiguity_resolver_f_0 = ccsds.mpsk_ambiguity_resolver_f(2,'49E0DCC7',32,1,0.8,block_len_enc,0)
        self.ccsds_ldpc_decoder_0 = ccsds.ldpc_decoder('/tmp/AR4JA_r12_k1024n.a', ccsds.LDPC_SYS_FRONT, ccsds.LDPC_PUNCT_BACK, 512, tuple(([])))
        self.ccsds_blob_msg_sink_b_0 = ccsds.blob_msg_sink_b(256/2)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 0.5)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-1, ))
        self.band_pass_filter_0 = filter.fir_filter_ccc(oversample, firdes.complex_band_pass(
        	1, samp_rate*oversample, 40e3, 60e3, 6e3, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate*oversample, analog.GR_COS_WAVE, frequency_offset_correction, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -50000, 1, 0)
        self.analog_agc_xx_0 = analog.agc_cc(1e-4, 0.5, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_throttle_0, 0))

        self.msg_connect((self.ccsds_blob_msg_sink_b_0, 'out'), (self.blocks_message_debug_1_0_0, 'print_pdu'))
        self.msg_connect((self.ccsds_blob_msg_sink_b_0, 'out'), (self.ccsds_message_info_0, 'in'))


        self.msg_connect((self.ccsds_blob_msg_sink_b_0, 'out'), (self.ccsds_send_nanolink_0, 'in'))
        self.msg_connect((self.ccsds_ldpc_decoder_0, 'out'), (self.ccsds_softbits_msg_to_bytes_b_0, 'in'))
        self.msg_connect((self.ccsds_mpsk_ambiguity_resolver_f_0, 'out'), (self.ccsds_randomiser_softbits_0, 'in'))
        self.msg_connect((self.ccsds_randomiser_softbits_0, 'out'), (self.ccsds_ldpc_decoder_0, 'in'))
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_sink_x_0_0_0_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.ccsds_mpsk_ambiguity_resolver_f_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.qtgui_sink_x_0_0_1, 0))
        self.connect((self.ccsds_softbits_msg_to_bytes_b_0, 0), (self.ccsds_blob_msg_sink_b_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_mpsk_receiver_cc_0_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_mpsk_receiver_cc_0_0, 0), (self.qtgui_sink_x_0_0_0, 0))
        #self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0_0, 0))

        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0_0, 0))
        #self.connect((self.blocks_throttle_0, 0), (self.qtgui_sink_x_0_0, 0))

        self.connect((self.rational_resampler_xxx_1, 0), (self.digital_mpsk_receiver_cc_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "downlink_em")
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

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0_0_1.set_frequency_range(145.79e6, self.samp_rate*self.oversample) # - 1??
        self.qtgui_sink_x_0_0_0_0.set_frequency_range(0, self.samp_rate/self.oversample)
        self.qtgui_sink_x_0_0_0.set_frequency_range(0, self.samp_rate/self.oversample)
        #self.osmosdr_source_0.set_sample_rate(self.samp_rate*self.oversample)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate*self.oversample)
        self.digital_mpsk_receiver_cc_0_0.set_omega(self.samp_rate/self.oversample/12.5e3)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate*self.oversample, 40e3, 60e3, 6e3, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate*self.oversample)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_payload(self):
        return self.payload

    def set_payload(self, payload):
        self.payload = payload

    def get_oversample(self):
        return self.oversample

    def set_oversample(self, oversample):
        self.oversample = oversample
        #self.osmosdr_source_0.set_sample_rate(self.samp_rate*self.oversample)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate*self.oversample, 40e3, 60e3, 6e3, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate*self.oversample)

    def get_frequency_offset_correction(self):
        return self.frequency_offset_correction

    def set_frequency_offset_correction(self, frequency_offset_correction):
        self.frequency_offset_correction = frequency_offset_correction
        self.analog_sig_source_x_0_0.set_frequency(self.frequency_offset_correction)


def main(top_block_cls=downlink_em, options=None):

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
