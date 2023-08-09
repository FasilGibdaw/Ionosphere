# pip install fluids, and compile the hwm fortran codes as explained in the doc of fluids package at
# https://fluids.readthedocs.io/fluids.atmosphere.html#rfc3966d4cedd-1
import matplotlib.pyplot as plt
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature
import fluids
import numpy as np
import cartopy.crs as ccrs
import warnings
warnings.filterwarnings("ignore")
projection = ccrs.PlateCarree()
# N is the meridional and E is the zonal winds
la = np.arange(-90, 90, 1)
lo = np.arange(-180, 180, 2)
E = np.zeros((len(lo), len(la)))
N = np.zeros((len(lo), len(la)))
for i in range(len(la)):
    for j in range(len(lo)):
        n, e = fluids.atmosphere.hwm14(
            130*1000, latitude=la[i], longitude=lo[j], day=118, seconds=12*60*60, geomagnetic_disturbance_index=35)
        E[j, i] = e
        N[j, i] = n
fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, zorder=100)
#ax.add_feature(cfeature.BORDERS, zorder=100)
ax.add_feature(cfeature.LAKES, edgecolor='black', facecolor='none', zorder=11)
cs1 = ax.pcolor(lo, la, N,
                transform=ccrs.PlateCarree(), cmap='RdBu_r', vmin=-150, vmax=150)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                  linewidth=1, color='black', alpha=0.3, linestyle='--')
ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
#ax.add_feature(cfeature.LAKES, edgecolor='black', facecolor='none')
ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
ax.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
plt.colorbar(cs1, shrink=0.45, label='Meridional wind (m/s)')

ax1 = fig.add_subplot(1, 2, 2, projection=ccrs.PlateCarree())
ax1.add_feature(cfeature.COASTLINE, zorder=100)
#ax.add_feature(cfeature.BORDERS, zorder=100)
ax1.add_feature(cfeature.LAKES, edgecolor='black', facecolor='none', zorder=11)
cs2 = ax1.pcolor(lo, la, E,
                 transform=ccrs.PlateCarree(), cmap='RdBu_r', vmin=-150, vmax=150)
g2 = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                   linewidth=1, color='black', alpha=0.3, linestyle='--')
ax1.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
ax1.yaxis.set_major_formatter(LATITUDE_FORMATTER)
#ax.add_feature(cfeature.LAKES, edgecolor='black', facecolor='none')
ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
ax1.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
plt.colorbar(cs2, shrink=0.45, label='Zonal wind (m/s)')
plt.tight_layout()
plt.show()
