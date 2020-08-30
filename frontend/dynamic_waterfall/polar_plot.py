import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import load, Loader, Topos, EarthSatellite
import datetime
import io
from os.path import dirname, join

#load = Loader(join(dirname(__file__), '../../persistent-data/config/skyfield-data'))
ts = load.timescale(builtin=True)


class PolarPlot:
    def __init__(self, tle, location, start_time, duration, N=25):
        self.tle = tle
        self.location = location
        t0 = start_time.timestamp()
        t1 = (start_time + datetime.timedelta(seconds=duration)).timestamp()
        self.t = np.linspace(t0, t1, N)

        self.location = Topos(
            latitude_degrees=location['lat'],
            longitude_degrees=location['lon'],
            elevation_m=location['elv']
        )
        self.sat = EarthSatellite(self.tle[1], self.tle[2], self.tle[0], ts)
        self.diff = self.sat - self.location

    def get_position(self, t):
        dt = datetime.datetime.utcfromtimestamp(t).replace(tzinfo=datetime.timezone.utc)
        alt, az, distance = self.diff.at(ts.from_datetime(dt)).altaz()
        return dict(alt=alt.degrees, az=az.degrees, distance=distance.km)

    def generate_svg(self):
        fig, ax = plt.subplots(figsize=(2,2), subplot_kw=dict(projection='polar'))

        #ax = fig.subplot(111, )
        az, alt = [], []
        for t in self.t:
            pos = self.get_position(t)
            az.append(pos["az"])
            alt.append(pos["alt"])
        print(az, alt)
        ax.plot(np.array(az)*np.pi/180, 90-np.array(alt))
        ax.set_rmax(90)
        ax.set_rgrids([45, 90], ('', ''))
        #ax.set_xticks(np.array([0,90,180,270])*np.pi/180)
        ax.set_thetagrids(range(0, 360, 90), ('N', 'E', 'S', 'W'))
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location("N")
        #ax.set_xtick_labels(["N", "E", "S", "W"])

        #ax.set_rlabel_position(-22.5)
        ax.grid(True)

        fig.tight_layout()
        f = io.BytesIO()
        fig.savefig(f, format="svg")
        return f.getvalue()