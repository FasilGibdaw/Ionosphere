# calculate the TEC by integrating electron density from IRI-2016
# using the package IRI2016: https://github.com/space-physics/iri2016
from datetime import datetime
from multiprocessing import Pool
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from itertools import repeat
import iri2016

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
    ax.set_ylabel('TEC (TECu)')
    # plt.grid()
    plt.show()


def TEC_alt(dn, lat, lon):
    x = iri2016.IRI(dn, [60, 1000, 5], lat, lon)
    x.ne.values[x.ne.values < 0] = np.nan
    return np.nansum(x.ne.values)*5000*1e-16


def TEC(dt1, dt2, lat, lon, time_step=60):

    #dt1 = dt.datetime(2010, 4, 1)
    #dt2 = dt.datetime(2010, 4, 1, 23, 59, 59)

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
