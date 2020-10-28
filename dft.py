import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def dft(time_series):
    N = len(time_series)
    if N % 2 == 0:
        print('even')
        time_series = time_series[0:-1]
        N -= 1
    elif N <= 1:
        raise ValueError("ValueError: length must be greater than 1")

    # Ensure that time_series is a column vector
    if len(np.array(time_series).shape) != 1:
        print('needs to be 1D')
    
    G = np.fft.fft(time_series)
    #freq = np.fft.fftfreq(len(y), t[1] - t[0])
    Nu = int(np.ceil((N+1)/2))
    G = G[0:Nu]
    
    alpha0 = np.real(G[0])/N
    alpha = 2*np.real(G[1:])/N
    beta = -2*np.imag(G[1:])/N
    power = 0.5*(alpha**2 + beta**2)/np.var(time_series, ddof=1)

    d = {'alpha': alpha, 'beta': beta, 'power': power}
    table = pd.DataFrame(d)
    return table    

def fourier_approx(alpha, beta, data):
    N = len(data)
    k = np.arange(1, len(alpha)+1)
    alpha0 = np.mean(data)
    y = np.zeros(N)
    for j in range(N):
        y[j] = alpha0 + np.sum(alpha*np.cos(2.*np.pi*k/N * j) + beta*np.sin(2.*np.pi*k/N * j))
    return y

dataframe = pd.read_csv('data/test_timeseries_noisy.csv')
data = dataframe.values.tolist()
data = np.array(data)
test_time = data[:, -2]
test_data = data[:, -1]
table = dft(test_data)

