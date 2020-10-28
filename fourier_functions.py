import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate


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

    return G

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
    
def fourier_to_freq_spectrum(time_series, test_time):
    '''
    :param time_series:  must be a vector with a length N that is >1 and odd.
    :returns alpha0: mean of the time-series
    '''
    sampling_rate = test_time[1]-test_time[0]
    fourier_transform = dft(time_series)
    abs_fourier_transform = np.abs(fourier_transform)
    power_spectrum = np.square(abs_fourier_transform)
    frequency = np.linspace(0, sampling_rate/2, len(power_spectrum))
    return frequency, power_spectrum

def fourier_to_coefficients(time_series):
    '''
    :param time_series:  must be a vector with a length N that is >1 and odd.
    :returns alpha0: mean of the time-series
    :returns table: a pandas dataframe containging alpha, beta, power
        table.alpha  = coefficients of cosine terms for k=1:Nyquist
        table.beta   = coefficients of sine terms for k=1:Nyquist
        table.power  = normalised power-spectrum of the time-series
    '''
    fourier_transform = dft(time_series)
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


def fourier_approx(alpha0, alpha, beta, data, k = 0):
    ''' fourier_approx
    calculates approximated data values 

    :param alpha0: mean of time series
    :param alpha: coefficients of cosine terms for k=1:(N-1)/2
    :param beta: coefficients of the sine terms for k=1:(N-1)/2
    :param data: 1 time-series of data 
    :return y: approximated time series
    '''
    N = len(data)
    #if k == 0:
    #    k = np.arange(1, len(alpha)+1)
    y = np.zeros(N)
    for j in range(N):
        y[j] = alpha0 + np.sum(
            alpha*np.cos(2.*np.pi*k/N * j)
            + beta*np.sin(2.*np.pi*k/N * j))
    return y

def calc_residuals(alpha0, table, data, data_times, components=0):
    # time series
    # top 5 components
    if components == 0:
        components = optimise_residuals(alpha0, table, data)
    print('back to calc residuals')
    top_indices = np.argsort(np.array(table.power))[-components:]
    top_alpha = [table.alpha[i] for i in top_indices]
    top_beta = [table.beta[i] for i in top_indices]
    true_approx= fourier_approx(alpha0, table.alpha, table.beta, data, np.arange(1, len(table.alpha)+1))
    approximation = fourier_approx(alpha0, top_alpha, top_beta, data, top_indices+1)
    # difference
    residual = data-approximation
    # plot residual against components
    print(np.argsort(np.array(table.power)))
    print(top_alpha, top_beta, top_indices)
    N = len(data)
    plt.plot(approximation)
    #plt.plot(true_approx)
    plt.plot(data)
    for i in range(0, components):
        y = alpha0 + top_alpha[i]*np.cos(2.*np.pi*top_indices[i]/N * np.arange(0, N)) + top_beta[i]*np.sin(2.*np.pi*top_indices[i]/N * np.arange(0, N))
        plt.plot(y)
    plt.show()

def optimise_residuals(alpha0, table, data):
    print('optimising residuals')
    mean_residual = []
    x = np.arange(1, 30)#np.arange(1, len(table.power), 1)
    for components in x:
        print(components)
        top_indices = np.argsort(np.array(table.power))[-components:]
        top_alpha = [table.alpha[i] for i in top_indices]
        top_beta = [table.beta[i] for i in top_indices]
        approximation = fourier_approx(alpha0, top_alpha, top_beta, data, top_indices+1)
        residual = data - approximation
        mean_residual.append(np.mean(abs(residual)))
    diff = np.gradient(np.gradient(mean_residual))
    sorted_indices = np.argsort(diff)
    for i in sorted_indices:
        if mean_residual[i]<1:
            best_index = i
            break
    return best_index


dataframe = pd.read_csv('data/test_timeseries_noisy.csv')
data = dataframe.values.tolist()
data = np.array(data)
# This is where you pass it the appropriate data - currently only works on 2 column data
test_time = data[:, -2]
test_data = data[:, -1]
alpha0, table = dfs(test_data)
calc_residuals(alpha0, table, test_data, test_time, 0)
'''plt.plot(test_data)
plt.plot(fourier_approx(alpha0, table.alpha, table.beta, test_data))
plt.show()'''
