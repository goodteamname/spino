import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def dft(time_series):
    '''DFT   Discrete Fourier transform
    DFS(time_series) computes the Discrete Fourier transform of an input
    time-series -- time_series.
    Uses numpy.fft method

    :param time_series:  must be a vector with a length N that is >1 and odd.
    :returns alpha0: mean of the time-series
    :returns table: a pandas dataframe containging alpha, beta, power
        table.alpha  = coefficients of cosine terms for k=1:Nyquist
        table.beta   = coefficients of sine terms for k=1:Nyquist
        table.power  = normalised power-spectrum of the time-series
    '''
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
    # freq = np.fft.fftfreq(len(y), t[1] - t[0])
    Nu = int(np.ceil((N+1)/2))
    G = G[0:Nu]

    alpha0 = np.real(G[0])/N
    alpha = 2*np.real(G[1:])/N
    beta = -2*np.imag(G[1:])/N
    power = 0.5*(alpha**2 + beta**2)/np.var(time_series, ddof=1)

    d = {'alpha': alpha, 'beta': beta, 'power': power}
    table = pd.DataFrame(d)
    return alpha0, table


def fourier_approx(alpha0, alpha, beta, data):
    N = len(data)
    k = np.arange(1, len(alpha)+1)
    y = np.zeros(N)
    for j in range(N):
        y[j] = alpha0 + np.sum(
            alpha*np.cos(2.*np.pi*k/N * j)
            + beta*np.sin(2.*np.pi*k/N * j))
    return y


dataframe = pd.read_csv('data/test_timeseries_noisy.csv')
data = dataframe.values.tolist()
data = np.array(data)
# This is where you pass it the appropriate data - currently only works on 2 column data
test_time = data[:, -2]
test_data = data[:, -1]
alpha0, table = dft(test_data)

plt.plot(test_data)
plt.plot(fourier_approx(alpha0, table.alpha, table.beta, test_data))
plt.show()
