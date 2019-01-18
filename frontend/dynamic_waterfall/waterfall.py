#
# TODO this script has to be cleaned up!
#

import numpy as np
from numpy.fft import fftshift
from scipy import signal

import holoviews as hv
from holoviews import opts
from holoviews.streams import RangeXY
from holoviews.operation.datashader import regrid, datashade
from bokeh.layouts import layout, row

from skimage.transform import rescale

import xarray as xr
import datashader.reductions as dsr

from bokeh.plotting import curdoc

from threading import Lock
from os.path import splitext, join
from configparser import ConfigParser

#hv.extension('bokeh')
renderer = hv.renderer('bokeh').instance(mode='server')

lock = Lock()

def next_power_of_2(x):
    return 1 if x == 0 else 2**np.ceil(np.log2(x))

def get_spectrogram(samples, samp_rate, size=1024, noverlap=None, zfill=1):
    f,t,S = signal.spectrogram(
        samples, samp_rate, 
        nperseg=size, 
        nfft=int(next_power_of_2(size*zfill)), 
        noverlap=noverlap, 
        return_onesided=False) # scaling='spectrum'
    return fftshift(f), t, 10*np.log10(fftshift(S, axes=(0,))).T

def create_doc(doc, data_dir):

    def get_spectrogram_img(z_min, z_max, tf_r, x_range, y_range, zfill, overlap):
        lock.acquire()

        image = None
        try:
            (x0, x1), (y0, y1) = x_range, y_range
            s0,s1 = sorted([min(max(int(yr * samp_rate),0),len(samples)) for yr in y_range])

            scale = samp_rate / np.abs(x_range[1] - x_range[0])

            size = int(width * scale)

            ds = np.abs(s1 - s0)
            if ds / size < height:
                size = int(np.sqrt(ds * scale * 10**tf_r))

            if ds / size > 2 * height:
                noverlap = -size * int(float(ds) / size / height / 2)
            else:
                noverlap = size // (1./overlap)       

            f,t,S = get_spectrogram(samples[s0:s1], samp_rate, size=size, noverlap=noverlap, zfill=zfill)
            t += max(min(y0,y1),0)

            image = S[:,(x0 < f) & (f < x1)]

            #if ds / size > height:
            #    image = signal.resample(image, height*2, axis=0)

            print(image.shape)

            if ds_enabled:
                array = xr.DataArray(image, coords=[t,f[(x0 < f) & (f < x1)]], dims=['x','y'], name="z")
                image = hv.Image(array, ['y','x'], 'z').redim.range(z=(z_min, z_max))
            elif intp_enabled:
                ratio = np.array(image.shape, dtype=np.float) / np.array((height, width))
                if np.min(ratio) < 1:
                    scale = np.max(np.abs(image))
                    image = rescale(image / scale, 1. / np.min(ratio), order=1) * scale

                image = np.flip(image,0)
                print(image.shape)
            else:
                image = np.flip(image,0)

            image = hv.Image(image, bounds=(x0, y0, x1, y1)).redim.range(z=(z_min, z_max)) # TODO get exact values in bounds
        except Exception as e:
            print(e)

        lock.release()
        return image

    def get_param(name, default, t=str):
        print(doc.session_context.request.arguments)
        try:
            args = doc.session_context.request.arguments
            if t == str:            
                p = str(args.get(name)[0], 'utf-8')
            else:
                p = t(args.get(name)[0])
        except:
            p = default
        return p

    file = get_param('file', '', str)
    offset = get_param('offset', 0, int)

    # low resolution for raspberry
    width, height = get_param('width', 600, int), get_param('height', 500, int)
    ds_enabled = get_param('ds', 0, int) # datashade enable flap
    intp_enabled = get_param('intp', 0, int) # interpolation enable flap


    if file.endswith(".meta"):
        config = ConfigParser().read(file)
        file = splitext(file)[0] + ".raw"
        samp_rate = config['main']['samp_rate']
    else:
        samp_rate = get_param('samp_rate', 128000, int)

    samples = np.memmap(join(data_dir, file), dtype='complex64', mode='r', offset=samp_rate * offset * np.dtype(np.complex64).itemsize) # shape=(samp_rate*300,)


    if len(samples) / width > 4 * height:
        noverlap = -width * int(float(len(samples)) / width / height / 2)
    else:
        noverlap = width // 8   

    f,t,S = get_spectrogram(samples, samp_rate, size=width, noverlap=noverlap)

    range_stream = RangeXY(x_range=(min(f), max(f)), y_range=(max(t), min(t)), transient=False) # transient=True
    # vdims=hv.Dimension('z', range=(1e-4,1))
    z_range = (np.min(S), np.max(S))
    z_init = np.percentile(S, (45,95))
    #z_init = z_range # for agg = max

    dmap = hv.DynamicMap(get_spectrogram_img, streams=[range_stream], kdims=[
        hv.Dimension('z_min', range=z_range, default=z_init[0]), hv.Dimension('z_max', range=z_range, default=z_init[1]),
        hv.Dimension('tf_r', range=(-10.,10.), default=0.),
        hv.Dimension('zfill', range=(1, 10), default=2),
        hv.Dimension('overlap', range=(-1.,1.), default=1./8)
    ]).options(
        framewise=True, # ???
        xlabel="Frequency [Hz]",
        ylabel="Time [s]") #.redim.range(z=z_init)
    #dmap = dmap.opts(opts.Image(height=height, width=width))

    if ds_enabled:
        dmap = regrid(dmap, aggregator=dsr.max, interpolation='linear', upsample=True, height=height*2, width=width*2) # aggregation=dsr.max

    #    .redim.range(z_min=z_range, z_max=(np.min(S)+1e-14, np.max(S)) )
    hist = dmap.hist(num_bins=150)

    hist.opts(
        opts.Image(cmap='viridis', framewise=False, colorbar=True, height=height, width=width), # title='Waterfall',
        opts.Histogram(framewise=True, width=150),
    ) # framewise=False

    #plot = renderer.get_plot(hist, doc).state
    #widget = renderer.get_widget(hist, None, position='right').state
    
    #hvobj = layout([plot, widget])
    
    #plot = layout([renderer.get_plot(hist, doc).state])
    #doc.add_root(plot)

    doc = renderer.server_doc(hist, doc=doc)
    doc.title = 'Waterfall Viewer'

