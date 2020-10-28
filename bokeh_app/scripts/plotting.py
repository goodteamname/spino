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
def plotting_tab(ts):

    def make_dataset(timeseries_list):

        df_to_plot = pd.DataFrame(columns=['values', 'time',
                                            'f_value', 'f_time',
                                            'name', 'color'])

        # Iterate through all the TS.
        for i, timeseries_name in enumerate(timeseries_list):
            # Subset to the carrier
            subset = ts[timeseries_name]

            # Define values.
            arr_df = pd.DataFrame({'values': subset, 'time': ts.index.tolist() })

            # Format the values
            arr_df['f_value'] = ['%0.2f' % values for values in arr_df['values']]

            # Format the interval
            arr_df['f_time'] = ['%0.2f' % time for time in arr_df['time']]

            # Assign the carrier for labels
            arr_df['name'] = timeseries_name

            # Color each carrier differently
            arr_df['color'] = Category20_16[i]

            # Add to the overall dataframe
            df_to_plot = df_to_plot.append(arr_df)

        # Overall dataframe
        df_to_plot = df_to_plot.sort_values('name')

        return ColumnDataSource(df_to_plot)

    # For extra functionality.
    # if distribution == 'Smoothed':
    #     window, order = 51, 3
    #     for key in STATISTICS:
    #         df[key] = savgol_filter(df[key], window, order)

    def style(p):
        # Title
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

    def make_lineplot(src):
        # Blank plot with correct labels.
        p = figure(plot_width=700, plot_height=700,
                    title='Plot of Time Series',
                    x_axis_label='Time', y_axis_label='Variable')

        # line glyphs to create a multiple line plots.
        p.quad(top='values', bottom=0, source=src, hover_fill_color = 'color', legend_label= 'name',
                hover_fill_alpha = 1.0, line_color = 'color')

        # Hover tool with vline mode
        hover = HoverTool(tooltips=[('Times Series', '@name'), 
                                    ('Time', '@f_time'),
                                    ('Value', '@f_value')],
                            mode='vline')

        p.add_tools(hover)

        # Styling.
        p = style(p)

        return p

    def update(attr, old, new):
        ts_to_plot = [ts_selection.labels[i] for i in ts_selection.active]

        new_src = make_dataset(ts_to_plot)

        src.data.update(new_src.data)


    # Widgets for interactivity.
    # Carriers and colors
    available_ts = ts.columns.tolist()
    available_ts.sort()

    ts_colors = Category20_16

    ts_selection = CheckboxGroup(labels=available_ts, active=[0, 1])
    ts_selection.on_change('active', update)

	# Initial ts and data source
    initial_ts = [ts_selection.labels[i] for i in ts_selection.active]

    src = make_dataset(initial_ts)

    p = make_lineplot(src)

	# Put controls in a single element.
    controls = WidgetBox(ts_selection)

	# Create a row layout
    layout = row(controls, p)

	# Make a tab with the layout 
    tab = Panel(child=layout, title = 'Time Series Plots')

    return tab