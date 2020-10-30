# Import packages.
import pandas as pd
import numpy as np
from .timeseries_stats import rolling_mean, rolling_std
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, ColumnDataSource,
                          Panel, FuncTickFormatter, SingleIntervalTicker,
                          LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Tabs,
                                  CheckboxButtonGroup, RadioButtonGroup,
                                  TableColumn, DataTable, Select, TextInput)
from bokeh.layouts import column, row, WidgetBox, gridplot
from bokeh.palettes import Category20_16

ts_colors = Category20_16


# Timeseries Tab.
def timeseries_tab(ts, hist_ts):

    #Style for the timeseries line plot 
    def timeseries_style(plot):
        plot.legend.location = "top_right"
        plot.legend.click_policy = "hide"
        plot.title.text_font_size = '14pt'
        plot.xaxis.axis_label_text_font_size = '12pt'
        plot.xaxis.axis_label_text_font_style = 'bold'
        plot.yaxis.axis_label_text_font_size = '12pt'
        plot.yaxis.axis_label_text_font_style = 'bold'

        return plot

    # Set up the timeseries line plot
    def make_lineplot(source):
        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('time')
        ttp = [("Time", "$x"), ("Value", "$y")]

        plot = figure(plot_height=400, plot_width=600, tooltips=ttp, title="Plot Name", x_axis_label="Axis label", y_axis_label="Axis label",
                      tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot = timeseries_style(plot)  
        return plot

    # Set up interactive elements 
    def update_title(attrname, old, new):
        plot.title.text = text.value

    def update_x_ax_label(attrname, old, new):
        plot.xaxis.axis_label = text2.value

    def update_y_ax_label(attrname, old, new):
        plot.yaxis.axis_label = text3.value

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

    # Set up widgets: text boxes, mean and standard deviation roller and window slider 
    text = TextInput(title="Title", value='Plot Name')
    text.on_change('value', update_title)
    text2 = TextInput(title="X Axis Label", value='Axis Label')
    text2.on_change('value', update_x_ax_label)
    text3 = TextInput(title="Y Axis Label", value='Axis Label')
    text3.on_change('value', update_y_ax_label)

    rolling_method = Select(value='Mean', title='Statistic', options=['Mean', 'Std. Dev.'])
    rolling_method.on_change('value', update_window)

    window_select = Slider(start=0, end=50, step=1, value=10, title='Window Size')
    window_select.on_change('value', update_window)

    #make the line timeseries plot 
    source = ColumnDataSource(data=ts)
    plot = make_lineplot(source)


    # Set up layouts and add to document
    # Put controls in a single element.
    lineplot_controls = WidgetBox(text, text2, text3, window_select, rolling_method)

    
    # Make plot with histogram
    # Find maximum range of ts.
    hist_ts_range = hist_ts.apply(lambda x: x.max() - x.min())
    range_max = hist_ts_range.max()

    # Function to make a dataset for histogram based on a list of timeseries 
    # and default histogram bin width.
    def make_dataset(timeseries_list, bin_width=5):
        # Dataframe to hold information
        df_to_plot = pd.DataFrame(columns=['proportion', 'left', 'right',
                                           'f_proportion', 'f_interval',
                                           'name', 'color'])


        # Iterate through all the TS.
        for i, timeseries_name in enumerate(timeseries_list):
            # Subset to the carrier
            subset = hist_ts[timeseries_name]

            # Create a histogram with default 5 minute bins
            arr_hist, edges = np.histogram(subset, 
                                           bins=int(range_max / bin_width))

            # Divide the counts by the total to get a proportion
            arr_df = pd.DataFrame({'proportion': arr_hist / np.sum(arr_hist), 
                                   'left': edges[:-1], 'right': edges[1:] })

            # Format the proportion
            arr_df['f_proportion'] = ['%0.5f' % proportion for 
                                      proportion in arr_df['proportion']]

            # Format the interval
            arr_df['f_interval'] = ['%d to %d units' % (left, right) for left, 
                                    right in zip(arr_df['left'], arr_df['right'])]

            # Assign the carrier for labels
            arr_df['name'] = timeseries_name

            # Color each carrier differently
            arr_df['color'] = Category20_16[i]

            # Add to the overall dataframe
            df_to_plot = df_to_plot.append(arr_df)

        # Overall dataframe
        df_to_plot = df_to_plot.sort_values(['name', 'left'])

        return ColumnDataSource(df_to_plot)

    def style(hist):
        # Title
        hist.title.align = 'left'
        hist.title.text_font_size = '14pt'

        # Axis titles
        hist.xaxis.axis_label_text_font_size = '12pt'
        hist.xaxis.axis_label_text_font_style = 'bold'
        hist.yaxis.axis_label_text_font_size = '12pt'
        hist.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        hist.xaxis.major_label_text_font_size = '12pt'
        hist.yaxis.major_label_text_font_size = '12pt'

        return hist

    def make_plot(hist_src):
        # Blank plot with correct labels

        hist = figure(plot_width=700, plot_height=700,
                    title='Histogram of Times Series Data Points',
                    x_axis_label='Bin width', y_axis_label='Proportion')

        # Quad glyphs to create a histogram
        hist.quad(source=hist_src, bottom=0, top = 'proportion', left = 'left', right = 'right',
                color = 'color', fill_alpha = 0.7, hover_fill_color = 'color', legend = 'name',
                hover_fill_alpha = 1.0, line_color = 'black')

        # Hover tool with vline mode
        hover = HoverTool(tooltips=[('Times Series', '@name'), 
                                    ('x', '@f_interval'),
                                    ('Proportion', '@f_proportion')],
                            mode='vline')

        hist.add_tools(hover)

        # Styling.
        hist= style(hist)

        return hist

    def update(attr, old, new):
        hist_ts_to_plot = [hist_ts_selection.labels[i] for i in hist_ts_selection.active]
        new_hist_src = make_dataset(hist_ts_to_plot,
                                    bin_width=binwidth_select.value)
        hist_src.data.update(new_hist_src.data)


    # Widgets for interactivity.
    # Carriers and colors
    available_hist_ts = hist_ts.columns.tolist()
    available_hist_ts.sort()

    hist_ts_selection = CheckboxButtonGroup(labels=available_hist_ts, active=[0, 1])
    hist_ts_selection.on_change('active', update)

    binwidth_select = Slider(start = 1, end = 10, 
    						 step = 1, value = 5,
    						 title = 'Bin Width')
    binwidth_select.on_change('value', update)

    # Call to set initial dataset.
    print(hist_ts_selection.labels, hist_ts_selection.active)
    # Initial ts and data source
    initial_hist_ts = [hist_ts_selection.labels[i] for i in hist_ts_selection.active]

    hist_src = make_dataset(initial_hist_ts, bin_width=binwidth_select.value)

    hist = make_plot(hist_src)

    # Put controls in a single element.
    histogram_controls = WidgetBox(hist_ts_selection, binwidth_select)

    # Create a row layout
    grid = gridplot([[lineplot_controls, plot], [histogram_controls, hist]], plot_width=500, plot_height=500)

    # Make a tab with the layout 
    tab = Panel(child=grid, title='Time Series Plots')

    return tab