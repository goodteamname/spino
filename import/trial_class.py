# Example ts class for imported time series data.
import pandas as pd

# Importing test_timeseries.csv.
example_df = pd.read_csv('./data/test_timeseries.csv', delimiter=',')


# Simple class for timeseries, ts.
class ts:

    # ts object stores the pandas dataframe, df.
    def __init__(self, df):
        self.df = df


example_ts = ts(example_df)

# To access pandas dataframe.
print(example_ts.df)
