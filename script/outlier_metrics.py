import numpy as np
import scipy
import polars as pl


def outlier_iqr(arr: np.ndarray, factor: float) -> float:  # tuple[float, float]:
    arr2 = arr[~np.isnan(arr)]
    q1 = np.quantile(arr2, 0.25)
    q3 = np.quantile(arr2, 0.75)
    iqr = q3 - q1  # scipy.stats.iqr(x=arr)

    if iqr > 0:
        return (arr > np.ceil(q3 + factor * iqr)) | (arr < np.floor(q1 - factor * iqr))  # , iqr
    else:
        return np.repeat(False, arr.shape[0])


def outlier_zscores(arr: np.ndarray, factor: float) -> float:  # tuple[float, float]:
    arr2 = arr[~np.isnan(arr)]
    mean = np.mean(arr2)
    sd = np.std(arr2)
    if sd > 0:
        return np.abs(arr - mean) / sd > factor  # , sd
    else:
        return np.repeat(False, arr.shape[0])


def outlier_ttt(arr: np.ndarray, q: float) -> float:  # tuple[float, float]:
    arr2 = arr[~np.isnan(arr)]
    arr_std = np.std(arr2)
    if arr_std > 0:
        t_obs = np.abs(arr - np.mean(arr2)) / arr_std
        t_alpha = scipy.stats.t.ppf(q=q, df=arr2.shape[0] - 2)
        tau = t_alpha * (arr2.shape[0] - 1) / np.sqrt(arr2.shape[0] * (arr2.shape[0] - 2 + t_alpha**2))
        return t_obs > tau  # , t_obs
    else:
        return np.repeat(False, arr.shape[0])


def outliers_df(df: pl.DataFrame, indicators: list, factor: dict, indicator_type: str = "count") -> tuple:
    cols = indicators.copy()
    nb_cols = len(cols)
    df2 = df.filter(pl.col("type") == indicator_type).sort(by="hf_id")  # .select(cols + ["hf_id", "hf_name"])
    hf_ids = df2.select(["hf_id"]).unique().to_series()
    for i, hf in enumerate(hf_ids):
        df_hf = df2.filter(pl.col("hf_id") == hf)
        years = np.array([])
        months = np.array([])
        arr_iqr = np.array([])
        arr_sd = np.array([])
        arr_ttt = np.array([])
        for col in cols:
            arr = df_hf[col].to_numpy()
            # arr2 = arr[~np.isnan(arr)]
            if len(arr[~np.isnan(arr)]) < 13:
                arr_iqr = np.append(arr_iqr, np.repeat(np.nan, arr.shape[0]))
                arr_sd = np.append(arr_sd, np.repeat(np.nan, arr.shape[0]))
                arr_ttt = np.append(arr_ttt, np.repeat(np.nan, arr.shape[0]))
                years = np.append(years, df_hf["year"].to_numpy())
                months = np.append(months, df_hf["month"].to_numpy())
                continue
            arr_iqr = np.append(arr_iqr, outlier_iqr(arr, factor=factor["iqr"]))
            arr_sd = np.append(arr_sd, outlier_zscores(arr, factor=factor["sd"]))
            arr_ttt = np.append(
                arr_ttt,
                outlier_ttt(
                    arr,
                    q=factor["ttt"],
                ),
            )
            years = np.append(years, df_hf["year"].to_numpy())
            months = np.append(months, df_hf["month"].to_numpy())

        if i == 0:
            df_hfs = pl.DataFrame(
                {
                    "hf_id": np.repeat(df_hf["hf_id"], nb_cols),
                    "hf_name": np.repeat(df_hf["hf_name"], nb_cols),
                    "indicator": np.repeat(cols, df_hf.shape[0]),
                    "years": years,
                    "months": months,
                    "iqr": arr_iqr,
                    "sd": arr_sd,
                    "ttt": arr_ttt,
                }
            )
        else:
            df_hfs = df_hfs.vstack(
                pl.DataFrame(
                    {
                        "hf_id": np.repeat(df_hf["hf_id"], nb_cols),
                        "hf_name": np.repeat(df_hf["hf_name"], nb_cols),
                        "indicator": np.repeat(cols, df_hf.shape[0]),
                        "years": years,
                        "months": months,
                        "iqr": arr_iqr,
                        "sd": arr_sd,
                        "ttt": arr_ttt,
                    }
                )
            )

    return df_hfs


def outliers_aggr(df):
    return (
        df.group_by(by=["hf_id", "hf_name", "indicator"])
        .agg(
            pl.col("iqr").filter(pl.col("iqr").is_not_nan()).sum().alias("iqr"),
            pl.col("sd").filter(pl.col("sd").is_not_nan()).sum().alias("sd"),
            pl.col("ttt").filter(pl.col("ttt").is_not_nan()).sum().alias("ttt"),
        )
        .filter((pl.col("iqr") > 0) | (pl.col("sd") > 0) | (pl.col("ttt") > 0))
    )


# Testing the outliers' functions above

x = np.array([1, 2, 13, 4, 51, 3, 2, 5, 7, 6, 1, 9])


def test_outlier_iqr():
    outliers = outlier_iqr(arr=x, factor=1.5)
    # breakpoint()
    assert (outliers == (False, False, True, False, True, False, False, False, False, False, False, True)).all()


def test_outlier_zscores():
    outliers = outlier_zscores(arr=x, factor=2)
    assert (outliers == (False, False, False, False, True, False, False, False, False, False, False, False)).all()


def test_outlier_ttt():
    outliers = outlier_ttt(arr=x, factor=2, q=0.95)
    assert (outliers == (False, False, False, False, True, False, False, False, False, False, False, False)).all()
