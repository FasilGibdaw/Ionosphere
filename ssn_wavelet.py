import numpy as np
import pywt  # https://pywavelets.readthedocs.io/en/latest/
import matplotlib.pyplot as plt
import pycwt as cwlet  # https://pycwt.readthedocs.io/en/latest/


#####

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
ssn = np.loadtxt('./SN_y_tot_V2.0.txt')
sst = ssn[:, 1]
t0 = 1700
dt = 1  # In years

# We also create a time array in years.
N = sst.size
time = np.arange(0, N) * dt + t0

# time, sst = pywt.data.nino()
# dt = time[1] - time[0]

# Taken from http://nicolasfauchereau.github.io/climatecode/posts/wavelet-analysis-in-python/
wavelet = 'cmor1.5-1.0'
# wavelet = 'cgau8'

scales = np.arange(1, 128)

[cfs, frequencies] = pywt.cwt(sst, scales, wavelet, dt)

cfs, scales, frequencies, coi, fft, fftfreqs = cwlet.cwt(
    sst, dt, 'cmor', freqs=frequencies)
power = (abs(cfs)) ** 2

period = 1. / frequencies
# levels=np.linspace(0.1,10,30)
levels = [0.01, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8]
fig, ax = plt.subplots(2, 1, constrained_layout=True, figsize=(8, 6))

ax[0].plot(time, sst, label='Yearly SSN')
ax[0].plot(time, moving_avg(sst, 50), label='100 years periodic variation')
ax[0].set_xlim([1700, 2021])
ax[0].set_ylabel('Sunspot number (SSN)')
ax[0].legend(frameon=False)
s = ax[1].contourf(time, np.log2(period), np.log10(power), levels=100,
                   extend='both')

ax[1].set_title(
    '%s Wavelet Power Spectrum (dashed line = 11 years) ' % ('SSN'))
ax[1].set_ylabel('Period (years)')
Yticks = 2 ** np.arange(np.ceil(np.log2(period.min())),
                        np.ceil(np.log2(period.max())))
ax[1].set_yticks(np.log2(Yticks))
ax[1].set_yticklabels(Yticks)
ax[1].invert_yaxis()
ylim = ax[1].get_ylim()
ax[1].set_xlabel('Time (years)')
# plt.colorbar(s)
ax[1].axhline(np.log2(11), ls='--', color='k', alpha=0.5)  # 11 year cycle plot
ax[1].set_ylim(ylim[0], 0)
# plt.tight_layout()
plt.savefig('SunSpotNumber.png', dpi=800)
