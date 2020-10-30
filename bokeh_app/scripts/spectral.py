# Import packages.
from .functions.timeseries_stats import remove_trend
from .functions.fourier_functions import dfs, fourier_to_freq_spectrum, calc_residuals
from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Tabs, RadioButtonGroup, TableColumn, DataTable, Select, TextInput)
from bokeh.layouts import row, WidgetBox, gridplot
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

        plot_q1 = figure(plot_height=300, plot_width=300, tooltips=ttp, title="Time Series",
                    tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot_q1.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot_q1.legend.location = "top_left"
        plot_q1.legend.click_policy = "hide"

        return plot_q1

    # Make line and circle plot for power spectrum.
    def make_lineplot_q2(source):

        ttp = [("Frequency", "$x"), ("Power", "$y")]

        plot_q2 = figure(plot_height=300, plot_width=300, tooltips=ttp, title="Power Spectrum",
                    tools="hover, pan, zoom_in, zoom_out, reset, save")
        plot_q2.line('frequency', 'power', source=source, line_width=3, line_color=ts_colors[10])
        plot_q2.circle('frequency', 'power', source=source, fill_color="white", size=8)
        plot_q2.legend.location = "top_left"

        return plot_q2

    # Make time series plot for fourier components.
    def make_lineplot_q3(source):
        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('times')

        ttp = [("Time", "$x"), ("Value", "$y")]

        plot_q3 = figure(plot_height=300, plot_width=300, tooltips=ttp, title="Components",
                    tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot_q3.line('times', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot_q3.legend.location = "top_left"
        plot_q3.legend.click_policy = "hide"

        return plot_q3

    # Make time series plot for fourier components.
    def make_lineplot_q4(source):
        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('time')

        ttp = [("Time", "$x"), ("Value", "$y")]

        plot_q4 = figure(plot_height=300, plot_width=300, tooltips=ttp, title="Residuals",
                    tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot_q4.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot_q4.legend.location = "top_left"
        plot_q4.legend.click_policy = "hide"

        return plot_q4

    # Make dataset function.
    def make_dataset(ts, col, N):
        ts_data = ts[['time', col]]
        if N == 0:
            return ts_data
        else:
            ts_detrended = remove_trend(ts_data, N)
            ts_data['detrended'] = ts_detrended.iloc[:,1]
            return ts_data

    ##############################################################
    # Set up callbacks
    def update_title(attrname, old, new):

        plot_q1.title.text = text.value

    def update_data(attrname, old, new):
        # Update data with selected timeseries and detrend with order N polynomial.
        new_data = make_dataset(ts, ts_select.value, order_select.value)
        # Store updated data in CDS format.
        new_source_q1 = ColumnDataSource(data=new_data)
        # Update CDS to plot_q1.
        source_q1.data.update(new_source_q1.data)

        # Compute power spectrum.
        # If timeseries has not been detrended (i.e. size == 2), use raw data in power spectrum.
        if new_data.size == 2:
            pspec_data = fourier_to_freq_spectrum(new_data.iloc[:,1], new_data['time'])
        else:
            pspec_data = fourier_to_freq_spectrum(new_data.iloc[:,2], new_data['time'])
        # Store update data in CDS format.
        new_source_q2 = ColumnDataSource(data=pspec_data)
        # Update CDS to plot_q2
        source_q2.data.update(new_source_q2.data)

        # Compute fourier components.
        if new_data.size == 2:
            alpha0, coef = dfs(new_data.iloc[:,1])
            top_components_for_approx, summary_table, residual_df = calc_residuals(alpha0, coef, new_data.iloc[:,1], new_data['time'], components=component_select.value)
        else:
            alpha0, coef = dfs(new_data.iloc[:,2])
            top_components_for_approx, summary_table, residual_df = calc_residuals(alpha0, coef, new_data.iloc[:,2], new_data['time'], components=component_select.value)

        new_source_q3 = ColumnDataSource(top_components_for_approx)
        source_q3.data.update(new_source_q3)
        new_source_q4 = ColumnDataSource(residual_df)
        source_q4.data.update(new_source_q4)

    # Set up widgets.
    # Input for Plot Titles.
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
    component_select = Slider(start=0, end=20, step=1, value=3, title='No. Fourier Components')
    component_select.on_change('value', update_data)

##############################################################
    # Initial state and plotting.

    # Ensuring ts dataframe has odd no. elements.
    if (len(ts)%2) == 0:
        # Remove last row when even no. elements.
        ts.drop(ts.tail(1).index,inplace=True)
    else:
        pass

    # Make initial dataset with first time series column by default.
    initial_data = make_dataset(ts, ts_available[0], 0)
    print(initial_data.iloc[:,1])
    source_q1 = ColumnDataSource(data=initial_data)
    # Compute initial power spectrum for default time series.
    initial_pspec = fourier_to_freq_spectrum(initial_data.iloc[:,1], initial_data['time'])
    source_q2 = ColumnDataSource(data=initial_pspec)
    # Compute initial fourier components for default time series.
    alpha0, coef = dfs(initial_data.iloc[:,1])
    top_components_for_approx, summary_table, residual_df = calc_residuals(alpha0, coef, initial_data.iloc[:,1], initial_data['time'], components=3)

    source_q3 = ColumnDataSource(data=top_components_for_approx)
    source_q4 = ColumnDataSource(data=residual_df)

    plot_q1 = make_lineplot_q1(source_q1)
    plot_q2 = make_lineplot_q2(source_q2)
    plot_q3 = make_lineplot_q3(source_q3)
    plot_q4 = make_lineplot_q4(source_q4)

    # Set up layouts and add to document.
    # Put controls in a single element.
    controls = WidgetBox(text, ts_select, order_select, component_select)

    # Create a row layout
    layout = row(controls, gridplot([[plot_q1, plot_q2], [plot_q3, plot_q4]]))

    # Make a tab with the layout.
    tab = Panel(child=layout, title='Spectral Analysis')
    return tab
