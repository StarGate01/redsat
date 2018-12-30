"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import time


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, rate=128000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Time Tagger',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.rate = rate
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
       
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        num_input_items = len(input_items[0])

        nread = self.nitems_read(0)
        tags = self.get_tags_in_range(0, nread, nread+num_input_items)

        output_items[0][:] = input_items[0]
        num_new_tags = (nread+num_input_items) // self.rate - nread // self.rate
        for i in range(num_new_tags):
            self.add_item_tag(
                0, 
                (nread // self.rate + (i+1)) * self.rate, 
                pmt.intern("time"),
                pmt.from_double(time.time()))


        #for tag in tags:            
            
        #    output_items[0][:] = input_items[0]
            
        #    print("update time:", time.time() )
            
            #self.remove_item_tag(0, tag)
        #    tag.key = pmt.to_pmt("time")
        #    tag.value = pmt.to_pmt(time.time())
        #    self.add_item_tag(0, tag)
            #if tag.offset == 0:

            
        return num_input_items
