import numpy as np
import pandas as pd


def dft(time_series):  # don't call this
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
        # print('even')
        time_series = time_series[0:-1]
        N -= 1
    elif N <= 1:
        raise ValueError("ValueError: length must be greater than 1")
    # print(time_series)
    # Ensure that time_series is a column vector
    if len(np.array(time_series).shape) != 1:
        raise ValueError("ValueError: needs to be 1D")

    G = np.fft.fft(time_series)

    return G


def dfs(time_series):  # yes
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
    # print(N)
    if N % 2 == 0:
        # print('even')
        time_series = time_series[0:-1]
        N -= 1
    elif N <= 1:
        raise ValueError("ValueError: length must be greater than 1")

    # Ensure that time_series is a column vector
    if len(np.array(time_series).shape) != 1:
        raise ValueError("ValueError: needs to be 1D")

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


def fourier_to_freq_spectrum(time_series, test_time):  # yes
    '''fourier_to_freq_spectrum
    :param time_series: time-series data.
        must be a vector with a length N that is >1 and odd.
    :param test_time: times corresponding to time-series data
    :returns alpha0: mean of the time-series
    '''
    sampling_rate = test_time[1]-test_time[0]
    fourier_transform = dft(time_series)
    abs_fourier_transform = np.abs(fourier_transform)
    power_spectrum = np.square(abs_fourier_transform)
    frequency = np.linspace(0, sampling_rate/2, len(power_spectrum))
    # pd dataframe columns freq, power
    d = {'frequency': frequency, 'power': power_spectrum}
    df = pd.DataFrame(d)
    return df


def fourier_to_coefficients(time_series):  # yes
    '''
    :param time_series:  must be a vector with a length N that is >1 and odd.
    :returns alpha0: mean of the time-series
    :returns table: a pandas dataframe containging alpha, beta, power
        table.alpha  = coefficients of cosine terms for k=1:Nyquist
        table.beta   = coefficients of sine terms for k=1:Nyquist
        table.power  = normalised power-spectrum of the time-series
    '''
    N = len(time_series)
    if N % 2 == 0:
        # print('even')
        time_series = time_series[0:-1]
        N -= 1
    elif N <= 1:
        raise ValueError("ValueError: length must be greater than 1")
    G = dft(time_series)

    # freq = np.fft.fftfreq(len(y), t[1] - t[0])
    N = len(time_series)
    Nu = int(np.ceil((N+1)/2))
    G = G[0:Nu]

    alpha0 = np.real(G[0])/N
    alpha = 2*np.real(G[1:])/N
    beta = -2*np.imag(G[1:])/N
    power = 0.5*(alpha**2 + beta**2)/np.var(time_series, ddof=1)

    d = {'alpha': alpha, 'beta': beta, 'power': power}
    table = pd.DataFrame(d)
    return alpha0, table


def fourier_approx(alpha0, table, data, k=[]):  # yes, total approx
    ''' fourier_approx
    calculates approximated data values

    :param alpha0: mean of time series
    :param alpha: coefficients of cosine terms for k=1:(N-1)/2
    :param beta: coefficients of the sine terms for k=1:(N-1)/2
    :param data: 1 time-series of data
    :param k: harmonic numbers associated with alpha and beta
    :return approximation: approximated time series
    '''
    alpha = table.alpha
    beta = table.beta
    N = len(data)
    if len(k) == 0:
        k = np.arange(1, len(alpha)+1)
    approximation = np.zeros(N)
    for j in range(N):
        approximation[j] = alpha0 + np.sum(
            alpha*np.cos(2.*np.pi*k/N * j)
            + beta*np.sin(2.*np.pi*k/N * j))
    # print(approximation)
    # print(approximation.size)
    return approximation


