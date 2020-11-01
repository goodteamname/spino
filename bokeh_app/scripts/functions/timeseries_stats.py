import pandas as pd
import numpy as np


def remove_trend(ts, N):
    """Remove a best fitting polynomial of degree N from time series data.

    Uses numpy methods polyfit to find the coefficients of a degree N
    polynomial of best fit (least squares resiuduals) and polyeval to
    construct the polynomial over the duration of the time series.
    If more than one column of data in ts, returns trend and detrended
    data for each data set.

    :param ts: Time series data as a pandas dataframe.
    :param N: Degree of polynomial trend to remove.
    :return ts_detrended: timeseries composed of time column, and two
        output result columns per input data column; fit_<data_col> is
        Array of values of the best fitting polynomial at each time;
        detrended_<data_col> is original data, with trend fit subtracted
    """
    headers = ['time']
    data = [ts.time]

    # Calculate trend for each column of data (not including time column)
    for col in np.delete(ts.columns.values, 0):
        fit = np.polyval(np.polyfit(ts.time, ts[col], deg=N), ts.time)
        detrended = ts[col]-fit
        headers.append('detrended_' + col)
        headers.append('fit_' + col)
        data.append(pd.Series(detrended))
        data.append(pd.Series(fit))

    ts_detrended = pd.concat(data, axis=1, keys=headers)  # return DataFrame
    return ts_detrended


# ts_detrended = remove_trend(ts, 1)
# plt.figure()
# plt.plot(ts.time, ts.y2, label='data2')
# plt.plot(ts_detrended.time, ts_detrended.detrended_y2, label='detrended2')
# plt.plot(ts_detrended.time, ts_detrended.fit_y2, label='fit2')
# plt.legend()
# plt.show()


def remove_seasonality(ts, T):
    """Remove periodic repetition of period T from time series data.

    Uses differencing methods to compare equivalent points in different
    periods,
    e.g. signal = data_[i] - data_[i-T]
    Note that this reduces duration of time series by T.
    If more than one column of data in ts, returns deseasonalised
    time series for each column.

    :param ts: Time series data as a pandas DataFrame.
    :param T: Period of seasonality to be removed.
    :return ts_diff: DataFrame with same columns as ts but data
        columns are now deseasonalised, and time column is correspondingly
        shorter.
    """

    T_ind = np.argmin(abs(ts.time-T))  # Find index in time array closest to T

    forward = ts.truncate(before=T_ind)  # Differencing
    backward = ts.truncate(after=ts.shape[0]-1-T_ind)

    forward = forward.reset_index(drop=True)  # So index starts at 0
    backward = backward.reset_index(drop=True)
    ts_diff = forward-backward

    # Values before first period T are lost; reset time indices to start at 0
    times = ts['time'][T_ind:].reset_index(drop=True)

    ts_diff['time_diff'] = times
    return ts_diff


# ts_diff = remove_seasonality(ts, 2*np.pi)
# plt.figure()
# plt.plot(ts.time, ts.y2, label='data2')
# plt.plot(ts_diff.time, ts_diff.y2, label='de seasoned2')
# plt.legend()
# plt.show()


def rolling_std(ts, window):
    """Calculate rolling standard deviation of time series.

    Uses pandas.DataFrame.rolling() to calculate rolling std
    dev of a given window size.
    If more than one column of data in ts, returns rolling std
    dev using given window size for each column of data.
    Returns nans for times before first window.

    :param ts: Time series data as a pandas DataFrame.
    :param window: Window size over which to calculate std dev (int).
    :return ts_std: DataFrame with same columns as ts but with rolling
        std dev in place of data column.
    """
    ts_std = ts.rolling(window).var()
    ts_std = np.sqrt(ts_std)
    ts_std["time"] = ts["time"]  # don't want std dev of time!
    return ts_std


def rolling_mean(ts, window):
    """Calculate rolling mean of time series.

    Uses pandas.DataFrame.rolling() to calculate rolling mean
    of a given window size.
    If more than one column of data in ts, returns rolling mean
    using given window size for each column of data.
    Returns nans for times before first window.

    :param ts: Time series data as a pandas DataFrame.
    :param window: Window size over which to calculate mean (int).
    :return ts_std: DataFrame with same columns as ts but with rolling
        mean in place of data column.
    """
    ts_mean = ts.rolling(window).mean()
    ts_mean["time"] = ts["time"]  # don't want mean of time!
    return ts_mean


# ts_mean = rolling_mean(ts, 20)
# plt.figure()
# plt.plot(ts.time, ts.y1, label='data1')
# plt.plot(ts.time, ts.y2, label='data2')
# plt.plot(ts.time, ts.y3, label='data3')
# plt.plot(ts_mean.time, ts_mean.y1, label='rolling mean 1')
# plt.plot(ts_mean.time, ts_mean.y2, label='rolling mean 2')
# plt.plot(ts_mean.time, ts_mean.y3, label='rolling mean 3')
# plt.legend()
# plt.show()

# ts_std = rolling_std(ts, 20)
# plt.figure()
# plt.plot(ts.time, ts.y2, label='data2')
# plt.plot(ts_std.time, ts_std.y2, label='rolling std 2')
# plt.legend()
# plt.show()


def auto_corr(data, max_lag):
    """Calculate autocorrelation of time series for range of
    lag values up to max_lag.

    Uses pandas.Series.autocorr() to calculate autocorrelation
    for a single column of data (i.e. a pandas.Series), for a
    range of values up to max_lag

    :param data: Time series data as a pandas Series.
    :param max_lag: Index of maximum time lag to calculate
        autocorrelation.
    :return: DataFrame with lags column and autocorrelation
        value at given lag.
    """
    auto_corrs = []
    lags = range(max_lag)
    for lag in lags:
        auto_corrs.append(pd.Series(data).autocorr(lag))
    headers = ['lags', 'auto_corrs']
    # Return as DataFrame:
    array = [pd.Series(lags), pd.Series(auto_corrs)]
    return pd.concat(array, axis=1, keys=headers)


# auto = auto_corr(ts.y1, 600)
# plt.figure()
# plt.plot(auto.lags, auto.auto_corrs, label='autocorrelation')
# plt.legend()
# plt.show()


def corr(data1, data2, max_lag):
    """Calculate correlation of two time series for a range
    of lags between them.

    Uses pandas.Series.corr() to calculate correlation between
    two columns of data (i.e. a pandas.Series), with data2
    shifted relative to data1 by a range of lags up to max_lag.

    :param data1: Time series data as a pandas Series.
    :param data2: Time series data as a pandas Series. This is
        the series that is shifted relative to data1.
    :param max_lag: Index of maximum time lag to calculate
        correlation.
    :return: DataFrame with lags column and correlation value
         at given lag.
    """
    corrs = []
    lags = range(max_lag)

    for lag in lags:
        corr = data1.corr(pd.Series(data2).shift(periods=lag))
        corrs.append(corr)

    headers = ['lags', 'corrs']
    array = [pd.Series(lags), pd.Series(corrs)]
    return pd.concat(array, axis=1, keys=headers)


# correlations = corr(ts.y1, ts.y3, 600)
# plt.figure()
# plt.plot(correlations.lags, correlations.corrs, label='correlation')
# plt.legend()
# plt.show()
