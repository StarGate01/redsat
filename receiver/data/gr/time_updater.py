"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr
import time

# lambda t: self.set_start_time(t)

class blk(gr.sync_block):
    def __init__(self, callback=None):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='First packet probe',
            in_sig=[np.complex64],
            out_sig=[]
        )
        
        self.time = None
        self.callback = callback

        print(self.callback)
        

    def work(self, input_items, output_items):        
        if self.time is None:
            self.time = time.time()
            if self.callback is not None:
                print('calling callback to set time:', self.time)
                self.callback(self.time)
        return 0