def calc_residuals(alpha0, table, data, data_times, components=0):
    '''calc_residuals
    plots the top contributing components to the approximation
    :param alpha0: mean of time series
    :param table: a pandas dataframe containging alpha, beta, power
    :param data: time-series data
    :param data_times: times corresponding to the time-series data
    :param components: number of components to include in approximation.
        If not entered then uses optimise_residuals to find best value to use.
    '''
    # time series
    # print(table)
    # print(type(table))
    if components == 0:
        components = optimise_residuals(alpha0, table, data)
    # print("number of components being used: " + str(components))
    top_indices = np.flip(np.argsort(np.array(table.power))[-components:])
    top_alpha = [table.alpha[i] for i in top_indices]
    top_beta = [table.beta[i] for i in top_indices]
    top_power = [table.power[i] for i in top_indices]
    top_table = pd.DataFrame(
        {'alpha': top_alpha, 'beta': top_beta, 'power': top_power}
        )
    approximation = fourier_approx(
        alpha0, top_table, data, k=top_indices+1
        )
    # difference
    residual = data-approximation
    residual_df = pd.DataFrame(
        {'time': data_times, 'raw_data': data, 'approx': approximation, 'residuals': residual}
        )
    # time, data, residual column
    # plt.plot(residual)
    # plt.plot(data)
    # plt.show()
    # plot residual against components
    N = len(data)
    top_components_for_approx_dict = {'times': data_times}
    freq = {}
    amplitude = {}
    power = {}
    for i in range(0, components):
        y = (
            alpha0
            + top_alpha[i]*np.cos(2.*np.pi*top_indices[i]/N * np.arange(0, N))
            + top_beta[i]*np.sin(2.*np.pi*top_indices[i]/N * np.arange(0, N))
        )
        # print('y', y)
        freq['Comp. '+str(i+1)] = round(2.*np.pi*top_indices[i]/N, 2)
        amplitude['Comp. '+str(i+1)] = round(max(y)-np.mean(y), 2)
        power['Comp. '+str(i+1)] = round(top_power[i], 2)
        top_components_for_approx_dict['comp.'+str(i+1)] = y
        # plt.plot(y)
    # plt.show()
    top_components_for_approx = pd.DataFrame(
        top_components_for_approx_dict
        )  # one column for time, then a column for each component
    summary_table = pd.DataFrame(
        {'frequency': freq, 'amplitude': amplitude, 'power': power}
        )
    return top_components_for_approx, summary_table, residual_df
    # THINGS YOU COULD RETURN
    # top_components_for_approx -
    #   pd.df with one column for time, then a column for each key component
    # summary_table -
    #   pd.df indexed by component, columns for frequency, amplitude, power
    # residual_df -
    #   pd.df with columns for time, data, residual


def optimise_residuals(alpha0, table, data):  # no
    '''optimise_residuals
    find the minimum number of components to use
        to suitably approximate the data
    :param alpha0: mean of time series
    :param table: a pandas dataframe containging alpha, beta, power
    :param data: time-series data
    :returns best_index: number of components to include in approximation.
    '''
    # print('optimising residuals')
    mean_residual = []
    x = np.arange(1, len(table.power), 1)
    for components in x:
        top_indices = np.argsort(np.array(table.power))[-components:]
        top_alpha = [table.alpha[i] for i in top_indices]
        top_beta = [table.beta[i] for i in top_indices]
        top_power = [table.power[i] for i in top_indices]
        top_table = pd.DataFrame(
            {'alpha': top_alpha, 'beta': top_beta, 'power': top_power}
            )
        approximation = fourier_approx(
            alpha0, top_table, data, top_indices+1
            )
        residual = data - approximation
        mean_residual.append(np.mean(abs(residual)))
    diff = np.gradient(np.gradient(mean_residual))
    sorted_indices = np.argsort(diff)
    if abs(max(mean_residual, key=abs)) > 1:
        best_index = len(sorted_indices)-1
    else:
        for i in sorted_indices:
            if abs(mean_residual[i]) < 1:
                best_index = i
                break
    return best_index


# example usage without Bokeh
# dataframe = pd.read_csv('bokeh_app/data/test_timeseries_noisy.csv')

# selected_column = 'y'

# time = dataframe['time'].values.tolist()
# data = dataframe[selected_column].values.tolist()

# This is where you pass it the appropriate data

# given name of header of pd

# alpha0, table = dfs(data)
# frequency, power_spectrum = fourier_to_freq_spectrum(data, time)
# print(len(frequency), len(power_spectrum))

# calc_residuals(alpha0, table, data, time, components = 0)

# plt.plot(data)
# plt.plot(fourier_approx(alpha0, table, data))
# plt.show()

# print(fourier_to_coefficients([1,2,3,4,5,6]))
