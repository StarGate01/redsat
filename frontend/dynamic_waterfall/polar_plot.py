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

    def get_overpass(self):
        pass

    def generate_svg(self):
        fig, ax = plt.subplots(figsize=(2,2), subplot_kw=dict(projection='polar'))

        az, alt = [], []
        for t in self.t:
            pos = self.get_position(t)
            az.append(pos["az"])
            alt.append(pos["alt"])

        az, alt = np.array(az), np.array(alt)
        ah = alt > 0  # above horizon
        p_az, r = az*np.pi/180, 90-alt
        p_az, r = p_az[ah], r[ah]

        ax.plot(p_az, r)

        ax.scatter(p_az[0], r[0], color='C2', zorder=3)
        ax.scatter(p_az[-1], r[-1], color='C3', zorder=3)

        ax.set_rmax(90)
        ax.set_rgrids([45, 90], ('', ''))
        ax.set_thetagrids(range(0, 360, 90), ('N', 'E', 'S', 'W'))
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location("N")
        ax.grid(True)

        fig.tight_layout()
        f = io.BytesIO()
        fig.savefig(f, format="svg")
        return f.getvalue()