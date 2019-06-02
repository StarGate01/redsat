#
# TODO this script has to be cleaned up!
#

import numpy as np
from numpy.fft import fftshift
from scipy import signal
from skimage.transform import rescale

import holoviews as hv
from holoviews import opts
from holoviews.streams import RangeXY
from holoviews.operation.datashader import regrid, datashade
from bokeh.layouts import layout, row

from datetime import datetime

import xarray as xr
import datashader.reductions as dsr

from threading import Lock
from os.path import splitext, join, basename, getsize
from configparser import ConfigParser
import traceback


#hv.extension('bokeh') # use this for Jupyter notebooks
renderer = hv.renderer('bokeh').instance(mode='server')

lock = Lock() # lock to prevent concurrent calls to spectrogram, maybe put in create_doc though to not block out multiple users

def next_power_of_2(x):
    return 1 if x == 0 else 2**np.ceil(np.log2(x))

freq_units = {1: 'Hz', int(1e3): 'kHz', int(1e6): 'MHz', int(1e9): 'GHz'}
freq_units_names = {v: k for k, v in freq_units.items()}
def format_freq(value):
    for freq_u in sorted(freq_units.keys(), reverse=True):
        if freq_u < value:
            return "{} {}".format(value / freq_u, freq_units[freq_u])
    return "{} {}".format(value, freq_units[1])

