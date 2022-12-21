import pandas as pd
import matplotlib.pyplot as plt
import datetime
#####
import numpy as np


def moving_avg(data, window_size):  # moving average
    nbackward = window_size//2
    if (window_size % 2) == 0:
        nforward = nbackward-1
    else:
        nforward = nbackward
    length = len(data)
    data_avg = np.zeros(data.shape)
    for i in range(length):
        lo = max([0, i-nbackward])
        hi = min(length, i+nforward)
        data_avg[i] = np.mean(data[lo:hi])
    return data_avg


####
df = pd.read_table(
    './Kp_ap_Ap_SN_F107_since_1932.txt', header=39, sep='\s+')
time = [datetime.datetime(y, m, d) for y, m, d in zip(
    df['#YYY'].values, df['MM'].values, df['DD'].values)]

# df.head()
fig = plt.figure(1, figsize=(15, 3))
plt.plot(time, df['SN'], ls='none', marker='.',
         markersize=3, label='Daily SSN')
# plt.plot(time,df['SN'].rolling(365).mean(),'r')
plt.plot(time, moving_avg(df['SN'].values, 30),
         '.k', markersize=3, label='Monthly averaged SSN')
plt.plot(time, moving_avg(df['SN'].values, 365),
         'r', label='Yearly averaged SSN')
plt.ylim(0, df['SN'].max())
plt.xlim(time[0],)
plt.legend(frameon=False)
plt.xlabel('Year')
plt.title('Sun Spot number since 1932')
plt.ylabel('Sun Spot number (#)')
plt.grid()
plt.tight_layout()
plt.savefig('SSN_1932_to_present.png')
plt.show()
