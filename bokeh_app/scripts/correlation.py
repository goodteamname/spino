# Import packages.
from .functions.timeseries_stats import auto_corr, corr
from bokeh.plotting import figure
from bokeh.models import (HoverTool, ColumnDataSource,
                          Panel,
                          LinearAxis)
from bokeh.models.widgets import (Slider,
                                  Select, TextInput)
from bokeh.layouts import WidgetBox, gridplot


# Correlations Tab - takes time series dataframe as input, ts.
def correlations_tab(ts):

    # Making dataset using the autocorrelation function,
    # input is a timeseries and default maximum lag of 10
    def make_dataset_autocorr(ts, col, lag):

        df_to_plot_autocorr = auto_corr(ts[col], lag)

        return ColumnDataSource(df_to_plot_autocorr)

    # Making autocorrelation plot
    def make_autocorrplot(source):
        ttp = [("Lag", "$x"), ("Autocorrelation", "$y")]

        plot_autocorr = figure(plot_height=400, plot_width=600, tooltips=ttp,
                               title="Autocorrelation",
                               x_axis_label="Lag", 
                               y_axis_label="Autocorrelation",
                               tools="hover, pan, zoom_in, zoom_out, reset, save")
        plot_autocorr.circle('lags', 'auto_corrs', source=source)
        plot_autocorr.line('lags', 'auto_corrs', source=source)
        plot_autocorr.title.text_font_size = '14pt'
        plot_autocorr.xaxis.axis_label_text_font_size = '12pt'
        plot_autocorr.xaxis.axis_label_text_font_style = 'bold'
        plot_autocorr.yaxis.axis_label_text_font_size = '12pt'
        plot_autocorr.yaxis.axis_label_text_font_style = 'bold'

        return plot_autocorr

    # Set up callbacks to interactively update data when different
    # time series and lag values are selected, and letting the user
    # set the title
    def update_title(attrname, old, new):
        plot_autocorr.title.text = text_autocorr.value

    def update_data_autocorr(attrname, old, new):
        new_source_autocorr = make_dataset_autocorr(ts,
                                                    ts_select_autocorr.value,
                                                    lag=lag_select_autocorr.value)
        source_autocorr.data.update(new_source_autocorr.data)


    # Set up widgets.
    # Input for plot titles
    text_autocorr = TextInput(title="Title", value='Autocorrelation')
    text_autocorr.on_change('value', update_title)
    # Select time series for Autocorrelation
    ts_available = ts.columns.tolist()
    print(ts_available)
    ts_available.remove('time')
    ts_select_autocorr = Select(value=ts_available[0], title='Time Series',
                                options=ts_available)
    ts_select_autocorr.on_change('value', update_data_autocorr)
    # Select lag value
    lag_select_autocorr = Slider(start=10, end=100, step=1, value=10,
                                 title='Lag')
    lag_select_autocorr.on_change('value', update_data_autocorr)

    # Initial state and plotting.
    source_autocorr = make_dataset_autocorr(ts, ts_available[0], 10)

    plot_autocorr = make_autocorrplot(source_autocorr)


    # Set up layouts and add to document.
    # Put controls in a single element.
    controls_autocorr = WidgetBox(text_autocorr, ts_select_autocorr,
                                  lag_select_autocorr)

    # making dataset using the correlation function
    # inputs are two different timeseries and default maximum lag of 10
    def make_dataset_corr(ts, col1, col2, lag):

        df_to_plot_corr = corr(ts[col1], ts[col2], lag)

        return ColumnDataSource(df_to_plot_corr)

    # Make line plot for correlation
    def make_corrplot(source):
        ttp = [("Lag", "$x"), ("Autocorrelation", "$y")]

        plot_corr = figure(plot_height=400, plot_width=600, tooltips=ttp,
                           title="Correlation",
                           x_axis_label="Lag", y_axis_label="Correlation",
                           tools="hover, pan, zoom_in, zoom_out, reset, save")
        plot_corr.circle('lags', 'corrs', source=source)
        plot_corr.line('lags', 'corrs', source=source)
        plot_corr.title.text_font_size = '14pt'
        plot_corr.xaxis.axis_label_text_font_size = '12pt'
        plot_corr.xaxis.axis_label_text_font_style = 'bold'
        plot_corr.yaxis.axis_label_text_font_size = '12pt'
        plot_corr.yaxis.axis_label_text_font_style = 'bold'

        return plot_corr

    # Set up callbacks to interactively update data when different
    # time series and lag values are selected, and letting the user
    # set the title
    def update_title(attrname, old, new):
        plot_corr.title.text = text_corr.value

    def update_data_corr(attrname, old, new):
        new_source_corr = make_dataset_corr(ts, ts_select_corr.value,
                                            ts_select2_corr.value,
                                            lag=lag_select_corr.value)
        source_corr.data.update(new_source_corr.data)


    # Set up widgets.
    # Input for plot titles
    text_corr = TextInput(title="Title", value='Correlation')
    text_corr.on_change('value', update_title)
    # Select time series for Autocorrelation
    ts_available = ts.columns.tolist()
    ts_available.remove('time')
    ts_select_corr = Select(value=ts_available[0], title='Time Series',
                            options=ts_available)
    ts_select_corr.on_change('value', update_data_corr)
    ts_select2_corr = Select(value=ts_available[1], title='Time Series',
                             options=ts_available)
    ts_select2_corr.on_change('value', update_data_corr)
    # Select lag value
    lag_select_corr = Slider(start=10, end=100, step=1, value=10, title='Lag')
    lag_select_corr.on_change('value', update_data_corr)

    # Initial state and plotting.
    source_corr = make_dataset_corr(ts, ts_available[0], ts_available[1], 10)

    plot_corr = make_corrplot(source_corr)


    # Set up layouts and add to document.
    # Put controls in a single element.
    controls_corr = WidgetBox(text_corr, ts_select_corr,
                              ts_select2_corr, lag_select_corr)

    # Create a row layout
    grid = gridplot([[controls_autocorr, plot_autocorr],
                     [controls_corr, plot_corr]],
                    plot_width=500, plot_height=500)

    # Make a tab with the layout.
    tab = Panel(child=grid, title='Autocorrelation and Correlation')
    return tab
