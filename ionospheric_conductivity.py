# program to calculate Pedersen (sigma_p), Hall (sigma_h) and parallel (sigma_0) conductivities and others
# developed by Fasil Tesema
# the calculaton of the conductivties is based on the Michael C. Kelley(2009) second edition book
# packages needed (install by using "pip install igrf iri2016 msise00")
# igrf: https://github.com/space-physics/igrf
# IRI2016: https://github.com/space-physics/iri2016
# msise00: https://github.com/space-physics/msise00
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import igrf
from iri2016.base import IRI
import msise00
import warnings
warnings.filterwarnings("ignore")
# mass of O+ ion [kg], whcih is the abundant ion in the ionosphere
Mi = 15.999/6.022e23/1e3
Me = 9.10938188e-31  # mass of the electron
q = 1.6021765e-19  # charge of the ion or it can be charge of an electron if it is negative
# date to calculate conductivity in the form of "datetime(YYYY,MM,DD,HH,mm)"
dn = datetime(2012, 4, 2, 10, 0)
lon = 37.36  # longitude in degrees (here for Bahir Dar)
lat = 11.6  # latitude in degrees (here for Bahir Dar)
x = IRI(dn, [60, 995, 5], lat, lon)
alt = x.alt_km.data  # the altitude range to be calculated in km
note = open('conductivity_trial' + '.txt', 'w')
note.write(
    'Altitude(km) sigma_p sigma_h sigma_0 kappa_i kappa_e nu_in nu_en omega_e omega_i\n')
for j in range(len(alt)):
    atmos = msise00.run(time=dn, altkm=alt[j], glat=lat, glon=lon)
    mag = igrf.igrf(dn, glat=lat, glon=lon, alt_km=alt[j])
    N2 = float(atmos.N2)
    O = float(atmos.O)
    O2 = float(atmos.O2)
    B = float(mag.total)*1e-9
    ne = x.ne.data[j]
    n = ne
    Te = x.Te.data[j]
    # sum of all the nutral density particles
    density_sum = (N2+O+O2)
    n_n = density_sum
    # multiplying by Avogadro's number 6.0221415e23 to get A in atomic mass unit (amu)
    omega_e = q*B/Me
    omega_i = q*B/Mi
    # colliion coefficient for ion-neutral collision (density in m^-3) (somewhere)
    nu_in = 4.34e-16*N2+4.28e-16*O2+2.44e-16*O
    # colliion coefficient for electron-neutral collision
    nu_en = 5.4e-16*n_n*np.sqrt(Te)  # colliion coefficient for electrons
    # if you want add electron ion collision (see kelly book) n is changed back to cm^-3 unit
    # colliion coefficient for electron-ion collision
    kappa_i = q*B/(Mi*nu_in)
    kappa_e = -q*B/(Me*nu_en)
    bi = q/(Mi*nu_in)
    be = -q/(Me*nu_en)  # mobility coefficients
    # Pedersen conductivity
    sigma_p = (n*(q/B)*((kappa_i/(1+kappa_i**2)) - (kappa_e/(1+kappa_e**2))))
    sigma_h = (n*(q/B)*((kappa_e**2./(1+kappa_e**2)) -
               ((kappa_i)**2./(1+kappa_i**2))))  # Hall conductivity
    sigma_0 = (n*(q/B)*(kappa_i-kappa_e))  # Parallel conductivity
    line = "{:8.2f} {:8.20f} {:8.20f} {:8.20f} {:8.20f} {:8.20f} {:8.20f} {:8.20f} {:8.20f} {:8.20f}\n".format(
        alt[j], sigma_p, sigma_h, sigma_0, kappa_i, kappa_e, nu_in, nu_en, omega_e, omega_i)
    note.write(line)
note.close()
# plotting
# read the data from the calculated and saved txt file above
data = np.loadtxt('conductivity_trial.txt', skiprows=1)
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
ax[0].semilogx(data[:, 1], data[:, 0], label='Pedersen')
ax[0].semilogx(data[:, 2], data[:, 0], label='Hall')
ax[0].semilogx(data[:, 3], data[:, 0], label='Parallel')
ax[0].set_ylim([80, 500])
ax[0].legend(frameon=False)
ax[0].set_xlabel('Conductivity (mho/m)')
ax[0].set_ylabel('Altitude (km)')

ax[1].semilogx(abs(data[:, 5]), data[:, 0], label='Ke')
ax[1].semilogx(data[:, 4], data[:, 0], label='Ki')
ax[1].legend(frameon=False)
ax[1].set_ylim([80, 250])
ax[1].set_ylabel('Altitude (km)')
ax[1].set_title(dn.strftime("%m/%d/%Y, %H:%M:%S") + ' at BahirDar')
ax[2].semilogx(data[:, 6], data[:, 0], label=r'$\nu_{in}$')
ax[2].semilogx(data[:, 7], data[:, 0], label=r'$\nu_{en}$')
ax[2].semilogx(data[:, 8], data[:, 0], label=r'$\Omega_{e}$')
ax[2].semilogx(data[:, 9], data[:, 0], label=r'$\Omega_{i}$')
ax[2].legend(frameon=False)
ax[2].set_xlabel('Frequency (Hz)')
ax[2].set_ylabel('Altitude (km)')
ax[2].set_ylim([80, 250])
plt.tight_layout()
plt.show()
# plt.savefig('conductivity_cal.pdf')
