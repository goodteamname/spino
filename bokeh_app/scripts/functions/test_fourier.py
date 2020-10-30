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
            (3, ),
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
            # alpha0, table = fourier_functions.fourier_to_coefficients(test_data)
            npt.assert_equal(
                fourier_functions.fourier_approx(
                    fourier_functions.fourier_to_coefficients(test_data)[0],
                    fourier_functions.fourier_to_coefficients(test_data)[1],
                    test_data).shape,
                expectedShape)
    else:
        alpha0, table = fourier_functions.fourier_to_coefficients(test_data)
        npt.assert_equal(fourier_functions.fourier_approx(alpha0, table, test_data).shape, expectedShape)


@pytest.mark.parametrize(

    "test_data, test_times, components, expectedShape0, expectedShape1, expectedShape2, raises",
    [
        (
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            2,
            (5, 3),
            (2, 3),
            (5, 4),
            None
        ),
        (
            [1, 2, 3, 4, 5, 6, 7],
            [1, 2, 3, 4, 5, 6, 7],
            2,
            (7, 3),
            (2, 3),
            (7, 4),
            None
        ),
        (
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            2,
            (6, 3),
            (2, 3),
            (6, 4),
            None
        ),
        (
            [[1, 2, 3], [4, 5, 6]],
            [1, 2, 3, 4, 5, 6],
            2,
            (5, 3),
            (3, 2),
            (5, 4),
            ValueError
        ),
        (
            [1],
            [1, 2, 3, 4, 5, 6],
            2,
            (1, 3),
            (2, 3),
            (1, 4),
            ValueError
        ),
        (
            [],
            [1, 2, 3, 4, 5, 6],
            2,
            (0, 3),
            (2, 3),
            (0, 4),
            ValueError
        ),
    ])
def test_calc_residuals(test_data, test_times, components, expectedShape0, expectedShape1, expectedShape2, raises):
    """Test normalisation works for arrays of one and positive integers."""
    import fourier_functions
    if raises:
        with pytest.raises(raises):
            alpha0, df = fourier_functions.fourier_to_coefficients(test_data)
            print(alpha0)
            print(df)
            npt.assert_equal(
                fourier_functions.calc_residuals(alpha0, df, test_data, test_times, components)[0].shape,
                expectedShape0
                )
            npt.assert_equal(
                fourier_functions.calc_residuals(alpha0, df, test_data, test_times, components)[1].shape,
                expectedShape1
                )
            npt.assert_equal(
                fourier_functions.calc_residuals(alpha0, df, test_data, test_times, components)[2].shape,
                expectedShape2
                )
    else:
        alpha0, df = fourier_functions.fourier_to_coefficients(test_data)
        print(alpha0)
        print(df)
        npt.assert_equal(
            fourier_functions.calc_residuals(alpha0, df, test_data, test_times, components)[0].shape,
            expectedShape0
            )
        npt.assert_equal(
            fourier_functions.calc_residuals(alpha0, df, test_data, test_times, components)[1].shape,
            expectedShape1
            )
        npt.assert_equal(
            fourier_functions.calc_residuals(alpha0, df, test_data, test_times, components)[2].shape,
            expectedShape2
            )


@pytest.mark.parametrize(

    "test_data, test_times",
    [
        (
            [1, 2, 3, 4, 5, 7, 8, 3, 4, 5, 6, 4, 3, 4, 6, 7, 8, 9, 0, 64, 4],
            [0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        ),
    ])
def test_optimise_residuals(test_data, test_times):
    """Test normalisation works for arrays of one and positive integers."""
    import fourier_functions
    alpha0, df = fourier_functions.fourier_to_coefficients(test_data)
    components = fourier_functions.optimise_residuals(alpha0, df, test_data)
    print(alpha0)
    print(df)
    expectedShape0 = (len(test_data), components+1)
    expectedShape1 = (components, 3)
    expectedShape2 = (len(test_data), 4)
    npt.assert_equal(fourier_functions.calc_residuals(alpha0, df, test_data, test_times, components)[0].shape, expectedShape0)
    npt.assert_equal(fourier_functions.calc_residuals(alpha0, df, test_data, test_times, components)[1].shape, expectedShape1)
    npt.assert_equal(fourier_functions.calc_residuals(alpha0, df, test_data, test_times, components)[2].shape, expectedShape2)
