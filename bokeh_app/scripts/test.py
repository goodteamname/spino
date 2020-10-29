# Set up data
import pandas as pd
import matplotlib.pyplot as plt
ts = pd.read_csv("./data/test_timeseries_copy.csv", skiprows=1, delimiter=",", names=['time', 'y1', 'y2', 'y3'])
ind = 'y1'
new_ts = ts[['time', ind]]
print(new_ts.head())
