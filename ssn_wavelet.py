import numpy as np
import pywt
import matplotlib.pyplot as plt
import random
import pycwt as cwlet
#url = 'http://paos.colorado.edu/research/wavelets/wave_idl/nino3sst.txt'
#sst = np.genfromtxt(url, skip_header=19)
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
#wavelet = 'cgau8'

scales = np.arange(1, 128)

[cfs, frequencies] = pywt.cwt(sst, scales, wavelet, dt)

cfs, scales, frequencies, coi, fft, fftfreqs = cwlet.cwt(
    sst, dt, 'cmor', freqs=frequencies)
power = (abs(cfs)) ** 2

period = 1. / frequencies
# levels=np.linspace(0.1,10,30)
levels = [0.01, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8]
fig, ax = plt.subplots(2, 1, constrained_layout=True, figsize=(8, 6))

ax[0].plot(time, sst)
ax[0].set_xlim([1700, 2021])
ax[0].set_ylabel('SSN')
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
cycle = 11*np.ones(sst.shape)
# ax[1].plot(time,np.log2(coi))
ax[1].plot(time, np.log2(cycle), '--k', alpha=0.5)
ax[1].set_ylim(ylim[0], 0)
# plt.tight_layout()
plt.savefig('SunSpotNumber.pdf')
