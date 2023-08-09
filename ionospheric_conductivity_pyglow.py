# program to calculate Pedersen (sigma_p), Hall (sigma_h) and parallel (sigma_0) conductivities
# developed by Fasil Tesema @ Bahir Dar university, Ethiopia November 10 2016
# the calculaton of the conductivties is based on the Michael C. Kelley(2009) second edition book
# pyglow package (https://github.com/timduly4/pyglow) is needed here besides the common packages like numpy
from datetime import datetime
import matplotlib.pyplot as plt
from pyglow.pyglow import Point
import numpy as np
# mass of O+ ion [kg], whcih is the abundant ion in the ionosphere
Mi = 15.999/6.022e23/1e3
Me = 9.10938188e-31  # mass of the electron
q = 1.6021765e-19  # charge of the ion or it can be charge of an electron if it is negative
alt = np.arange(60, 1000, 5)  # the altitude range to be calculated in km
#alt=np.linspace(60, 1000, num=471)
# date to calculate conductivity in the form of "datetime(YYYY,MM,DD,HH,mm)"
dn = datetime(2001, 1, 2, 10, 0)
lon = 37.36  # longitude in degrees (here for Bahir Dar)
lat = 11.6  # latitude in degrees (here for Bahir Dar)
note = open('conductivity' + '.txt', 'w')
note.write('Altitude(km) sigma_p sigma_h sigma_0 kappa_i kappa_e\n')
for j in range(len(alt)):
    pt = Point(dn, lat, lon, alt[j])
    # two versions of IRI are included in the pyglow module, version=2016 and version=2012
    pt.run_iri(version=2016)
    # two versions of igrf are included in the pyglow module, version=11 and version=12
    pt.run_igrf(version=12)
    pt.run_msis(version=2000)  # runs the MSIS-00 model
    AR = pt.nn['AR']
    H = pt.nn['H']
    HE = pt.nn['HE']
    N = pt.nn['N']
    N2 = pt.nn['N2']
    O = pt.nn['O']
    O2 = pt.nn['O2']
    # sum of all the nutral density particles
    density_sum = (AR+H+HE+N+N2+O+O2)*1e6
    n_n = density_sum
    total_mass = pt.rho*1e3/density_sum  # rho is g/cm^3 so 1e3 factor here
    # multiplying by Avogadro's number 6.0221415e23 to get A in atomic mass unit (amu)
    A = total_mass*6.0221415e26
    Te = pt.Te
    ne = pt.ne*1e6
    n = ne
    # Te=electron temperature, ne=electron density (m^-3) and B=total geomagnetic field (Tesla)
    B = pt.B
    omega_e = q*B/Me
    omega_i = q*B/Mi
    # nu_in=(4.34e-16*N2+4.28e-16*O2+2.44e-16*O)*1e6
    # colliion coefficient for ion-neutral collision
    nu_in = 2.6e-15*(n_n+n)*A**(-1./2)
    # colliion coefficient for electron-neutral collision
    nu_en = 5.4e-16*n_n*np.sqrt(Te)
    # if you want add electron ion collision (see kelly book) n is changed back to cm^-3 unit
    n_m3 = n*1e-6
    # colliion coefficient for electron-ion collision
    nu_ei = (34+(4.18*np.log(Te**3./n_m3)))*n_m3*Te**(-3./2)
    nu_e = nu_en  # + nu_ei # colliion coefficient for total electron collision
    kappa_i = q*B/(Mi*nu_in)
    kappa_e = -q*B/(Me*nu_e)
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
data = np.loadtxt('conductivity.txt', skiprows=1)
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
