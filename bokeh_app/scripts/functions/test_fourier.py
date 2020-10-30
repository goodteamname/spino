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
            [[1, 2, 3], [4, 5, 6]],
            (0, 0),
            ValueError
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
    import fourier_functions
    if raises:
        with pytest.raises(raises):
            npt.assert_equal(fourier_functions.fourier_to_coefficients(test)[1].shape, expectedShape)
    else:
        npt.assert_equal(fourier_functions.fourier_to_coefficients(test)[1].shape, expectedShape)


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
            [[1, 2, 3], [4, 5, 6]],
            (0, 3),
            ValueError
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
def test_dfs(test, expectedShape, raises):
    """Test normalisation works for arrays of one and positive integers."""
    import fourier_functions
    if raises:
        with pytest.raises(raises):
            npt.assert_equal(fourier_functions.dfs(test)[1].shape, expectedShape)
    else:
        npt.assert_equal(fourier_functions.dfs(test)[1].shape, expectedShape)



@pytest.mark.parametrize(

    "test_data, test_times, expectedShape, raises",
    [
        (
            [1, 2, 3],
            [1, 2, 3],
            (3, 2),
            None
        ),
        (
            [1, 2, 3, 4, 5, 6, 7],
            [1, 2, 3, 4, 5, 6, 7],
            (7, 2),
            None
        ),
        (
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            (5, 2),
            None
        ),
        (
            [[1, 2, 3], [4, 5, 6]],
            [1, 2, 3, 4, 5, 6],
            (3, 2),
            ValueError
        ),
        (
            [1],
            [1, 2, 3, 4, 5, 6],
            (1, 2),
            ValueError
        ),
        (
            [],
            [1, 2, 3, 4, 5, 6],
            (1, 0),
            ValueError
        ),
    ])
def test_freq(test_data, test_times, expectedShape, raises):
    """Test normalisation works for arrays of one and positive integers."""
    import fourier_functions
    if raises:
        with pytest.raises(raises):
            npt.assert_equal(fourier_functions.fourier_to_freq_spectrum(test_data, test_times).shape, expectedShape)
    else:
        npt.assert_equal(fourier_functions.fourier_to_freq_spectrum(test_data, test_times).shape, expectedShape)



@pytest.mark.parametrize(

    "test_data, expectedShape, raises",
    [
        (
            [1, 2, 3],
            (3,),
            None
        ),
        (
            [1, 2, 3, 4, 5, 6, 7],
            (7,),
            None
        ),
        (
            [1, 2, 3, 4, 5, 6],
            (6,),
            None
        ),
        (
            [[1, 2, 3], [4, 5, 6]],
            (0,),
            ValueError
        ),
        (
            [1],
            (0,),
            ValueError
        ),
        (
            [],
            (0,),
            ValueError
        ),
    ])
def test_fourier_approx(test_data, expectedShape, raises):
    """Test normalisation works for arrays of one and positive integers."""
    import fourier_functions
    if raises:
        with pytest.raises(raises):
            alpha0, table = fourier_functions.fourier_to_coefficients(test_data)
            npt.assert_equal(fourier_functions.fourier_approx(alpha0, table, test_data).shape, expectedShape)
    else:
        alpha0, table = fourier_functions.fourier_to_coefficients(test_data)
        npt.assert_equal(fourier_functions.fourier_approx(alpha0, table, test_data).shape, expectedShape)
