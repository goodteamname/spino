# Very rough first attempt at detrending, deseasonalising data

# Expect input as a pandas df
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Import temporary test data as pandas df
df = pd.read_csv(os.getcwd() + '/data/linear_trend_test_timeseries_noisy.csv')

ts = pd.read_csv("bokeh_app/data/test_timeseries.csv", skiprows=1, delimiter=",", names=['time', 'y1', 'y2', 'y3'])
ts=ts.truncate(after=999) # cannot handle NaN in imported data in remove_trend
print(ts)


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
    print(type(ts.columns.values))
    print(ts.columns.values)
    print(np.delete(ts.columns.values, 0))
    for col in np.delete(ts.columns.values, 0):
        print(col)
        print(ts[col])
        fit = np.polyval(np.polyfit(ts.time, ts[col], deg=N), ts.time)
        detrended = ts[col]-fit
        headers.append('detrended_' + col)
        headers.append('fit_' + col)
        data.append(pd.Series(detrended))
        data.append(pd.Series(fit))
    ts_detrended = pd.concat(data, axis=1, keys=headers)
    return ts_detrended

ts_detrended = remove_trend(ts,1)
plt.figure()
plt.plot(ts.time, ts.y2, label='data2')
plt.plot(ts_detrended.time, ts_detrended.detrended_y2, label='detrended2')
plt.plot(ts_detrended.time, ts_detrended.fit_y2, label='fit2')
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

    T_ind = np.argmin(abs(df.time-T))  # Find index in time array closest to T

    diffs = list()
    for i in range(T_ind, len(df.y)):  # Begin differencing after 1 full period
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


def rolling_std(ts, window):
    ts_std = ts.rolling(window).var()
    ts_std=np.sqrt(ts_std)
    ts_std["time"] = ts["time"]
    return ts_std


def rolling_mean(ts, window):
    ts_mean = ts.rolling(window).mean()
    ts_mean["time"] = ts["time"]
    return ts_mean


ts_mean=rolling_mean(ts,20)
plt.figure()
plt.plot(ts.time, ts.y1, label='data1')
plt.plot(ts.time, ts.y2, label='data2')
plt.plot(ts.time, ts.y3, label='data3')
plt.plot(ts_mean.time, ts_mean.y1, label='rolling mean 1')
plt.plot(ts_mean.time, ts_mean.y2, label='rolling mean 2')
plt.plot(ts_mean.time, ts_mean.y3, label='rolling mean 3')
plt.legend()
plt.show()

ts_std=rolling_std(ts,20)
plt.figure()
plt.plot(ts.time, ts.y2, label='data2')
plt.plot(ts_std.time, ts_std.y2, label='rolling std 2')
plt.legend()
plt.show()