import pytest
import os
import pandas as pd

df = pd.read_csv(os.getcwd() + '/data/linear_trend_test_timeseries_noisy.csv')


@pytest.mark.parametrize(

    "data, expectedShape ",
    [
        (
            df,
            (df.shape[0], 3)
        )
    ])
def test_remove_trend(data, expectedShape):
    """Test normalisation works for arrays of one and positive integers."""
    from timeseries_stats import remove_trend
    assert(remove_trend(data, 1).shape == expectedShape)
