import pytest
import numpy.testing as npt


@pytest.mark.parametrize(

    "test, expectedShape, raises",
    [
        (
            [1, 2, 3],
            (1, 3),
            None
        ),
        (
            [1, 2, 3, 4, 5, 6, 7],
            (3, 3),
            None
        ),
        (
            [1, 2, 3, 4, 5, 6],
            (2, 3),
            None
        ),
        (
            [1],
            (0, 0),
            ValueError
        ),
        (
            [],
            (0, 0),
            ValueError
        ),
    ])
def test_dft(test, expectedShape, raises):
    """Test normalisation works for arrays of one and positive integers."""
    import dft
    if raises:
        with pytest.raises(raises):
            npt.assert_equal(dft.dft(test).shape, expectedShape)
            print(type(dft.dft(test)))
    else:
        npt.assert_equal(dft.dft(test).shape, expectedShape)
