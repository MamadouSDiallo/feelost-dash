import numpy as np
import scipy


def outlier_iqr(arr: np.ndarray, factor: float) -> float:
    iqr = scipy.stats.iqr(x=arr)

    return arr > factor * iqr


def outlier_sd(arr: np.ndarray, factor: float) -> float:
    sd = np.sqrt(scipy.stats.describe(a=arr).variance)
    # breakpoint()
    return arr > factor * sd


def outlier_ttt(arr: np.ndarray, factor: float, q: float) -> float:
    t_obs = np.abs(arr - np.mean(arr)) / np.sqrt(scipy.stats.describe(a=arr).variance)
    return t_obs > scipy.stats.t.ppf(q=q, df=arr.shape[0] - 1)


# Testing the outliers' functions above

x = np.array([1, 2, 13, 4, 51, 3, 2, 5, 7, 6, 1, 9])


def test_outlier_iqr():
    outliers = outlier_iqr(arr=x, factor=1.5)
    # breakpoint()
    assert (outliers == (False, False, True, False, True, False, False, False, False, False, False, True)).all()


def test_outlier_sd():
    outliers = outlier_sd(arr=x, factor=2)
    assert (outliers == (False, False, False, False, True, False, False, False, False, False, False, False)).all()


def test_outlier_ttt():
    outliers = outlier_ttt(arr=x, factor=2, q=0.95)
    assert (outliers == (False, False, False, False, True, False, False, False, False, False, False, False)).all()
