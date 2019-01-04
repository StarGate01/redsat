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
from math import floor

class doppler_calculator(gr.sync_block):
    C = 299792458. # light speed

    def __init__(self, 
        time=0., 
        freq=0., 
        samp_rate=0., 
        tle="", 
        location=None,
        #interpolated=True,
        dbg=True):
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

        self.interpolated = True # interpolated

        self.current_time = None
        if time != 0.: # avoid exception at design time
            self.last_freq = self.get_doppler_freq_intp(0)
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
            d_f = None
            for tag in tags:
                #if tag.key == pmt.intern("DopplerUpdate"):         
                i = tag.offset - nread                
                d_f = self.get_doppler_freq_intp(tag.offset) #if self.interpolated else self.get_doppler_freq(tag.offset)
                output_items[0][i:] = d_f
                
                if self.dbg:
                    print("n", gmtime(self.time + tag.offset/self.samp_rate), d_f)

            self.last_freq = d_f
        
        return num_input_items

    def get_doppler_freq(self, time):
        self.obs.date = strftime('%Y/%m/%d %H:%M:%S', gmtime(time))
        self.sat.compute(self.obs)
        doppler = (self.freq - self.sat.range_velocity * self.freq / self.C)
        return doppler

    # linear interpolation between full seconds
    def get_doppler_freq_intp(self, offset):
        new_time = self.time + float(offset)/float(self.samp_rate)

        if self.current_time is None or floor(new_time) != self.current_time:
            self.current_time = floor(new_time)

            self.current_doppler = self.get_doppler_freq(self.current_time)
            self.next_doppler = self.get_doppler_freq(self.current_time + 1)

        return self.current_doppler + (self.next_doppler - self.current_doppler) * (new_time - self.current_time)

        