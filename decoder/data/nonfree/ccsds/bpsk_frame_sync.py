#!/usr/bin/env python
#
# Copyright 2010,2011 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gru
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser
from string import maketrans
# import scipy
# import numpy
# from numpy import asarray

# From gr-digital
from gnuradio import digital
# From gr-ccsds
import ccsds
from ccsds import ccsds_swig

import gnuradio.gr.gr_threading as _threading
# import packet_utils
from gnuradio.digital import digital_swig

# from current dir
# from receive_path import receive_path
# from uhd_interface import uhd_receiver

import struct
import sys

#import os
#print os.getpid()
#raw_input('Attach and press enter: ')

def hexstr2binstr(str,length=None):
	if length is None:
		length = len(str)*4
	return bin(int(str,16))[2:].zfill(length)

def int2binstr(num,length):
	return bin(num)[2:].zfill(length)

def hexstr2int(str):
	return int(str,16)

class bpsk_frame_sync(gr.hier_block2):
	def __init__(self, access_code=None, callback=None, threshold=-1):
	# """
	# Hierarchical block for frame syncing.

		# @param access_code: Attached Sync Marker
		# @type access_code: hex string
		# @param callback:  function of two args: ok, payload
		# @type callback: ok: bool; payload: string
		# @param threshold: detect access_code with up to threshold bits wrong (-1 -> use default)
		# @type threshold: int
	# """
		gr.hier_block2.__init__(self, "bpsk_frame_sync",
				gr.io_signature(2, 2, gr.sizeof_char), # Input signature
				gr.io_signature(0, 0, 0))					# Output signature

		if access_code is None:
			access_code = '1ACFFC1D'
		# if not digital.packet_utils.is_1_0_string(access_code):
			# raise ValueError, "Invalid access_code %r. Must be string of 1's and 0's" % (access_code,)
		self._access_code = hexstr2binstr(access_code)
		self._inv_access_code = self._access_code.translate(maketrans("10","01"))

		# Convolutional encoded ASM
		k = 7
		code_length = (len(access_code)*4)
		seed_length = k - 1
		length2encode = code_length - seed_length
		self.encoder = ccsds.ccsds_conv_encode(hexstr2int(access_code) >> length2encode, k) #, 2, asarray([79, 91]))
		enc_access_code = self.encoder.encode(hexstr2int(access_code), length2encode, 79, 109)
		self._enc_access_code = int2binstr(enc_access_code,length2encode*2)
		self._enc_inv_access_code = self._enc_access_code.translate(maketrans("10","01"))
		print "encoded ASM: %s" % str(hex(enc_access_code)) #
		print "encoded ASM: %s" % str(self._enc_access_code)
		self._access_code = self._enc_access_code
		self._inv_access_code = self._enc_inv_access_code

		if threshold == -1:
			threshold = 12			  # FIXME raise exception

		self.output_msgq = gr.msg_queue()		  # holds packets from the PHY
		# correlator looking for the non-inverted ASM
		self.correlator = digital_swig.correlate_access_code_bb(self._access_code, threshold)
		# correlator looking for the inverted ASM
		self.inv_correlator = digital_swig.correlate_access_code_bb(self._inv_access_code, threshold)

		# new framer that accepts parallel inputs from two correlators
		self.framer_sink = ccsds_swig.framer_sink_dual(self.output_msgq, 2550, 8) #2550, 8  1275, 4
		# connect the block input to the correlators
		# and the correlators to their respective port on the framer
		self.connect((self,0), self.correlator, (self.framer_sink,0))
		self.connect((self,1), self.inv_correlator, (self.framer_sink,1))

		# self._watcher = _queue_watcher_thread(self.output_msgq, callback)

class vit27_decode(gr.hier_block2):
	def __init__(self, options, input_msgq):
	# """
	# Hierarchical block for viterbi27 decoding.

		# @param access_code: Attached Sync Marker
		# @type access_code: hex string
		# @param callback:  function of two args: ok, payload
		# @type callback: ok: bool; payload: string
		# @param threshold: detect access_code with up to threshold bits wrong (-1 -> use default)
		# @type threshold: int
	# """
		gr.hier_block2.__init__(self, "vit27_decode",
				gr.io_signature(0, 0, 0), # Input signature
				gr.io_signature(0, 0, 0))					# Output signature
		# import os
		# print 'Blocked waiting for GDB attach (pid = %d)' % (os.getpid(),)
		# raw_input ('Press Enter to continue: ')
		# self._decoder = ccsds_swig.viterbi27_bb(10232);
		self._pkt_input = ccsds_swig.msg_source(gr.sizeof_char, input_msgq)
		# self._throttle = gr.throttle(gr.sizeof_char,1e3)
		# self._pkt_input.msgq().insert_tail(gr.message_from_string('01234'))
		# self.unpacker_bb = gr.packed_to_unpacked_bb(1,gr.GR_MSB_FIRST)
		# self.file_sink = gr.file_sink(gr.sizeof_char, options.to_file)
		self.file_sink = gr.file_sink(gr.sizeof_char, options.to_file)
		self.connect(self._pkt_input, 
			# self._throttle, 
			self.file_sink)