def create_doc(doc, data_dir):

    def get_spectrogram(s0=None, s1=None, size=1024, overlap=1./8, zfill=1, mode='psd'):
        s_size = np.dtype(np.complex64).itemsize
        
        if s1 is None and s0 is None:
            ds = None
        elif s1 is None:
            ds = None
        elif s0 is None:
            ds = np.abs(s1)
        else:
            ds = np.abs(s1 - s0)
        
        if ds is not None and s0 is not None:
            flen = getsize(join(data_dir, file))
            print("file size: {} bytes".format(flen))
            if (ds + s0) * s_size > flen:
                ds = flen - s0 * s_size
            
        samples = np.memmap(join(data_dir, file), dtype='complex64', mode='r', offset=s0 * s_size, shape=(ds,) if ds else None)

        if ds is None:
            ds = len(samples)
        
        if ds / size > (res + 0.5) * height:
            noverlap = -int(float(size) * float(ds) / size / height / res)
        else:
            noverlap = size // (1./overlap)
        
        f,t,S = signal.spectrogram(
            samples, samp_rate, 
            nperseg=size, 
            nfft=int(next_power_of_2(size)*int(zfill)), 
            noverlap=noverlap, 
            return_onesided=False,
            scaling='density',
            mode=mode) #
        
        f = fftshift(f)
        S = fftshift(S, axes=(0,))

        if mode == 'psd':
            S = 10*np.log10(S)
            
        return f, t, S, samples
    
    def get_spectrogram_img(z_min, z_max, tf_r, zfill, overlap, show_realfreq, freq_unit, x_range, y_range):
        lock.acquire()

        show_realfreq = bool(show_realfreq)        
        
        hv_image = None
        try:   
            print("y_range:", y_range, type(y_range))
            
            if type(y_range[0]) != float:
                if np.issubdtype(y_range[0], np.datetime64) and time is not None:
                    y_range = [(y - np.datetime64(time)).astype('timedelta64[us]').astype('float') / 1e6 for y in y_range]
                #elif np.issubdtype(y0, np.timedelta64):
                #    y0, y1 = [y.astype('timedelta64[s]').astype('float') for y in [y0,y1]]
                
            # tranform back to relative frequency if required

            print(doc.session_context.show_realfreq, x_range)
            
            last_freq_unit = doc.session_context.freq_unit       
            x_range = [x * freq_units_names[last_freq_unit] for x in x_range]                        
            
            if doc.session_context.show_realfreq:
                x_range = [(x - freq) for x in x_range]
            
            print(doc.session_context.show_realfreq, "after transform", x_range)            
            
            (x0, x1), (y0, y1) = x_range, y_range
            
            #print("y0 dtype:", y0.dtype)
                
            s0,s1 = sorted([min(max(int(yr * samp_rate),0), total_samples) for yr in [y0,y1]])

            scale = samp_rate / np.abs(x_range[1] - x_range[0])

            size = int(width * scale) # required freq resolution to fulfill zoom level

            ds = np.abs(s1 - s0) # number of samples covered at the current zoom level
            if ds / size < height:
                size = int(np.sqrt(ds * scale * 10**tf_r))
            
            f,t,S,samples = get_spectrogram(s0, s1, size=size, overlap=overlap, mode=mode, zfill=zfill if size < res * width else 1)
            t += max(min(y0,y1),0)

            f_range = (x0 <= f) & (f <= x1)
            image = S[f_range,:]
            f = f[f_range]
            
            #if ds / size > height:
            #    image = signal.resample(image, height*2, axis=0)

            print(image.shape)
            
            if intp_enabled:
                ratio = np.array(image.shape, dtype=np.float) / np.array((height*res, width*res))
                if np.min(ratio) < 1:
                    scale = np.max(np.abs(image)) # normalization factor for image because rescale needs that
                    image = rescale(image / scale, 1. / np.min(ratio), order=1) * scale

                    f = signal.resample(f, image.shape[0])
                    t = signal.resample(t, image.shape[1])
                    
                    print("after resampling: ", image.shape)

            del samples
            #image = hv.Image(image, bounds=(x0, y0, x1, y1)).redim.range(z=(z_min, z_max)) # TODO get exact values in bounds
            
            if show_realtime and time is not None:
                t = np.datetime64(time) + np.array(t*1e6).astype('timedelta64[us]')
            #else:
            #    t = (t*1e6) #.astype('timedelta64[us]')                
            
            if show_realfreq:
                f += freq
            f /= freq_units_names[freq_unit]
            
            #image = image.astype('float16') # trying to reduce network bandwidth...
            
            print("image dtype:", image.dtype)
            
            #hv_image = hv.Image(np.flip(image, axis=1), bounds=(min(f), max(t), max(f), min(t))) \
            hv_image = hv.Image(xr.DataArray(image, coords=[f,t], dims=['f','t'], name='z'), ['f','t'], 'z') \
                .options(
                    xlabel="Frequency [{}]".format(freq_unit),
                    ylabel="Time " + '[s]' if not show_realtime else '') \
                .redim.range(z=(z_min, z_max))
            
            if doc.session_context.show_realfreq != show_realfreq or doc.session_context.freq_unit != freq_unit:
                hv_image = hv_image \
                    .redim.range(f=(min(f), max(f))) \
                    .redim.range(t=(min(t), max(t)))
                print("redimming axis range")
            
            doc.session_context.show_realfreq = show_realfreq
            doc.session_context.freq_unit = freq_unit
            
        except Exception as e:
            print("Exception in image generation:", e)
            print(traceback.format_exc())

        lock.release()
        return hv_image

    def get_param(name, default, t=str):
        try:
            args = doc.session_context.request.arguments
            if t == str:            
                p = str(args.get(name)[0], 'utf-8')
            else:
                p = t(args.get(name)[0])
        except:
            p = default
        return p

    time = None
    freq = 0
    
    file = basename(get_param('file', '', str))
    skip = get_param('skip', 0, int)
    keep = get_param('keep', None, int)
    
    # low resolution for raspberry
    width, height = get_param('width', 600, int), get_param('height', 500, int)
    res = get_param('res', 1.5, float)
    ds_enabled = get_param('ds', None, str) # datashade option (default: avg)
    intp_enabled = get_param('intp', 0, int) # interpolation enable flap
    show_realtime = bool(get_param('rt', 0, int)) # show real time on vertical axis

    mode = get_param('mode', 'psd', str)

    t_range = get_param('t', None, str)
    f_range = get_param('f', None, str)

    if t_range is not None:
        try:
            parts = t_range.split(",")
            if len(parts) == 2:
                t_range = list(map(float, parts))
        except:
            pass

    if f_range is not None:
        try:
            parts = f_range.split(",")
            if len(parts) == 2:
                f_range = list(map(float, parts))
            elif len(parts) == 1:
                _f = abs(float(parts[0]))
                f_range = (-_f, _f)
        except:
            pass

    if file.endswith(".meta"):
        config = ConfigParser()
        config.read(join(data_dir, file))
        
        file = splitext(file)[0] + ".raw"
        samp_rate = int(config['main']['samp_rate'])
        freq = float(config['main']['freq'])
        time = datetime.fromtimestamp(float(config['main']['time']))
    else:
        samp_rate = get_param('samp_rate', 128000, int)

    f,t,S,samples = get_spectrogram(s0=skip*samp_rate, s1=keep*samp_rate if keep else None, size=width, mode=mode)
    total_samples = len(samples)
    
    del samples
    
    # default is True
    if show_realtime and time is not None:
        t = np.datetime64(time) + np.array(t).astype('timedelta64[s]')

    doc.session_context.show_realfreq = False
    doc.session_context.freq_unit = freq_units[1000]
    
    range_stream = RangeXY(
        x_range=tuple(x / freq_units_names[doc.session_context.freq_unit] for x in
                      ((min(f_range), max(f_range)) if f_range else (min(f), max(f)))),
        y_range=(max(t_range), min(t_range)) if t_range else (max(t), min(t))) # transient=True
    
    z_range = (np.min(S), np.max(S))
    z_init = np.percentile(S, (50,100))    
    
    dmap = hv.DynamicMap(get_spectrogram_img, streams=[range_stream], kdims=[
        hv.Dimension('z_min', range=z_range, default=z_init[0]), hv.Dimension('z_max', range=z_range, default=z_init[1]),
        hv.Dimension('tf_r', label='Time-Frequency pixel ratio', range=(-10.,10.), default=0.),
        hv.Dimension('zfill', label='Zero-filling factor', range=(1, 10), default=2),
        hv.Dimension('overlap', label='Overlap factor', range=(-1.,1.), default=1./8),
        #hv.Dimension('show_realtime', label='Show real time on vertical axis', range=(0,1), default=0),
        hv.Dimension('show_realfreq', label='Show real frequency', range=(0,1), default=int(doc.session_context.show_realfreq)),
        hv.Dimension('freq_unit', label='Frequency unit', values=list(map(lambda x: freq_units[x], sorted(freq_units.keys()))), default=doc.session_context.freq_unit),
        #hv.Dimension('mode', label='Spectrogram mode', values=['psd', 'angle', 'phase', 'magnitude'], default='psd')
    ]).options(
        framewise=True, # ???
        ) #.redim.range(z=z_init)
    #dmap = dmap.opts(opts.Image(height=height, width=width))

    if ds_enabled != None:
        print("datashade enabled: yes")
        if ds_enabled == "" or ds_enabled=="mean":
            ds_enabled = dsr.mean
        elif ds_enabled == "max":
            ds_enabled = dsr.max
        else:
            print("warning: invalid option for datashade. using default value: mean")
            ds_enabled = dsr.mean
        dmap = regrid(dmap, aggregator=ds_enabled, interpolation='linear', upsample=True, height=height*2, width=width*2) # aggregation=dsr.max
    
    #dmap = dmap.hist(num_bins=150, normed=False)
    
    dmap = dmap.opts(
        opts.Image(cmap='viridis', framewise=True, colorbar=True, height=height, width=width, tools=['hover'],
                   title='{}, {} {} sps'.format(time.strftime('%Y-%m-%d %H:%M:%S') if time else 'Time unknown', format_freq(freq), samp_rate)),
        opts.Histogram(framewise=False, width=150)
    )

    #plot = renderer.get_plot(hist, doc).state
    #widget = renderer.get_widget(hist, None, position='right').state
    
    #hvobj = layout([plot, widget])
    
    #plot = layout([renderer.get_plot(hist, doc).state])
    #doc.add_root(plot)

    doc = renderer.server_doc(dmap, doc=doc)
    doc.title = 'Waterfall Viewer'

