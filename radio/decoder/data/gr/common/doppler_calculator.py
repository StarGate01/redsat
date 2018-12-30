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
        freq=0., 
        samp_rate=0., 
        tle="", 
        location=None,
        dbg=True):
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
            self.obs.lat = str(location.lat)
            self.obs.lon = str(location.lon)
            self.obs.elevation = float(location.elv)

        tle_data = tle.split(",")
        if len(tle_data) >= 3:
            self.sat = ephem.readtle(tle_data[0], tle_data[1], tle_data[2])
        elif len(tle) > 0:
            raise ValueError("TLE string should have three entries separated by commas")
        else:
            pass

        if time != 0.:
            self.last_freq = self.get_doppler_freq(0)
        else:
            self.last_freq = freq

        self.dbg = dbg
        if dbg:
            print "time: ", self.time
            print "freq:", self.freq
            if location is not None:
                print "lat, lon, elv:", location.lat, location.lon, location.elv
            print "obs:", self.obs

    def work(self, input_items, output_items):        
        num_input_items = len(input_items[0])

        nread = self.nitems_read(0)
        tags = self.get_tags_in_range(0, nread, nread+num_input_items)

        output_items[0][:] = self.last_freq
        if len(tags) > 0:
            for tag in tags:            
                i = tag.offset - nread
                d_f = self.get_doppler_freq(tag.offset)
                output_items[0][i:] = d_f
                
                if self.dbg:
                    print(gmtime(self.time + tag.offset/self.samp_rate), d_f)

                #print pmt.pmt_symbol_to_string(tag.key)
                #print pmt.pmt_symbol_to_string(tag.value)
                #self.key = pmt.pmt_symbol_to_string(tag.key)    

            self.last_freq = self.get_doppler_freq(tags[-1].offset)
        
        return num_input_items

    def get_doppler_freq(self, offset):        
        self.obs.date = strftime('%Y/%m/%d %H:%M:%S', gmtime(self.time + offset/self.samp_rate))
        self.sat.compute(self.obs)
        doppler = (self.freq - self.sat.range_velocity * self.freq / self.C)
        return doppler