class _queue_watcher_thread(_threading.Thread):
	def __init__(self, rcvd_pktq, callback):
		_threading.Thread.__init__(self)
		self.setDaemon(1)
		self.rcvd_pktq = rcvd_pktq
		self.callback = callback
		self.keep_running = True
		self.start()


	def run(self):
		while self.keep_running:
			msg = self.rcvd_pktq.delete_head()
			payload = msg.to_string()
			if self.callback:
				self.callback(1, payload)


class receive_path(gr.hier_block2):
	def __init__(self, rx_callback, options):
		gr.hier_block2.__init__(self, "receive_path",
				gr.io_signature(2, 2, gr.sizeof_char),
				gr.io_signature(0, 0, 0))
		
		# options = copy.copy(options)	# make a copy so we can destructively modify

		self._verbose	 = options.verbose

		self._rx_callback = rx_callback  # this callback is fired when a frame arrives
		self._access_code = options.access_code
		self._threshold = options.threshold

		# receiver
		self.frame_receiver = \
			bpsk_frame_sync(access_code=self._access_code,
							   callback=self._rx_callback,
							   threshold=self._threshold)

		# Display some information about the setup
		# if self._verbose:
			# self._print_verbage()

		# connect block input to the frame receiver
		self.connect((self,0), (self.frame_receiver,0))
		self.connect((self,1), (self.frame_receiver,1))	
		
		if options.viterbi27:
			self.decoder = vit27_decode(options,self.frame_receiver.output_msgq);
			self.connect(self.decoder)
	
	def _print_verbage(self):
		"""
		Prints information about the receive path
		"""
		# print "\nReceive Path:"
		# print "modulation:	  %s"	% (self._demod_class.__name__)
		# print "bitrate:		 %sb/s" % (eng_notation.num_to_str(self._bitrate))
		# print "samples/symbol:  %.4f"	% (self.samples_per_symbol())
		# print "Differential:	%s"	% (self.differential())

class my_top_block(gr.top_block):
	def __init__(self, rx_callback, options):
		gr.top_block.__init__(self)

		if(options.from_file is not None):
			sys.stderr.write(("Reading samples from '%s'.\n\n" % (options.from_file)))
			self.source = gr.file_source(gr.sizeof_char, options.from_file, options.repeat_file)
		else:
			sys.stderr.write("No source defined, pulling samples from null source.\n\n")
			self.source = gr.null_source(gr.sizeof_gr_byte)

		# Set up receive path
		self.rxpath = receive_path(rx_callback, options) 
		self.unpacker_bb = gr.packed_to_unpacked_bb(1,gr.GR_MSB_FIRST)
		self.connect(self.source, self.unpacker_bb)
		self.connect(self.unpacker_bb, (self.rxpath, 0))
		self.connect(self.unpacker_bb, (self.rxpath, 1))
		# self.connect(self.source, self.unpacker_bb, self.rxpath)


# /////////////////////////////////////////////////////////////////////////////
#								   main
# /////////////////////////////////////////////////////////////////////////////

global n_rcvd, n_right

def main():
	global n_rcvd, n_right

	n_rcvd = 0
	n_right = 0
	
	def rx_callback(ok, payload):
		global n_rcvd, n_right
		(pktno,) = struct.unpack('!H', payload[0:2])
		n_rcvd += 1
		if pktno == 16912:
			n_right += 1

		print "ok = %5s  pktno = %4d  n_rcvd = %4d  n_right = %4d" % (
			ok, pktno, n_rcvd, n_right)
		# if n_right == 3000: print "%s\n" %(payload)


	# Create Options Parser:
	parser = OptionParser (option_class=eng_option, conflict_handler="resolve")
	# expert_grp = parser.add_option_group("Expert")

	parser.add_option("","--from-file", default=None,
					  help="input file of samples to demod", dest="from_file")
	parser.add_option("-r", "--repeat-file", action="store_true", 
					  help="Repeat file contents as input?", dest="repeat_file")
	parser.add_option("", "--ASM", default="1ACFFC1D",
					  help="Attached Sync Marker as hex string", dest="access_code")
	parser.add_option("", "--threshold", default=3, type="int",
					  help="max number of allowable bit errors in ASM detection", dest="threshold")
	parser.add_option("-v", "--verbose", action="store_true", default=False)
	parser.add_option("-d", "--decode27", action="store_true", default=False, dest="viterbi27")
	parser.add_option("-T", "--to-file", dest="to_file", default=None)

	(options, args) = parser.parse_args ()

	if len(args) != 0:
		parser.print_help(sys.stderr)
		sys.exit(1)

	if options.from_file is None:
		sys.stderr.write("You must specify --from-file\n")
		parser.print_help(sys.stderr)
		sys.exit(1)

	if options.viterbi27 and options.to_file is None:
		sys.stderr.write("You must specify --to-file when decoding\n")
		parser.print_help(sys.stderr)
		sys.exit(1)
		

	# build the graph
	tb = my_top_block(rx_callback, options)

	r = gr.enable_realtime_scheduling()
	if r != gr.RT_OK:
		print "Warning: Failed to enable realtime scheduling."

	tb.start()		# start flow graph
	tb.wait()		 # wait for it to finish

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass
