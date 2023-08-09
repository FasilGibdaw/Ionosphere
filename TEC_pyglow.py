# calculate the TEC by integrating electron density from IRI-2016 using pyglow package
# https://github.com/timduly4/pyglow
from pyglow.pyglow import Point
from datetime import datetime
from multiprocessing import Pool
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from itertools import repeat
# t1=_np.append(t_list,t_list2);t1=t1[32:-41];


def main():
    dt1 = dt.datetime(2013, 2, 1)
    dt2 = dt.datetime(2013, 2, 1, 23, 59, 59)
    time_step = 60
    delta = dt2 - dt1
    delta_sec = delta.days * 24 * 60 * 60 + delta.seconds
    time = [dt1 + dt.timedelta(0, t) for t in range(0, delta_sec, time_step)]
    tec = TEC(dt1, dt2, 11.6, 37.4, time_step=time_step)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(time, tec)
    locator = mdates.AutoDateLocator(minticks=4, maxticks=10)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    plt.show()


def TEC_alt(dn, lat, lon):
    ne2 = []
    alt = np.arange(60, 1000, 10)
    for j in range(len(alt)):
        pt = Point(dn, lat, lon, alt[j])
        pt.run_iri(version=2016)
        ne1 = pt.ne
        ne2 = np.append(ne2, ne1)
    # here ne is in cm^-3, and TEC unit is 1e16/m^2,
    # the factor 10 is due to the change in height (alt step) in the integration, see the alt definition above
    tec = np.sum(ne2)*10*1e5*1e-12  # putting tec in TEC units
    return tec


def TEC(dt1, dt2, lat, lon, time_step=60):

    # dt1 = dt.datetime(2010, 4, 1)
    # dt2 = dt.datetime(2010, 4, 1, 23, 59, 59)

    # time_step = 60 # secoonds
    delta = dt2 - dt1

    delta_sec = delta.days * 24 * 60 * 60 + delta.seconds

    res = [dt1 + dt.timedelta(0, t) for t in range(0, delta_sec, time_step)]
    with Pool() as pool:
        # result=pool.map(func=TEC_alt,iterable=res)
        # result=pool.map(partial(prep_atVSC, cellid=cellid), files)
        result = pool.starmap(TEC_alt, zip(res, repeat(lat), repeat(lon)))
    return result


if __name__ == "__main__":
    main()
