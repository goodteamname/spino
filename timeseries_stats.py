# Very rough first attempt at detrending, deseasonalising data

# Expect input as a panda df
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

#print(os.getcwd())
df = pd.read_csv(os.getcwd() + '/spino/data/linear_trend_test_timeseries.csv')


#print(df.head(n=5))

# Remove trend
def remove_trend(df, N):
    #df = ts.df
    trend_coeffs = np.polyfit(df.time, df.y, deg=N) # gives coefficients
    fit = np.polyval(trend_coeffs, df.time) # evaluates polynomial fit
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

