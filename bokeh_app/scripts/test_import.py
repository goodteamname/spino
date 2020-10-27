import pandas as pd

ts = pd.read_csv("./data/test_timeseries.csv")
# print(ts.head())
# ts.set_index('time', inplace=True, drop=True)
# print(ts.head())
print(ts)

# Find maximum range of ts.
# ts_range = ts.apply(lambda x: x.max()-x.min())
# range_max = ts_range.max()
