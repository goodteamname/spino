# Very rough first attempt at detrending, deseasonalising data

# Expect input as a pandas df
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Import temporary test data as pandas df
df = pd.read_csv(os.getcwd() + '/spino/data/linear_trend_test_timeseries.csv')


def remove_trend(df, N):
    """Remove a best fitting polynomial of degree N from time series data.

    Uses numpy methods polyfit to find the coefficients of a degree N
    polynomial of best fit (least squares resiuduals) and polyeval to
    construct the polynomial over the duration of the time series.

    :param df: Time series data as a pandas dataframe.
    :param N: Degree of polynomial trend to remove.
    :return detrended: df.y with the best fitting polynomial subtracted off.
    :return fit: Array of values of the best fitting polynomial at each time.
    """
    trend_coeffs = np.polyfit(df.time, df.y, deg=N)
    fit = np.polyval(trend_coeffs, df.time)
    detrended = df.y - fit
    return detrended, fit


detrended, fit = remove_trend(df, 1)

plt.figure()
plt.plot(df.time, df.y, label='data')
plt.plot(df.time, fit, label='fit')
plt.plot(df.time, detrended, label='detrended')
plt.legend()
plt.show()

# Remove seasonality of a set period
