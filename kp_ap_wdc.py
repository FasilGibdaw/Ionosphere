# reading Kp Ap and SSN from the data provided in ftp://ftp.gfz-potsdam.de/pub/home/obs/kp-ap/wdc/yearly/

from datetime import datetime
import numpy as np


def kp_ap_wdc(fname):
    kp = {}
    ap = {}
    daily_kp = {}
    daily_ap = {}
    daily_SSN = {}
    with open(fname) as f:
        for x in f.readlines():
            year = int(x[0:2])
            if year < 40:  # need to change this is 2040....
                year = year + 2000
            else:
                year = year + 1900
            month = int(x[2:4])  # parse the line for month
            day = int(x[4:6])  # ... and the days
            kp[datetime(year, month, day, 0)] = int(x[12:14])/10.
            kp[datetime(year, month, day, 3)] = int(x[14:16])/10.
            kp[datetime(year, month, day, 6)] = int(x[16:18])/10.
            kp[datetime(year, month, day, 9)] = int(x[18:20])/10.
            kp[datetime(year, month, day, 12)] = int(x[20:22])/10.
            kp[datetime(year, month, day, 15)] = int(x[22:24])/10.
            kp[datetime(year, month, day, 18)] = int(x[24:26])/10.
            kp[datetime(year, month, day, 21)] = int(x[26:28])/10.

            ap[datetime(year, month, day, 0)] = int(x[31:34])
            ap[datetime(year, month, day, 3)] = int(x[34:37])
            ap[datetime(year, month, day, 6)] = int(x[37:40])
            ap[datetime(year, month, day, 9)] = int(x[40:43])
            ap[datetime(year, month, day, 12)] = int(x[43:46])
            ap[datetime(year, month, day, 15)] = int(x[46:49])
            ap[datetime(year, month, day, 18)] = int(x[49:52])
            ap[datetime(year, month, day, 21)] = int(x[52:55])
            daily_kp[datetime(year, month, day)] = int(x[28:31])
            daily_ap[datetime(year, month, day)] = int(x[55:58])
            daily_SSN[datetime(year, month, day)] = int(x[62:65])
    time, KP = zip(*daily_kp.items())
    _, AP = zip(*daily_ap.items())
    _, SSN = zip(*daily_SSN.items())
    return time, np.array(KP)/8, AP, SSN
