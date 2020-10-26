import pandas as pd
import matplotlib.pyplot as plt

#importing the dataset
data = pd.read_csv('test_timeseries.csv', header=None)

histogram(data, 10)

