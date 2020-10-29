import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ts = pd.read_csv(
    "bokeh_app/data/test_timeseries.csv",
    skiprows=1,
    delimiter=",",
    names=['time', 'y1', 'y2', 'y3']
)

ts = ts.truncate(after=999)  # cannot handle NaN in remove_trend


def remove_trend(ts, N):
    """Remove a best fitting polynomial of degree N from time series data.

    Uses numpy methods polyfit to find the coefficients of a degree N
    polynomial of best fit (least squares resiuduals) and polyeval to
    construct the polynomial over the duration of the time series.

    :param df: Time series data as a pandas dataframe.
    :param N: Degree of polynomial trend to remove.
    :return detrended: df.y with the best fitting polynomial subtracted off.
    :return fit: Array of values of the best fitting polynomial at each time.
    """
    headers = ['time']
    data = [ts.time]
    for col in np.delete(ts.columns.values, 0):
        fit = np.polyval(np.polyfit(ts.time, ts[col], deg=N), ts.time)
        detrended = ts[col]-fit
        headers.append('detrended_' + col)
        headers.append('fit_' + col)
        data.append(pd.Series(detrended))
        data.append(pd.Series(fit))
    ts_detrended = pd.concat(data, axis=1, keys=headers)
    return ts_detrended


ts_detrended = remove_trend(ts, 1)
plt.figure()
plt.plot(ts.time, ts.y2, label='data2')
plt.plot(ts_detrended.time, ts_detrended.detrended_y2, label='detrended2')
plt.plot(ts_detrended.time, ts_detrended.fit_y2, label='fit2')
plt.legend()
plt.show()


# Remove seasonality of a set period
def remove_seasonality(ts, T):
    """Remove periodic repetition of period T from time series data.

    Uses differencing methods to compare equivalent points in different periods
    e.g. signal = data_[i] - data_[i-T]
    This reduces duration of time series by T.

    :param df: Time series data as a pandas DataFrame.
    :param T: Period of seasonality to be removed.
    :return diff_df: DataFrame with axes "time" and "y", corresponding
        to new time array and deseasonalised time series respectively.
    """

    T_ind = np.argmin(abs(ts.time-T))  # Find index in time array closest to T
    forward = ts.truncate(before=T_ind)
    backward = ts.truncate(after=ts.shape[0]-1-T_ind)
    forward = forward.reset_index(drop=True)
    backward = backward.reset_index(drop=True)
    ts_diff = forward-backward
    times = ts['time'][T_ind:].reset_index(drop=True)
    ts_diff['time'] = times
    return ts_diff


ts_diff = remove_seasonality(ts, 2*np.pi)
plt.figure()
plt.plot(ts.time, ts.y2, label='data2')
plt.plot(ts_diff.time, ts_diff.y2, label='de seasoned2')
plt.legend()
plt.show()


def rolling_std(ts, window):
    ts_std = ts.rolling(window).var()
    ts_std = np.sqrt(ts_std)
    ts_std["time"] = ts["time"]
    return ts_std


def rolling_mean(ts, window):
    ts_mean = ts.rolling(window).mean()
    ts_mean["time"] = ts["time"]
    return ts_mean


ts_mean = rolling_mean(ts, 20)
plt.figure()
plt.plot(ts.time, ts.y1, label='data1')
plt.plot(ts.time, ts.y2, label='data2')
plt.plot(ts.time, ts.y3, label='data3')
plt.plot(ts_mean.time, ts_mean.y1, label='rolling mean 1')
plt.plot(ts_mean.time, ts_mean.y2, label='rolling mean 2')
plt.plot(ts_mean.time, ts_mean.y3, label='rolling mean 3')
plt.legend()
plt.show()

ts_std = rolling_std(ts, 20)
plt.figure()
plt.plot(ts.time, ts.y2, label='data2')
plt.plot(ts_std.time, ts_std.y2, label='rolling std 2')
plt.legend()
plt.show()


def auto_corr(data, max_lag):
    auto_corrs = []
    lags = range(max_lag)
    for lag in lags:
        auto_corrs.append(pd.Series(data).autocorr(lag))
    headers = ['lags', 'auto_corrs']
    array = [pd.Series(lags), pd.Series(auto_corrs)]
    return pd.concat(array, axis=1, keys=headers)


auto = auto_corr(ts.y1, 600)
plt.figure()
plt.plot(auto.lags, auto.auto_corrs, label='autocorrelation')
plt.legend()
plt.show()


def corr(data1, data2, max_lag):
    corrs = []
    lags = range(max_lag)
    for lag in lags:
        corr = data1.corr(pd.Series(data2).shift(periods=lag))
        corrs.append(corr)
    headers = ['lags', 'corrs']
    array = [pd.Series(lags), pd.Series(corrs)]
    return pd.concat(array, axis=1, keys=headers)


correlations = corr(ts.y1, ts.y3, 600)
plt.figure()
plt.plot(correlations.lags, correlations.corrs, label='correlation')
plt.legend()
plt.show()
