import pandas as pd
ts = pd.read_csv("/Users/ollietooth/Desktop/Core Training/Software Engineering/spino/bokeh_app/data/test_timeseries_copy.csv", skiprows=1, delimiter=",", names=['time', 'y1', 'y2', 'y3'])

print(ts.head())
