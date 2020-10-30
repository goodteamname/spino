# Import packages.
from .functions.timeseries_stats import remove_trend
from .functions.fourier_functions import dfs, fourier_to_freq_spectrum, calc_residuals
from bokeh.plotting import figure
from bokeh.models import (ColumnDataSource, Panel)
from bokeh.models.widgets import (Slider, TableColumn, DataTable, Select)
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

        plot_q1 = figure(plot_height=400, plot_width=400, tooltips=ttp, title="Time Series",
                         tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot_q1.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot_q1.legend.location = "top_left"
        plot_q1.legend.click_policy = "hide"

        return plot_q1

    # Make line and circle plot for power spectrum.
    def make_lineplot_q2(source):

        ttp = [("Frequency", "$x"), ("Power", "$y")]

        plot_q2 = figure(plot_height=400, plot_width=400, tooltips=ttp, title="Power Spectrum",
                         tools="hover, pan, zoom_in, zoom_out, reset, save")
        plot_q2.line('frequency', 'power', source=source, line_width=3, line_color=ts_colors[10])
        plot_q2.circle('frequency', 'power', source=source, fill_color="white", size=8)

        return plot_q2

    # Make time series plot for fourier components.
    def make_lineplot_q3(source):
        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('times')

        ttp = [("Time", "$x"), ("Value", "$y")]

        plot_q3 = figure(plot_height=400, plot_width=400, tooltips=ttp, title="Top 3 Fourier Components",
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

        plot_q4 = figure(plot_height=400, plot_width=400, tooltips=ttp, title="Fourier Residuals",
                         tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot_q4.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot_q4.legend.location = "top_left"
        plot_q4.legend.click_policy = "hide"

        return plot_q4

    # Make Summary Table of top 5 fourier components.
    def make_summarytable(source):
        columns = [
            TableColumn(field="frequency", title="Frequency"),
            TableColumn(field="amplitude", title="Amplitude"),
            TableColumn(field="power", title="Power")
        ]
        summary_table = DataTable(source=source, columns=columns, width=400, height=200)
        return summary_table

    # Make dataset function.
    def make_dataset(ts, col, N):
        ts_data = ts[['time', col]]
        ts_data.columns = ['time', 'raw_data']
        if N == 0:
            ts_data['detrended'] = ts_data['raw_data']
            return ts_data
        else:
            ts_data.columns = ['time', 'raw_data']
            ts_detrended = remove_trend(ts_data, N)
            ts_data['detrended'] = ts_detrended.iloc[:, 1]
            return ts_data

    ##############################################################
    # Set up callbacks

    def update_data(attrname, old, new):
        # Update data with selected timeseries and detrend with order N polynomial.
        new_data = make_dataset(ts, ts_select.value, order_select.value)

        update_dataset(new_data=new_data)
        update_powerspectrum(new_data=new_data)
        update_fourier1(new_data=new_data)
        update_fourier2(new_data=new_data)
        update_summarytable(new_data=new_data)

    def update_dataset(new_data):
        # Store updated data in CDS format.
        new_source_q1 = ColumnDataSource(data=new_data)
        # Update CDS to plot_q1.
        source_q1.data.update(new_source_q1.data)
        print(source_q1.data)

    def update_powerspectrum(new_data):
        # Compute power spectrum.
        # If timeseries has not been detrended (i.e. size == 2), use raw data in power spectrum.
        if len(new_data.columns) == 2:
            pspec_data = fourier_to_freq_spectrum(new_data.iloc[:, 1], new_data['time'])
        else:
            pspec_data = fourier_to_freq_spectrum(new_data.iloc[:, 2], new_data['time'])
        # Store update data in CDS format.
        new_source_q2 = ColumnDataSource(data=pspec_data)
        # Update CDS to plot_q2
        source_q2.data.update(new_source_q2.data)
        print(source_q2.data)

    def update_fourier1(new_data):
        # Compute fourier components.
        if len(new_data.columns) == 2:
            alpha0, coef = dfs(new_data.iloc[:, 1])
            top_components_for_approx, _, _ = calc_residuals(alpha0, coef, new_data.iloc[:, 1], new_data['time'], components=5)
        else:
            alpha0, coef = dfs(new_data.iloc[:, 2])
            top_components_for_approx, _, _ = calc_residuals(alpha0, coef, new_data.iloc[:, 2], new_data['time'], components=5)

        new_source_q3 = ColumnDataSource(data=top_components_for_approx)
        source_q3.data.update(new_source_q3.data)
        print(source_q3.data)

    def update_fourier2(new_data):
        if len(new_data.columns) == 2:
            alpha0, coef = dfs(new_data.iloc[:, 1])
            _, _, residual_df = calc_residuals(alpha0, coef, new_data.iloc[:, 1], new_data['time'], components=component_select.value)
        else:
            alpha0, coef = dfs(new_data.iloc[:, 2])
            _, _, residual_df = calc_residuals(alpha0, coef, new_data.iloc[:, 2], new_data['time'], components=component_select.value)

        new_source_q4 = ColumnDataSource(data=residual_df)
        source_q4.data.update(new_source_q4.data)
        print(source_q4.data)

    def update_summarytable(new_data):
        if len(new_data.columns) == 2:
            alpha0, coef = dfs(new_data.iloc[:, 1])
            _, summary_table, _ = calc_residuals(alpha0, coef, new_data.iloc[:, 1], new_data['time'], components=5)
        else:
            alpha0, coef = dfs(new_data.iloc[:, 2])
            _, summary_table, _ = calc_residuals(alpha0, coef, new_data.iloc[:, 2], new_data['time'], components=5)

        new_source_summarytable = ColumnDataSource(data=summary_table)
        source_summarytable.data.update(new_source_summarytable.data)
        print(source_summarytable.data)

    # Set up widgets.
    # Select time series for Spectral Analysis.
    ts_available = ts.columns.tolist()
    ts_available.remove('time')
    ts_select = Select(value=ts_available[0], title='Time Series', options=ts_available)
    ts_select.on_change('value', update_data)
    # Select order of polynomial for removing trend.
    order_select = Slider(start=0, end=10, step=1, value=0, title='Detrending Polynomial Order')
    order_select.on_change('value', update_data)
    # Select no. components for spectral analysis.
    component_select = Slider(start=0, end=20, step=1, value=5, title='No. Fourier Components')
    component_select.on_change('value', update_data)

##############################################################
    # Initial state and plotting.

    # Ensuring ts dataframe has odd no. elements.
    if (len(ts) % 2) == 0:
        # Remove last row when even no. elements.
        ts.drop(ts.tail(1).index, inplace=True)
    else:
        pass

    # Make initial dataset with first time series column by default.
    initial_data = make_dataset(ts, ts_available[0], 0)
    source_q1 = ColumnDataSource(data=initial_data)
    # Compute initial power spectrum for default time series.
    initial_pspec = fourier_to_freq_spectrum(initial_data.iloc[:, 1], initial_data['time'])
    source_q2 = ColumnDataSource(data=initial_pspec)
    # Compute initial fourier components for default time series.
    alpha0, coef = dfs(initial_data.iloc[:, 1])
    top_components_for_approx, summary_table, residual_df = calc_residuals(alpha0, coef, initial_data.iloc[:, 1], initial_data['time'], components=5)

    source_q3 = ColumnDataSource(data=top_components_for_approx)
    source_q4 = ColumnDataSource(data=residual_df)

    source_summarytable = ColumnDataSource(data=summary_table)

    plot_q1 = make_lineplot_q1(source_q1)
    plot_q2 = make_lineplot_q2(source_q2)
    plot_q3 = make_lineplot_q3(source_q3)
    plot_q4 = make_lineplot_q4(source_q4)
    summary_table = make_summarytable(source_summarytable)

    # Set up layouts and add to document.
    # Put controls in a single element.
    controls = WidgetBox(ts_select, order_select, component_select)

    # Create a row layout
    layout = row(controls, gridplot([[plot_q1, plot_q2], [plot_q3, plot_q4], [summary_table, None]]))

    # Make a tab with the layout.
    tab = Panel(child=layout, title='Spectral Analysis')
    return tab
