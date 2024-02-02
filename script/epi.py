import polars as pl

from outlier_metrics import outliers_df

# Health facility list datasets
hf_list_df = pl.read_csv("./data/clean/hf_list_amhara_region.csv")

hf_list_df.write_csv("./data/input/hf_list_df.csv")

# EPI datasets
epi_df = (
    pl.read_csv("./data/clean/epi_data.csv")
    .drop(["hf_code", "period_id"])
    .with_columns(
        pl.col("period_code").cast(pl.Utf8).str.slice(0, 4).cast(pl.Int32).alias("year"),
        pl.col("period_code").cast(pl.Utf8).str.slice(4, 6).cast(pl.Int32).alias("month_code"),
    )
    .drop(["period_code"])
    .with_columns(
        pl.when(pl.col("month_code") == 1)
        .then(pl.lit("January"))
        .when(pl.col("month_code") == 2)
        .then(pl.lit("February"))
        .when(pl.col("month_code") == 3)
        .then(pl.lit("March"))
        .when(pl.col("month_code") == 4)
        .then(pl.lit("April"))
        .when(pl.col("month_code") == 5)
        .then(pl.lit("May"))
        .when(pl.col("month_code") == 6)
        .then(pl.lit("June"))
        .when(pl.col("month_code") == 7)
        .then(pl.lit("July"))
        .when(pl.col("month_code") == 8)
        .then(pl.lit("August"))
        .when(pl.col("month_code") == 9)
        .then(pl.lit("September"))
        .when(pl.col("month_code") == 10)
        .then(pl.lit("October"))
        .when(pl.col("month_code") == 11)
        .then(pl.lit("November"))
        .when(pl.col("month_code") == 12)
        .then(pl.lit("December"))
        .otherwise(pl.lit(""))
        .alias("month")
    )
    .with_columns(
        pl.when(pl.col("month_code").is_null())
        .then(pl.lit(""))
        .when(pl.col("month_code") > 9)
        .then(pl.col("month_code").cast(pl.Utf8))
        .when(pl.col("month_code") < 10)
        .then("0" + pl.col("month_code").cast(pl.Utf8))
        .alias("month_code")
    )
)

epi_df = (
    epi_df.drop("hf_id")
    .insert_column(index=0, column=epi_df.get_column("hf_id"))
    .drop("year")
    .insert_column(index=1, column=epi_df.get_column("year"))
    .drop("month")
    .insert_column(index=2, column=epi_df.get_column("month"))
)

epi_df = hf_list_df.select("hf_id", "hf_name").join(epi_df, on="hf_id")

epi_df.write_csv("./data/input/epi_df.csv")


# Simulated denominator data

epi_denom = (
    epi_df.select(["hf_id", "year", "month", "month_code", "bcg_all_ages", "ipv_given", "penta1_one_year"])
    .with_columns(
        pl.when(pl.col("bcg_all_ages").is_not_null())
        .then("bcg_all_ages")
        .when(pl.col("ipv_given").is_not_null())
        .then("ipv_given")
        .when(pl.col("penta1_one_year").is_not_null())
        .then("penta1_one_year")
        .alias("nb_infants")
    )
    .drop(["bcg_all_ages", "ipv_given", "penta1_one_year"])
)


# EPI indicators

epi_ind_count = (
    epi_denom.join(
        epi_df.select(
            [
                "hf_id",
                "hf_name",
                "year",
                "month",
                "month_code",
                "bcg_all_ages",
                "ipv_one_year",
                "penta1_one_year",
                "penta3_one_year",
                "penta_doses_given_all_ages",
                "mcv1_one_year",
                "mcv_all_ages",
                "rota2_one_year",
                "full_vacc_one_year",
            ]
        ),
        on=["hf_id", "year", "month"],
    )
    .rename(
        {
            "bcg_all_ages": "bcg",
            "ipv_one_year": "ipv",
            "penta1_one_year": "penta1",
            "penta3_one_year": "penta3",
            "penta_doses_given_all_ages": "penta_all_ages",
            "mcv1_one_year": "mcv1",
            "mcv_all_ages": "mcv_all_ages",
            "rota2_one_year": "rota2",
            "full_vacc_one_year": "full_vacc",
        }
    )
    .with_columns(pl.lit("count").alias("type"), dropout=None)
)

epi_ind_prop = epi_ind_count.with_columns(
    (100 * pl.col("bcg") / pl.col("nb_infants")).alias("bcg"),
    (100 * pl.col("ipv") / pl.col("nb_infants")).alias("ipv"),
    (100 * pl.col("penta1") / pl.col("nb_infants")).alias("penta1"),
    (100 * pl.col("penta3") / pl.col("nb_infants")).alias("penta3"),
    (100 * pl.col("mcv1") / pl.col("nb_infants")).alias("mcv1"),
    (100 * pl.col("full_vacc") / pl.col("nb_infants")).alias("full_vacc"),
    (100 * pl.col("rota2") / pl.col("nb_infants")).alias("rota2"),
).with_columns((pl.col("penta3") - pl.col("penta1")).alias("dropout"), pl.lit("proportion").alias("type"))

epi_ind = (
    pl.concat([epi_ind_count, epi_ind_prop], how="vertical_relaxed")
    .with_columns(
        period=pl.col("year").cast(pl.Utf8) + "-" + pl.col("month_code").cast(pl.Utf8),
        bcg_diff1=pl.col("bcg").diff(),
        ipv_diff1=pl.col("ipv").diff(),
        penta1_diff1=pl.col("penta1").diff(),
        penta3_diff1=pl.col("penta3").diff(),
        mcv1_diff1=pl.col("mcv1").diff(),
        rota2_diff1=pl.col("rota2").diff(),
        full_vacc_diff1=pl.col("full_vacc").diff(),
    )
    .with_columns(
        previous_period=pl.col("period").shift(),
        bcg_previous=pl.col("bcg").shift(),
        ipv_previous=pl.col("ipv").shift(),
        penta1_previous=pl.col("penta1").shift(),
        penta3_previous=pl.col("penta3").shift(),
        mcv1_previous=pl.col("mcv1").shift(),
        rota2_previous=pl.col("rota2").shift(),
        full_vacc_previous=pl.col("full_vacc").shift(),
    )
)

epi_ind.write_csv("./data/input/epi_ind.csv")

indicators = ["bcg", "ipv", "penta1", "penta3", "mcv1", "rota2", "full_vacc"]
factors = {"iqr": 1.5, "sd": 2, "ttt": 95}
epi_outliers = outliers_df(df=epi_ind, indicators=indicators, factor=factors)
# breakpoint()
epi_outliers.write_csv("./data/input/epi_outliers.csv")
