# Import packages.
import pandas as pd
from scripts.functions.timeseries_stats import remove_trend, remove_seasonality
from bokeh.plotting import figure
from bokeh.models import (ColumnDataSource, Panel)
from bokeh.models.widgets import (Slider, TextInput, Select, Div)
from bokeh.layouts import row, column, WidgetBox
from bokeh.palettes import Category20_16

ts_colors = Category20_16


# decomp Tab.
def decomp_tab(ts):

    # Set up plot.
    def make_decompplot(source):
        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('time')

        ttp = [("Time", "$x"), ("Value", "$y")]

        plot = figure(plot_height=400, plot_width=600, tooltips=ttp, title="Plot Name",
                      tools="hover, pan, zoom_in, zoom_out, reset, save")
        for i, name in enumerate(ts_list):
            plot.line('time', name, source=source, line_width=3, line_color=ts_colors[i], legend_label=name)

        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"

        return plot

    # Set up plot
    def make_seasonplot(source):
        ts_list = source.column_names
        ts_list.remove('index')
        ts_list.remove('time')
        ts_list.remove('time_diff')
        ts_list.remove('data')

        ttp = [("Time", "$x"), ("Value", "$y")]

        plot = figure(plot_height=400, plot_width=600, tooltips=ttp, title="Plot Name",
                      tools="hover, pan, zoom_in, zoom_out, reset, save")

        plot.line('time', 'data', source=source, line_width=3, line_color=ts_colors[0], legend_label='data')

        plot.line('time_diff', 'detrended_data', source=source, line_width=3, line_color=ts_colors[2], legend_label='diff_data')

        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"

        return plot

    # Make dataset function.
    def make_dataset(ts, col):
        ts_data = ts[['time', col]]
        ts_data.columns = ['time', 'data']
        return ts_data

##################################################################
    # Set up callbacks
    def update_title(attrname, old, new):
        plot1.title.text = text1.value

    def update_title2(attrname, old, new):
        plot2.title.text = text2.value

    def update_x_ax_label(attrname, old, new):
        plot1.xaxis.axis_label = xaxis.value
        plot2.xaxis.axis_label = xaxis.value

    def update_y_ax_label(attrname, old, new):
        plot1.yaxis.axis_label = yaxis.value
        plot2.xaxis.axis_label = yaxis.value

    def update_data(attrname, old, new):
        # Update data with selected timeseries.
        new_data = make_dataset(ts, ts_select.value)

        update_poly(new_data=new_data)
        update_season(new_data=new_data)

    def update_poly(new_data):
        if poly_select.value == 0:
            pass
        else:
            # poly_select.value = new

            detrended_data = remove_trend(new_data, poly_select.value)
            combine = [new_data, detrended_data]
            combined_df = pd.concat(combine)
            newsource1 = ColumnDataSource(data=combined_df)
            source_p1.data.update(newsource1.data)

    def update_season(new_data):
        if season_select.value == 0:
            pass
        else:
            # season_select.value = new

            detrended_data = remove_trend(new_data, poly_select.value)
            deseason_data = remove_seasonality(detrended_data[['time', 'detrended_data']], season_select.value)
            combine = [new_data, deseason_data]
            combined_df = pd.concat(combine)
            newsource2 = ColumnDataSource(data=combined_df)
            source_p2.data.update(newsource2.data)

    # Set up widgets
    text1 = TextInput(title="Title of Trend Plot", value='Plot Name')
    text1.on_change('value', update_title)

    text2 = TextInput(title="Title of Difference Plot", value='Plot Name')
    text2.on_change('value', update_title2)

    xaxis = TextInput(title="x axis label", value='Axis Label')
    xaxis.on_change('value', update_x_ax_label)
    yaxis = TextInput(title="y axis label", value='Axis Label')
    yaxis.on_change('value', update_y_ax_label)

    div1 = Div(text="""<b>Plot Attributes:</b> <br> Modify axis labels. <br>""")
    div2 = Div(text="""<b>Detrend Time Series:</b> <br> Specify the order of a polynomial to fit and detrend your data with. <br>""")
    div3 = Div(text="""<b>Seasonal Differencing:</b> <br> Take the difference between an observation and its value in the previous season. <br>""")

    # Select time series for decomposition.
    ts_available = ts.columns.tolist()
    ts_available.remove('time')
    ts_select = Select(value=ts_available[0], title='Time Series', options=ts_available)
    ts_select.on_change('value', update_data)

    # Slider for polynomial detrending.
    poly_select = Slider(start=1, end=10, step=1, value=1, title='Polynomial Order')
    poly_select.on_change('value', update_data)

    # Slider for removing seasonality.
    steps = ts['time'].iloc[-1] / 20
    season_select = Slider(start=0, end=ts['time'].iloc[-1], step=steps, value=0, title='Seasonal Difference (period)')
    season_select.on_change('value', update_data)

    # Prepare initial data for trend removal.
    ts_initial = make_dataset(ts, col=ts_select.value)
    detrended_data = remove_trend(ts_initial, poly_select.value)
    combine = [ts_initial, detrended_data]
    combined_df = pd.concat(combine)
    source_p1 = ColumnDataSource(data=combined_df)
    plot1 = make_decompplot(source_p1)

    # Preparing initial data for differencing.
    deseason_data = remove_seasonality(detrended_data[['time', 'detrended_data']], season_select.value)
    combine3 = [ts_initial, deseason_data]
    combined_df3 = pd.concat(combine3)
    source_p2 = ColumnDataSource(data=combined_df3)
    plot2 = make_seasonplot(source_p2)

    # Set up layouts and add to document
    # Put controls in a single element.
    controls = WidgetBox(ts_select, div1, xaxis, yaxis, div2, text1, poly_select, div3, text2, season_select)

    # Create a row layout
    gridplot = column(plot1, plot2)
    formatting = row(controls, gridplot)

    # Make a tab with the layout.
    tab = Panel(child=formatting, title='Decomposition and Seasonality')
    return tab
