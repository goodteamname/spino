# Pandas for data management
import pandas as pd

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# Each tab is drawn by one script
<<<<<<< HEAD
from scripts.timeseries_copy import timeseries_tab
from scripts.spectral import spectral_tab
=======
from scripts.timeseries import timeseries_tab
from scripts.correlation import correlations_tab
# from scripts.histogram import histogram_tab
>>>>>>> main

# Read data into dataframes
# Import data.
ts = pd.read_csv("./bokeh_app/data/test_timeseries_copy.csv", skiprows=1,
                 delimiter=",", names=['time', 'y1', 'y2', 'y3'])
hist_ts = pd.read_csv("./bokeh_app/data/test_timeseries_copy.csv",
                      skiprows=1, delimiter=",",
                      names=['time', 'y1', 'y2', 'y3'])
hist_ts.set_index('time', inplace=True, drop=True)

# Create each of the tabs
<<<<<<< HEAD
tab1 = timeseries_tab(ts)
tab4 = spectral_tab(ts)

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab4])
=======
tab1 = timeseries_tab(ts, hist_ts)
tab3 = correlations_tab(ts)

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab3])
>>>>>>> main

# Put the tabs in the current document for display
curdoc().add_root(tabs)
