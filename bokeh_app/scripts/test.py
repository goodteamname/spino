# Set up data
import pandas as pd

ts = pd.read_csv("./data/test_timeseries_copy.csv", skiprows=1, delimiter=",", names=['time', 'y1', 'y2', 'y3'])

print(len(ts))
