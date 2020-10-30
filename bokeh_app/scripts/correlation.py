# Import packages.
from .functions/timeseries_stats import auto_corr, corr
from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Tabs, CheckboxButtonGroup, RadioButtonGroup, TableColumn, DataTable, Select, TextInput)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

# Set the colour palette from bokeh palettes.
ts_colors = Category20_16


# Correlations Tab - takes time series dataframe as input, ts.
def correlations_tab(ts):

    #making dataset using timeseries with default maximum lag of 10
    def make_dataset(ts[['time', ts_available[0]]]), lag=10):

        df_to_plot = auto_corr(ts, lag)

        return ColumnDataSource(df_to_plot) 

    # Make line plot for raw and detrended data.
    def make_autocorrplot(source):

        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('time')

        ttp = [("Time", "$x"), ("Value", "$y")]

        plot_autocorr = figure(plot_height=400, plot_width=600, tooltips=ttp, title="Autocorrelation",
                    tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot_autocorr.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot_autocorr.legend.location = "top_left"
        plot_autocorr.legend.click_policy = "hide"

        return plot_autocorr

    # Set up callbacks
    def update_title(attrname, old, new):
        plot_autocorr.title.text = text.value

    def update_data(attrname, old, new):
        new_source_autocorr = ColumnDataSource(data=ts[['time', ts_select.value]])
        make_dataset()
        source_autocorr.data.update(new_source_autocorr.data)
        # new_hist_src = make_dataset(hist_ts_to_plot,
        #                             bin_width=binwidth_select.value)
        #hist_src.data.update(new_hist_src.data)

    # Set up widgets.
    # Input for plot titles
    text = TextInput(title="Title", value='Plot Name')
    text.on_change('value', update_title)
    # Select time series for Autocorrelation
    ts_available = ts.columns.tolist()
    ts_available.remove('time')
    ts_select = Select(value=ts_available[0], title='Time Series', options=ts_available)
    ts_select.on_change('value', update_data)
    # Select lag value
    lag_select = Slider(start=0, end=10, step=1, value=0, title='Lag')
    lag_select.on_change('value', update_data)

    # Initial state and plotting.

    source_autocorr = ColumnDataSource(data=ts[['time', ts_available[0]]])

    plot_autocorr = make_lineplot_autocorr(source_autocorr)


    # Set up layouts and add to document.
    # Put controls in a single element.
    controls = WidgetBox(text, ts_select, component_select)

    # Create a row layout
    layout = row(controls, plot_autocorr)

    # Make a tab with the layout.
    tab = Panel(child=layout, title='Autocorrelation and Correlation')
    return tab