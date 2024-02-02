import numpy as np
import scipy
import polars as pl


def outlier_iqr(arr: np.ndarray, factor: float) -> float:  # tuple[float, float]:
    q1 = np.quantile(arr, 0.25)
    q3 = np.quantile(arr, 0.75)
    iqr = q3 - q1  # scipy.stats.iqr(x=arr)

    if iqr > 0:
        return (arr > np.ceil(q3 + factor * iqr)) | (arr < np.floor(q1 - factor * iqr))  # , iqr
    else:
        return np.repeat(False, arr.shape[0])


def outlier_sd(arr: np.ndarray, factor: float) -> float:  # tuple[float, float]:
    mean = np.mean(arr)
    sd = np.std(arr)
    # breakpoint()
    if sd > 0:
        return (arr > np.ceil(mean + factor * sd)) | (arr < np.floor(mean - factor * sd))  # , sd
    else:
        return np.repeat(False, arr.shape[0])


def outlier_ttt(arr: np.ndarray, q: float) -> float:  # tuple[float, float]:
    arr_std = np.std(arr)
    if arr_std > 0:
        t_obs = np.abs(arr - np.mean(arr)) / arr_std
        t_alpha = scipy.stats.t.ppf(q=q, df=arr.shape[0] - 2)
        tau = t_alpha * (arr.shape[0] - 1) / np.sqrt(arr.shape[0] * (arr.shape[0] - 2 + t_alpha**2))
        return t_obs > tau  # , t_obs
    else:
        return np.repeat(False, arr.shape[0])


def outliers_df(df: pl.DataFrame, indicators: list, factor: dict, indicator_type: str = "count") -> tuple:
    cols = indicators.copy()
    cols.append("hf_id")
    # regions = epi_ind.select("region").unique().to_series().sort().to_list()
    df2 = df.filter(pl.col("type") == indicator_type).select(cols)
    hf_list = df2.select("hf_id").unique().to_series()
    nb_cols = len(df2.columns) - 1
    hf_ids = np.repeat(hf_list, repeats=nb_cols)
    ind_names = np.array([])
    cols.remove("hf_id")

    arr_iqr = np.array([])
    arr_sd = np.array([])
    arr_ttt = np.array([])

    for hf in hf_list:
        df_hf = df2.filter(pl.col("hf_id") == hf).drop("hf_id")
        ind_names = np.append(ind_names, cols)
        for col in df_hf.columns:
            arr = df_hf[col].to_numpy()
            arr2 = arr[~np.isnan(arr)]
            if len(arr2) < 13:
                arr_iqr = np.append(arr_iqr, np.nan)
                arr_sd = np.append(arr_sd, np.nan)
                arr_ttt = np.append(arr_ttt, np.nan)
                continue
            # breakpoint()
            arr_iqr = np.append(arr_iqr, outlier_iqr(arr2, factor=factor["iqr"]).sum())
            arr_sd = np.append(arr_sd, outlier_sd(arr2, factor=factor["sd"]).sum())
            arr_ttt = np.append(
                arr_ttt,
                outlier_ttt(
                    arr2,
                    q=factor["ttt"],
                ).sum(),
            )

    df_hfs = (
        pl.DataFrame({"hf_id": hf_ids, "indicator": ind_names, "iqr": arr_iqr, "sd": arr_sd, "ttt": arr_ttt})
        .filter(pl.col("iqr").is_not_nan() & pl.col("sd").is_not_nan() | pl.col("ttt").is_not_nan())
        .filter((pl.col("iqr") > 0) | (pl.col("sd") > 0) | (pl.col("ttt") > 0))
    )
    return df_hfs


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
