
import pandas as pd

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Tabs, CheckboxButtonGroup, TableColumn, DataTable, Select, TextInput)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

ts_colors = Category20_16
initial_ts_list = ['y1', 'y2', 'y3']

# Set up data
ts = pd.read_csv("data/test_timeseries.csv", skiprows=1, delimiter=",", names=['time', 'y1', 'y2', 'y3'])


# Set up plot
def make_lineplot(source):
    ts_list = source.column_names
    ts_list.remove('index')
    ts_list.remove('time')

    ttp = [("Time" , "$x"), ("Value", "$y")]

    plot = figure(plot_height=400, plot_width=400, tooltips=ttp, title="Plot Name",
                tools="hover, crosshair, zoom_in, zoom_out, reset, save")
    for i, name in enumerate(ts_list):
        plot.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

    plot.legend.location = "top_left"
    plot.legend.click_policy="hide"

    return plot


# Set up widgets
text = TextInput(title="title", value='Plot Name')

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_window(attrname, old, new):
    if window_select.value == 0:
        pass
    else:
        # Function to apply moving average to pandas dataframe and export to CDS type.
        ts_rmean = ts.rolling(window=window_select.value).mean()
        new_source = ColumnDataSource(data=ts_rmean)

        source.data.update(new_source.data)


window_select = Slider(start=0, end=20, step=1, value=10, title='Window Size')
window_select.on_change('value', update_window)

source = ColumnDataSource(data=ts)
plot = make_lineplot(source)


# Set up layouts and add to document
# Put controls in a single element.
controls = WidgetBox(text, window_select)

curdoc().add_root(row(controls, plot, width=800))
curdoc().title = "Plotting"
