import numpy as np


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
    if N % 2 == 0 or N == 1:
        print('Input vector must have length greater than 1 and ODD.')

    # Ensure that time_series is a column vector
    if len(time_series.shape) != 1:
        print('needs to be 1D')

    # Create index of time-series entries
    j = np.arange(1, N+1)

    # Calculate the coefficients at each frequenctime_series
    G = np.zeros((N, 2,  int((N-1)/2)))
    for k in range(1, int((N-1)/2)):
        C = np.cos(2*np.pi*j*k/N)
        S = np.sin(2*np.pi*j*k/N)
        Z = np.vstack((C, S)).T
        print(Z.shape)
        a = (np.vstack((time_series, time_series)) - np.mean(time_series))
        print(a.shape)
        G[:, :, k] = (2/N) * Z * a

    # Assemble structure containing results
    alpha0 = np.mean(time_series)
    alpha = G[0, :]
    beta = G[1, :]
    power = 0.5 * (alpha**2 + beta**2)/np.var(time_series)

    return alpha, beta, power


Y = np.array([1, 2, 3, 4, 5])

alpha, beta, power = dfs(Y)

print(alpha)
print(beta)
print(power)
