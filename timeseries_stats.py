# Very rough first attempt at detrending, deseasonalising data

# Expect input as a pandas df
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Import temporary test data as pandas df
df = pd.read_csv(os.getcwd() + '/data/linear_trend_test_timeseries_noisy.csv')


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
    data = [df.time, pd.Series(detrended), pd.Series(fit)]
    headers = ["time", "y", "fit"]
    df_detrended = pd.concat(data, axis=1, keys=headers)
    return df_detrended


df_detrended = remove_trend(df, 1)

plt.figure()
plt.plot(df.time, df.y, label='data')
plt.plot(df_detrended.time, df_detrended.fit, label='fit')
plt.plot(df_detrended.time, df_detrended.y, label='detrended')
plt.legend()
plt.show()


# Remove seasonality of a set period
def remove_seasonality(df, T):
    """Remove periodic repetition of period T from time series data.

    Uses differencing methods to compare equivalent points in different periods
    e.g. signal = data_[i] - data_[i-T]
    This reduces duration of time series by T.

    :param df: Time series data as a pandas DataFrame.
    :param T: Period of seasonality to be removed.
    :return diff_df: DataFrame with axes "time" and "y", corresponding
        to new time array and deseasonalised time series respectively.
    """

    T_ind = np.argmin(abs(df.time-T)) # Find index in time array closest to T

    diffs = list()
    for i in range(T_ind, len(df.y)): # Begin differencing after 1 full period
        diff = df.y[i] - df.y[i-T_ind]
        diffs.append(diff)

    # Store time (from T_ind to end) and deseasonalised data in DataFrame
    # Note: reset indices for time to start at 0, not T_ind for
    # consistency with deseasonalised data
    data = [df["time"][T_ind:].reset_index(drop=True), pd.Series(diffs)]
    headers = ["time", "y"]
    diff_df = pd.concat(data, axis=1, keys=headers)

    return diff_df  # Length is shorter by T_ind


diffs = remove_seasonality(df, 2*np.pi)

plt.figure()
plt.plot(df.time, df.y, label='data')
plt.plot(diffs.time, diffs.y, label='detrended')
plt.legend()
plt.show()


def rolling_mean(df, window):
    """Calculate rolling mean of time series data using specified window.

    Uses pandas.rolling methods to find rolling mean
    and returns this in a DataFrame with time array.

    :param df: Time series data as a pandas DataFrame.
    :param window: Size of window to be averaged over (int).
    :return df_mean: DataFrame with axes "time" and "y", corresponding
        to time array and rolling mean respectively.
    """
    mean = df["y"].rolling(window).mean()
    # Store result in a DataFrame
    data = [df["time"], pd.Series(mean)]
    headers = ["time", "y"]
    df_mean = pd.concat(data, axis=1, keys=headers)

    return df_mean


df_mean = rolling_mean(df, 200)

plt.figure()
plt.plot(df.time, df.y, label='data')
plt.plot(df_mean.time, df_mean.y, label='rolling mean')
plt.legend()
plt.show()
