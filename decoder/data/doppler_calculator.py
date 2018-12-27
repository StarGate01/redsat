"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr
import pmt
import ephem
from time import gmtime, strftime

class doppler_calculator(gr.sync_block):
    C = 299792458. # light speed

    def __init__(self, 
        time=0., 
        freq=145.95e6, 
        samp_rate=128000, 
        tle="MOVE-II;1 43774U 18099S   18340.66044376  .00001644  00000-0  15648-3 0  9996;2 43774  97.7715  49.7845 0011035 250.7436 273.4950 14.94768966   423;", 
        location=None):
        #lat=0., lon=0., elv=0.): 
        gr.sync_block.__init__(
            self,
            name='Doppler calculator',
            in_sig=[np.complex64],
            out_sig=[np.float32]
        )
        self.time = time
        self.samp_rate = samp_rate       
        self.freq = freq        
                
        self.obs = ephem.Observer()        
        if location is not None:
            self.obs.lat = location.lat
            self.obs.lon = location.lon
            self.obs.elevation = location.elv

        tle_data = tle.split(";")
        self.sat = ephem.readtle(tle_data[0], tle_data[1], tle_data[2])

    def work(self, input_items, output_items):        
        num_input_items = len(input_items[0])

        nread = self.nitems_read(0)
        tags = self.get_tags_in_range(0, nread, nread+num_input_items)
        for tag in tags:            
            i = tag.offset - nread
            output_items[0][i:] = self.get_doppler_freq(tag.offset)
            
            #print pmt.pmt_symbol_to_string(tag.key)
            #print pmt.pmt_symbol_to_string(tag.value)
            #self.key = pmt.pmt_symbol_to_string(tag.key)    

        return len(output_items[0])

    def get_doppler_freq(self, offset):        
        self.obs.date = strftime('%Y/%m/%d %H:%M:%S', gmtime(self.time + offset/self.samp_rate))
        self.sat.compute(self.obs)
        doppler = (self.freq - self.sat.range_velocity * self.freq / self.C)
        return doppler