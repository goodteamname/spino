import pytest
import pandas as pd

ts = pd.read_csv(
  "data/test_timeseries_copy.csv",
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
