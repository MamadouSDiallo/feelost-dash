import polars as pl

# Population data 
denom_data = pl.read_csv("./data/raw/Population data from 2011 to 2016 EFY by WrHO_ZHD_RHB.csv") 

denom_data.columns = [x.lower() for x in denom_data.columns]
denom_data.columns = [" ".join(x.split()) for x in denom_data.columns]
denom_data.columns = [x.replace(" - ", "_") for x in denom_data.columns]
denom_data.columns = [x.replace(" ", "_") for x in denom_data.columns]
denom_data.columns = [x.replace("-", "_") for x in denom_data.columns]

breakpoint()


# Health facility list
hf_list = (
    pl.read_csv("./data/raw/Health Facilities_Amhara_Lastest.csv")
    .select(["ID", "Health Facility name", "Facility Type", "Ownership", "level", "Region", "Zone", "Woreda", "PHCU"])
    .rename({"ID": "hf_id", "Health Facility name": "hf_name", "Facility Type": "hf_type", "Ownership": "ownership"})
)

hf_list.columns = [x.lower() for x in hf_list.columns]


hf_list.write_csv(file="./data/clean/hf_list_amhara_region.csv")

# EPI data
epi_data = pl.read_csv("./data/raw/EPI data_Amhara by HFs.csv")

epi_data.columns = [x.lower() for x in epi_data.columns]
epi_data.columns = [" ".join(x.split()) for x in epi_data.columns]
epi_data.columns = [x.replace(" ", "_") for x in epi_data.columns]

epi_data2 = epi_data.select(
    [
        "organisationunitid",
        "organisationunitcode",
        "periodid",
        "periodcode",
        "epi_bcg_doses_given_(all_ages)",
        "epi_children_under_one_year_of_age_who_have_received_inactivated_polio_vaccine",
        "epi_ipv_doses_given",
        "epi_children_under_one_year_of_age_who_have_received_first_dose_of_measles_vaccine",
        "epi_measles_doses_given_(all_ages)",
        "epi_children_under_one_year_of_age_who_have_received_first_dose_of_pentavalent_vaccine",
        "epi_children_under_one_year_of_age_who_have_received_third_dose_of_pentavalent_vaccine",
        "epi_pentavalent_(dpt-hepb-hib)_doses_given_(all_ages)",
        "epi_children_under_one_year_of_age_who_have_received_2nd_dose_of_rotavirus_vaccine",
        "epi_children_received_all_vaccine_doses_before_1st_birthday",
    ]
).rename(
    {
        "organisationunitid": "hf_id",
        "organisationunitcode": "hf_code",
        "periodid": "period_id",
        "periodcode": "period_code",
        "epi_bcg_doses_given_(all_ages)": "bcg_all_ages",
        "epi_children_under_one_year_of_age_who_have_received_inactivated_polio_vaccine": "ipv_one_year",
        "epi_ipv_doses_given": "ipv_given",
        "epi_children_under_one_year_of_age_who_have_received_first_dose_of_measles_vaccine": "mcv1_one_year",
        "epi_measles_doses_given_(all_ages)": "mcv_all_ages",
        "epi_children_under_one_year_of_age_who_have_received_first_dose_of_pentavalent_vaccine": "penta1_one_year",
        "epi_children_under_one_year_of_age_who_have_received_third_dose_of_pentavalent_vaccine": "penta3_one_year",
        "epi_pentavalent_(dpt-hepb-hib)_doses_given_(all_ages)": "penta_doses_given_all_ages",
        "epi_children_under_one_year_of_age_who_have_received_2nd_dose_of_rotavirus_vaccine": "rota2_one_year",
        "epi_children_received_all_vaccine_doses_before_1st_birthday": "full_vacc_one_year",
    }
)

epi_data.write_csv(file="./data/clean/epi_data.csv")
