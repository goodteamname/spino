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
        for i, timeseries_name in enumerate(src.columns.tolist()):
            p.line(x=ts.index.tolist(), y=src[timeseries_name], legend_label=timeseries_name, color=ts_colors[i], line_width=2)

        # Hover tool with vline mode
        hover = HoverTool(tooltips=[('Times Series', '@name'), 
                                    ('Time', '@x'),
                                    ('Value', '@y')],
                            mode='vline')

        p.add_tools(hover)

        # Styling.
        p = style(p)

        return p

    def update(attr, old, new):
        ts_to_plot = [ts_selection.labels[i] for i in ts_selection.active]

        src = ts[ts_to_plot]

        return src
	    # src.data.update(new_src.data)


    # Widgets for interactivity.
    # Carriers and colors
    available_ts = ts.columns.tolist()
    available_ts.sort()

    ts_colors = Category20_16

    ts_selection = CheckboxGroup(labels=available_ts, active=[0, 1])
    ts_selection.on_change('active', update)

    # Initial dataframe.
    src = ts[available_ts]

    p = make_lineplot(src)

	# Put controls in a single element.
    controls = WidgetBox(ts_selection)

	# Create a row layout
    layout = row(controls, p)

	# Make a tab with the layout 
    tab = Panel(child=layout, title = 'Time Series Plots')

    return tab