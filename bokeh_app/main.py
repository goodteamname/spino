# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
from scripts.timeseries_copy import timeseries_tab
# from scripts.histogram import histogram_tab

# Read data into dataframes
# Import data.
ts = pd.read_csv("./bokeh_app/data/test_timeseries_copy.csv", skiprows=1, delimiter=",", names=['time', 'y1', 'y2', 'y3'])

# Create each of the tabs
tab1 = timeseries_tab(ts)

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
