import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import (CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Tabs, CheckboxButtonGroup, TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

ts = pd.read_csv("./bokeh_app/data/test_timeseries.csv", skiprows=1, delimiter=",", names=['time', 'y1', 'y2', 'y3'])
ts.set_index('time', inplace=True, drop=True)

ts_colors = Category20_16


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
    # for i, timeseries_name in enumerate(src.columns.tolist()):
    p.line(x=ts.index.tolist(), y=src['y1'], legend_label='y1', color=ts_colors[0], line_width=2)
    p.line(x=ts.index.tolist(), y=src['y2'], legend_label='y2', color=ts_colors[1], line_width=2)
    p.line(x=ts.index.tolist(), y=src['y3'], legend_label='y3', color=ts_colors[2], line_width=2)

    # Hover tool with vline mode
    hover = HoverTool(tooltips=[('Times Series', '@name'),
                                ('Time', '@x'),
                                ('Value', '@y')],
                        mode='vline')

    p.add_tools(hover)

    # Styling.
    p = style(p)

    return p


ts_plot = make_lineplot(ts)
show(ts_plot)
