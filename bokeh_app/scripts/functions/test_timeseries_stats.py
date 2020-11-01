import pytest
import pandas as pd

ts = pd.read_csv(
  "bokeh_app/data/test_timeseries.csv",
  skiprows=1,
  delimiter=",",
  names=['time', 'y1', 'y2', 'y3']
)


@pytest.mark.parametrize(

    "data, expectedShape ",
    [
        (
            ts,
            (ts.shape[0], 7)
        )
    ])
def test_remove_trend(data, expectedShape):
    """Test normalisation works for arrays of one and positive integers."""
    from timeseries_stats import remove_trend
    assert(remove_trend(data, 1).shape == expectedShape)


@pytest.mark.parametrize(

    "data, expectedShape ",
    [
        (
            ts,
            (ts.shape[0]-1, ts.shape[1])
        )
    ])
def test_remove_seasonality(data, expectedShape):
    """Test normalisation works for arrays of one and positive integers."""
    from timeseries_stats import remove_seasonality
    assert(remove_seasonality(data, ts.time[1]).shape == expectedShape)


@pytest.mark.parametrize(

    "data, expectedShape ",
    [
        (
            ts,
            ts.shape
        )
    ])
def test_rolling_std(data, expectedShape):
    """Test normalisation works for arrays of one and positive integers."""
    from timeseries_stats import rolling_std
    assert(rolling_std(data, 2).shape == expectedShape)


@pytest.mark.parametrize(

    "data, expectedShape ",
    [
        (
            ts,
            ts.shape
        )
    ])
def test_rolling_mean(data, expectedShape):
    """Test normalisation works for arrays of one and positive integers."""
    from timeseries_stats import rolling_mean
    assert(rolling_mean(data, 2).shape == expectedShape)


@pytest.mark.parametrize(

    "data, expectedShape ",
    [
        (
            ts.y1,
            (5, 2)
        )
    ])
def test_auto_corr(data, expectedShape):
    """Test normalisation works for arrays of one and positive integers."""
    from timeseries_stats import auto_corr
    assert(auto_corr(data, 5).shape == expectedShape)


@pytest.mark.parametrize(

    "data1, data2, expectedShape ",
    [
        (
            ts.y1,
            ts.y2,
            (5, 2)
        )
    ])
def test_corr(data1, data2, expectedShape):
    """Test normalisation works for arrays of one and positive integers."""
    from timeseries_stats import corr
    assert(corr(data1, data2, 5).shape == expectedShape)
