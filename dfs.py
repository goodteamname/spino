import numpy as np
import pandas as pd


def dfs(time_series):
    # DFS   Discrete Fourier series
    #   DFS(time_series) computes the Discrete Fourier series of an input
    #   time-series time_series.
    # time_series must be a vector with a length N that
    #   is greater than 1 and odd in number.  F=DFS(time_series) returns a
    #   structure F as follows:
    #     F.alpha0 = mean of the time-series
    #     F.alpha  = coefficients of cosine terms for k=1:(N-1)/2
    #     F.beta   = coefficients of the sine terms for k=1:(N-1)/2
    #     F.power  = normalised power-spectrum of the time-series

    # Check length of time-series.  Must be odd and longer than 1
    N = len(time_series)
    print(N)
    if N % 2 == 0:
        print('even')
        time_series = time_series[0:-1]
        N -= 1
    elif N == 1:
        print("length must be greater than 1")

    # Ensure that time_series is a column vector
    if len(time_series.shape) != 1:
        print('needs to be 1D')

    # Create index of time-series entries
    j = np.arange(0, N)

    # Calculate the coefficients at each frequenctime_series
    G = np.zeros((int((N-1)/2), 2))
    # 2 = sin, cos
    # N = number of timesteps (5)
    # k_max = int(N-1)/2 = maximum harmonic number
    alpha0 = np.mean(time_series)
    for k in range(1, 1+int((N-1)/2)):
        C = np.cos(2*np.pi*j*k/N)
        S = np.sin(2*np.pi*j*k/N)
        Z = np.vstack((C, S))
        # print time_series
        G[k-1, :] = (2./N) * np.matmul(Z, time_series - alpha0)
    # Assemble structure containing results
    alpha = G[:, 0]
    beta = G[:, 1]
    power = 0.5 * (alpha.T**2 + beta.T**2)/np.var(time_series, ddof=1)
    d = {'alpha': alpha, 'beta': beta, 'power': power}
    table = pd.DataFrame(d)
    return table

test = np.loadtxt('data/test_timeseries.csv', delimiter=',', dtype=float)
test_data = test[:,1]

dataframe = pd.read_csv('data/test_timeseries.csv')
print(dataframe)
data = dataframe.values.tolist()
data = np.array(data)
test_data = data[:,-1]
table = dfs(test_data)

""" print(alpha)
print(beta)
print(power)

def fourier_approx(alpha, beta, data):
    N = len(data)
    k = np.arange(1,len(alpha)+1)
    alpha0 = np.mean(data)
    y = np.zeros(N)
    for j in range(N):
        y[j] = alpha0 + np.sum(alpha*np.cos(2.*np.pi*k/N * j) + beta*np.sin(2.*np.pi*k/N * j))
    return y

import matplotlib.pyplot as plt

plt.plot(test_data)
plt.plot(fourier_approx(alpha,beta,test_data))
plt.show()
 """