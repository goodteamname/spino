# Import packages.
from .timeseries_stats import remove_trend
from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Tabs, CheckboxButtonGroup, RadioButtonGroup, TableColumn, DataTable, Select, TextInput)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

# Set the colour palette from bokeh palettes.
ts_colors = Category20_16


# Spectral Tab - takes time series dataframe as input, ts.
def spectral_tab(ts):
    # Make line plot for raw and detrended data.
    def make_lineplot_q1(source):
        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('time')

        ttp = [("Time", "$x"), ("Value", "$y")]

        plot_q1 = figure(plot_height=400, plot_width=600, tooltips=ttp, title="Time Series",
                    tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot_q1.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot_q1.legend.location = "top_left"
        plot_q1.legend.click_policy = "hide"

        return plot_q1

    # Make line and circle plot for power spectrum.
    def make_lineplot_q2(source):

        ttp = [("Frequency", "$x"), ("Power", "$y")]

        plot_q2 = figure(plot_height=400, plot_width=600, tooltips=ttp, title="Power Spectrum",
                    tools="hover, pan, zoom_in, zoom_out, reset, save")
        plot_q2.line('frequency', 'power', source=source, line_width=3, line_color=ts_colors[10])
        plot_q2.circle('frequency', 'power', source=source, fill_color="white", size=8)
        plot_q2.legend.location = "top_left"

        return plot_q2

    # Make time series plot for fourier components.
    def make_lineplot_q3(source):
        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('time')

        ttp = [("Time", "$x"), ("Value", "$y")]

        plot_q3 = figure(plot_height=400, plot_width=600, tooltips=ttp, title="Components",
                    tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot_q3.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot_q3.legend.location = "top_left"
        plot_q3.legend.click_policy = "hide"

        return plot_q3

    # Make time series plot for fourier components.
    def make_lineplot_q4(source):
        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('time')

        ttp = [("Time", "$x"), ("Value", "$y")]

        plot_q4 = figure(plot_height=400, plot_width=600, tooltips=ttp, title="Residuals",
                    tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot_q4.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot_q4.legend.location = "top_left"
        plot_q4.legend.click_policy = "hide"

        return plot_q4

    # Set up callbacks
    def update_title(attrname, old, new):
        plot_q1.title.text = text.value


    def update_data(attrname, old, new):
        new_source_q1 = ColumnDataSource(data=ts[['time', ts_select.value]])

        source_q1.data.update(new_source_q1.data)

    # Set up widgets.
    # Input for plot titles.
    text = TextInput(title="Title", value='Plot Name')
    text.on_change('value', update_title)
    # Select time series for Spectral Analysis.
    ts_available = ts.columns.tolist()
    ts_available.remove('time')
    ts_select = Select(value=ts_available[0], title='Time Series', options=ts_available)
    ts_select.on_change('value', update_data)
    # Select order of polynomial for removing trend.
    order_select = Slider(start=0, end=10, step=1, value=0, title='Detrending Polynomial Order')
    order_select.on_change('value', update_data)
    # Select no. components for spectral analysis.
    component_select = Slider(start=0, end=10, step=1, value=0, title='No. Fourier Components')
    component_select.on_change('value', update_data)

    # Initial state and plotting.

    source_q1 = ColumnDataSource(data=ts[['time', ts_available[0]]])
    source_q2 = ColumnDataSource(data=ts)
    source_q3 = ColumnDataSource(data=ts)
    source_q4 = ColumnDataSource(data=ts)

    plot_q1 = make_lineplot_q1(source_q1)
    plot_q2 = make_lineplot_q2(source_q2)
    plot_q3 = make_lineplot_q3(source_q3)
    plot_q4 = make_lineplot_q4(source_q4)

    # Set up layouts and add to document.
    # Put controls in a single element.
    controls = WidgetBox(text, ts_select, component_select)

    # Create a row layout
    layout = row(controls, plot_q1, plot_q2, plot_q3, plot_q4)

    # Make a tab with the layout.
    tab = Panel(child=layout, title='Spectral Analysis')
    return tab
