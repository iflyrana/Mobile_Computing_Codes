import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

N=10**6
ip = np.random.randint(0,1)
s = 2*ip-1

n = np.sqrt(1/2)*(np.random.randn(N)+1j*np.random.randn(N))

EbNodB = np.arange(0, 61)

EbNo = 10**(EbNodB / 10)

nErrAwgn = np.zeros(len(EbNodB))
nErrRayleigh = np.zeros(len(EbNodB))

for i in range(len(EbNodB)):
    y_awgn = s + 10**(-EbNodB[i]/20)*n
    ipHatawgn = np.real(y_awgn) > 0
    nErrAwgn[i] = np.sum(ip!=ipHatawgn)

    h = np.sqrt(1/2)*(np.random.randn(N) + 1j*np.random.randn(N))
    y_Rayleigh = h*s + 10**(-EbNodB[i]/20)*n
    ipHatRayleigh = np.real(y_Rayleigh/h) > 0
    nErrRayleigh[i] = np.sum(ip!=ipHatRayleigh)

simBERawgn = nErrAwgn/N
simBERRayleigh = nErrRayleigh/N

theoryBERawgn = 0.5* erfc(np.sqrt(EbNo))
theoryBErayleigh = 0.5 * (1-np.sqrt((EbNo)/(1+EbNo)))

plt.figure()
plt.semilogy(EbNodB, theoryBERawgn, 'b.-', label='AWGN Theory')
plt.semilogy(EbNodB, simBERawgn, 'mx-', label='AWGN Sim')
plt.semilogy(EbNodB, theoryBErayleigh, 'r.-', label='Rayleigh Theory')
plt.semilogy(EbNodB, simBERRayleigh, 'go-', label='Rayleigh Sim')

plt.axis([0, 60, 10**-6, 0.5])
plt.grid(True)
plt.xlabel("EbNodB")
plt.ylabel("BER")
plt.legend()
plt.show()

