import numpy as np
import scipy
import polars as pl


def outlier_iqr(arr: np.ndarray, factor: float) -> float:
    iqr = scipy.stats.iqr(x=arr)

    return arr > factor * iqr


def outlier_sd(arr: np.ndarray, factor: float) -> float:
    sd = np.sqrt(scipy.stats.describe(a=arr).variance)
    # breakpoint()
    return arr > factor * sd


def outlier_ttt(arr: np.ndarray, q: float) -> float:
    t_obs = np.abs(arr - np.mean(arr)) / np.sqrt(scipy.stats.describe(a=arr).variance)
    return t_obs > scipy.stats.t.ppf(q=q, df=arr.shape[0] - 1)


def outliers_df(df: pl.DataFrame, indicators: list, factor: dict) -> tuple:
    cols = indicators.copy()
    cols.append("hf_id")
    # regions = epi_ind.select("region").unique().to_series().sort().to_list()
    df2 = df.select(cols)
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
            # breakpoint()
            arr_iqr = np.append(arr_iqr, outlier_iqr(df_hf[col].to_numpy(), factor=factor["iqr"]).sum())
            arr_sd = np.append(arr_sd, outlier_sd(df_hf[col].to_numpy(), factor=factor["sd"]).sum())
            arr_ttt = np.append(
                arr_ttt,
                outlier_ttt(
                    df_hf[col].to_numpy(),
                    q=factor["ttt"],
                ).sum(),
            )

    df_hfs = pl.DataFrame({"hf_id": hf_ids, "indicator": ind_names, "iqr": arr_iqr, "sd": arr_sd, "ttt": arr_ttt})
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
