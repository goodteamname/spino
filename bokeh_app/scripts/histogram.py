# A histogram plot script will go here.

# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Tabs, CheckboxButtonGroup, TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

# Make plot with histogram and return tab
def histogram_tab(ts):

    # Find maximum range of ts.
    print(ts)
    ts_range = ts.apply(lambda x: x.max() - x.min())
    range_max = ts_range.max()

    # Function to make a dataset for histogram based on a list of timeseries and default histogram bin width.
    def make_dataset(timeseries_list, bin_width = 5):
        # Dataframe to hold information
        df_to_plot = pd.DataFrame(columns=['proportion', 'left', 'right', 
                                            'f_proportion', 'f_interval',
                                            'name', 'color'])


        # Iterate through all the TS.
        for i, timeseries_name in enumerate(timeseries_list):
            # Subset to the carrier
            subset = ts[timeseries_name]

            # Create a histogram with default 5 minute bins
            print(subset)
            print(range_max)
            print(bin_width)
            arr_hist, edges = np.histogram(subset, bins=int(range_max / bin_width))

            # Divide the counts by the total to get a proportion
            arr_df = pd.DataFrame({'proportion': arr_hist / np.sum(arr_hist), 'left': edges[:-1], 'right': edges[1:] })

            # Format the proportion 
            arr_df['f_proportion'] = ['%0.5f' % proportion for proportion in arr_df['proportion']]

            # Format the interval
            arr_df['f_interval'] = ['%d to %d units' % (left, right) for left, right in zip(arr_df['left'], arr_df['right'])]

            # Assign the carrier for labels
            arr_df['name'] = timeseries_name

            # Color each carrier differently
            arr_df['color'] = Category20_16[i]

            # Add to the overall dataframe
            df_to_plot = df_to_plot.append(arr_df)

        # Overall dataframe
        df_to_plot = df_to_plot.sort_values(['name', 'left'])

        return ColumnDataSource(df_to_plot)

    def style(p):
        #Title
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p

    def make_plot(src):
        # Blank plot with correct labels
        p = figure(plot_width=700, plot_height=700, 
                    title='Histogram of Times Series Data Points',
                    x_axis_label='x', y_axis_label='Proportion')

        # Quad glyphs to create a histogram
        p.quad(source=src, bottom=0, top = 'proportion', left = 'left', right = 'right',
                color = 'color', fill_alpha = 0.7, hover_fill_color = 'color', legend = 'name',
                hover_fill_alpha = 1.0, line_color = 'black')

        # Hover tool with vline mode
        hover = HoverTool(tooltips=[('Times Series', '@name'), 
                                    ('x', '@f_interval'),
                                    ('Proportion', '@f_proportion')],
                            mode='vline')

        p.add_tools(hover)

        # Styling.
        p = style(p)

        return p

    def update(attr, old, new):
	    ts_to_plot = [ts_selection.labels[i] for i in ts_selection.active]

	    new_src = make_dataset(ts_to_plot,
							   bin_width = binwidth_select.value)


	    src.data.update(new_src.data)


    # Widgets for interactivity.
    # Carriers and colors
    available_ts = ts.columns.tolist()
    available_ts.sort()

    print(available_ts, len(available_ts))


    ts_colors = Category20_16
    # ts_colors.sort()

    ts_selection = CheckboxButtonGroup(labels=available_ts, active = [0, 1])
    ts_selection.on_change('active', update)

    binwidth_select = Slider(start = 1, end = 10, 
							 step = 1, value = 5,
							 title = 'Bin Width (units)')
    binwidth_select.on_change('value', update)

    # Call to set initial dataset.
    print(ts_selection.labels, ts_selection.active)
	# Initial ts and data source
    initial_ts = [ts_selection.labels[i] for i in ts_selection.active]

    src = make_dataset(initial_ts, bin_width = binwidth_select.value)

    p = make_plot(src)

	# Put controls in a single element.
    controls = WidgetBox(ts_selection, binwidth_select)

	# Create a row layout
    layout = row(controls, p)

	# Make a tab with the layout 
    tab = Panel(child=layout, title = 'Histogram')

    return tab