# Import packages.
from .functions.timeseries_stats import rolling_mean, rolling_std
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Tabs, CheckboxButtonGroup, RadioButtonGroup, TableColumn, DataTable, Select, TextInput)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

ts_colors = Category20_16


# Timeseries Tab.
def timeseries_tab(ts):
    # Set up plot
    def make_lineplot(source):
        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('time')

        ttp = [("Time", "$x"), ("Value", "$y")]

        plot = figure(plot_height=400, plot_width=600, tooltips=ttp, title="Plot Name",
                    tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot.legend.location = "top_left"
        plot.legend.click_policy="hide"

        return plot

    # Set up callbacks
    def update_title(attrname, old, new):
        plot.title.text = text.value


    def update_window(attrname, old, new):
        if window_select.value == 0:

            raw_source = ColumnDataSource(data=ts)
            source.data.update(raw_source.data)
        else:
            if rolling_method.value == "Mean":
                # Apply moving average to pandas dataframe and export to CDS type.
                ts_rmean = rolling_mean(ts, window=window_select.value)
                new_source = ColumnDataSource(data=ts_rmean)
            else:
                # Apply moving std to pandas dataframe and export to CDS type.
                ts_rstd = rolling_std(ts, window=window_select.value)
                new_source = ColumnDataSource(data=ts_rstd)

            source.data.update(new_source.data)

    # Set up widgets
    text = TextInput(title="Title", value='Plot Name')
    text.on_change('value', update_title)

    rolling_method = Select(value='Mean', title='Statistic', options=['Mean', 'Std. Dev.'])
    rolling_method.on_change('value', update_window)

    window_select = Slider(start=0, end=50, step=1, value=0, title='Window Size')
    window_select.on_change('value', update_window)

    source = ColumnDataSource(data=ts)
    plot = make_lineplot(source)


    # Set up layouts and add to document
    # Put controls in a single element.
    controls = WidgetBox(text, rolling_method, window_select)

    # Create a row layout
    layout = row(controls, plot)

    # Make a tab with the layout 
    tab = Panel(child=layout, title='Time Series Plots')
    return tab
