import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def dfs(time_series):
    '''DFS   Discrete Fourier series
    DFS(time_series) computes the Discrete Fourier series of an input
    time-series -- time_series.

    :param time_series:  must be a vector with a length N that is >1 and odd.
    :returns alpha0:mean of the time-series
    :returns table: a pandas dataframe containging alpha, beta, power
        table.alpha  = coefficients of cosine terms for k=1:(N-1)/2
        table.beta   = coefficients of the sine terms for k=1:(N-1)/2
        table.power  = normalised power-spectrum of the time-series
    '''

    # Check length of time-series.  Must be odd and longer than 1

    N = len(time_series)
    print(N)
    if N % 2 == 0:
        print('even')
        time_series = time_series[0:-1]
        N -= 1
    elif N <= 1:
        raise ValueError("ValueError: length must be greater than 1")

    # Ensure that time_series is a column vector
    if len(np.array(time_series).shape) != 1:
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
    return alpha0, table


def fourier_approx(alpha0, alpha, beta, data):
    ''' fourier_approx
    calculates approximated data values 

    :param alpha0: mean of time series
    :param alpha: coefficients of cosine terms for k=1:(N-1)/2
    :param beta: coefficients of the sine terms for k=1:(N-1)/2
    :param data: 1 time-series of data 
    :return y: approximated time series
    '''
    N = len(data)
    k = np.arange(1, len(alpha)+1)
    y = np.zeros(N)
    for j in range(N):
        y[j] = alpha0 + np.sum(
                    alpha*np.cos(2.*np.pi*k/N * j)
                    + beta*np.sin(2.*np.pi*k/N * j))
    return y


dataframe = pd.read_csv('data/test_timeseries_noisy.csv')
print(dataframe)
data = dataframe.values.tolist()
data = np.array(data)
# This is where you pass it the appropriate data
# currently only works on 2 column data
test_data = data[:, -1]
alpha0, table = dfs(test_data)

plt.plot(test_data)
plt.plot(fourier_approx(alpha0, table.alpha, table.beta, test_data))
plt.show()
