# Import packages.
import numpy as np
import pandas as pd
from scripts.functions.timeseries_stats import rolling_mean, remove_trend, remove_seasonality
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Tabs, CheckboxButtonGroup, RadioButtonGroup, TableColumn, DataTable, Select, TextInput)
from bokeh.layouts import row, column, WidgetBox
from bokeh.palettes import Category20_16

ts_colors = Category20_16

# decomp Tab.
def decomp_tab(ts):

    # Set up plot
    def make_decompplot(source):
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

    # Set up plot
    def make_seasonplot(source):
        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('time')
        ts_list.remove('fit_y')

        ttp = [("Time", "$x"), ("Value", "$y")]

        plot = figure(plot_height=400, plot_width=600, tooltips=ttp, title="Plot Name",
                    tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot.legend.location = "top_left"
        plot.legend.click_policy="hide"

        return plot

    #Set up callbacks
    def update_title(attrname, old, new):
        plot.title.text = text.value

    def update_title2(attrname, old, new):
        plot2.title.text = text2.value

    def update_poly(attrname, old, new):
        if poly_select.value == 0:
            pass
        else:
            # method = [rolling_method.labels[i] for i in rolling_method.active]
            # if method == "Mean"

            # Function to apply moving average to pandas dataframe and export to CDS type.
            poly_select.value = new

            detrended_data = remove_trend(ts, poly_select.value)
            combine = [ts, detrended_data]
            combined_df = pd.concat(combine)
            newsource = ColumnDataSource(data=combined_df)
            source.data.update(newsource.data)

    def update_season(attrname, old, new):
        if season_select.value == -1:
            pass
        else:
            # method = [rolling_method.labels[i] for i in rolling_method.active]
            # if method == "Mean"

            # Function to apply moving average to pandas dataframe and export to CDS type.
            season_select.value = new

            deseason_data = remove_seasonality(detrended_data, season_select.value)
            combine = [ts, deseason_data]
            combined_df = pd.concat(combine)
            newsource2 = ColumnDataSource(data=combined_df)
            source3.data.update(newsource2.data)

    # Set up widgets
    text = TextInput(title="Title of Decomposition Plot", value='Plot Name')
    text.on_change('value', update_title)

    text2 = TextInput(title="Title of Seasonality Plot", value='Plot Name')
    text2.on_change('value', update_title2)

    poly_select = Slider(start=1, end=10, step=1, value=1, title='Polynomial')
    poly_select.on_change('value', update_poly)


    steps = ts['time'].iloc[-1] / 10
    season_select = Slider(start=0, end=ts['time'].iloc[-1], step=steps, value=0, title='Season period')
    season_select.on_change('value', update_season)

    #preparing data to go into trend removal graph
    detrended_data = remove_trend(ts, poly_select.value)
    combine = [ts, detrended_data]
    combined_df = pd.concat(combine)
    source = ColumnDataSource(data=combined_df)
    plot = make_decompplot(source)

    #preparing data for seasonality graph
    deseason_data = remove_seasonality(detrended_data, 0)
    combine3 = [ts, deseason_data]
    combined_df3 = pd.concat(combine3)
    source3 = ColumnDataSource(data=combined_df3)
    plot2 = make_seasonplot(source3)

    # Set up layouts and add to document
    # Put controls in a single element.
    controls = WidgetBox(text, poly_select, text2, season_select)

    # Create a row layout
    gridplot = column(plot, plot2)
    formatting = row(controls, gridplot)

    # Make a tab with the layout 
    tab = Panel(child=formatting, title='Decomposition and Seasonality')
    return tab
