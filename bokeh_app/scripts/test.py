# Set up data
import pandas as pd
import matplotlib.pyplot as plt
ts = pd.read_csv("spino/bokeh_app/data/test_timeseries.csv", skiprows=1, delimiter=",", names=['time', 'y1', 'y2', 'y3'])

rolling_mean = ts.rolling(window=30).mean()
print(rolling_mean.head())
plt.plot(rolling_mean)
plt.show()
