# Simulation of the CHAPMAN PROFILE
# which can be formulated as
##### q(z)=qmo*exp(-z+1)*exp(-(sec(x)*exp(-z))#####
# z is the reduced height
# x is the solar zentih angle measured from the zenith
# c is the ratio b/n q(z) and qmo where
# q(z) is the production rate
# qmo is the maximum production rate for an overhead sun
# copyright @Fasil Tesema
# Bahrdar university, Department of Physics, WaGRL member
import numpy as np
import matplotlib.pyplot as plt
z = np.arange(-3, 6, 0.1)
x = np.arange(0, (9/18)*np.pi, (1/18)*np.pi)  # degree range from 0 to 80
c = np.zeros((len(x), len(z)))
for i in range(len(x)):
    for j in range(len(z)):
        c[i, j] = np.exp(-z[j]+1)*np.exp(-(1/np.cos(x[i])*np.exp(-z[j])))
for i in range(len(x)):
    plt.plot(c[i, :], z, label=str(int(np.rad2deg(x[i]).round()))+r'$^{o}$')
    plt.legend(frameon=False)
plt.grid()
plt.xlim([0, 1])
plt.ylim([-2, 6])
plt.xlabel(r'$q/q_{mo}$', fontsize=14)
plt.ylabel('reduced height z', fontsize=14)
plt.savefig('chapman_profile.png', dpi=800)
plt.show()
