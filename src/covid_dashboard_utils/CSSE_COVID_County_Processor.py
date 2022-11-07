# Load county level COVID data from Github and county population data into DataFrames
# Perform 7 day average cases / 100k for full dataset

import pandas as pd
import numpy as np
import logging as log
import dashboard_utils as utils

csse_us_county_cases_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv';

county_pop_url = 'https://raw.githubusercontent.com/balsama/us_counties_data/main/data/counties.csv'

csse_current_county_values = dict()
csse_counties_norm_cases_df = pd.DataFrame()
csse_full_counties_norm_cases_df = pd.DataFrame()
csse_series_list = list() # global list of extracted county time series

def __init__(self):

    log.info("Loading CSSE County CSV data...")

    try:
        csse_county_df = pd.read_csv(csse_us_county_cases_URL, parse_dates=True)
    except:
        log.error("ERROR: Can't load CSSE data")
    
    print(csse_county_df.shape)
    log.debug(csse_county_df.dtypes)
    log.debug(csse_county_df.head)

    log.info("this is log.info")
    log.info("Loading US population data...")
    try:
        county_pop_df = pd.read_csv(county_pop_url, parse_dates=True) #, usecols=['FIPS Code', 'Population'])
    except:
        print("ERROR: Can't load Population data")

    log.debug(county_pop_df.shape)
    log.debug(county_pop_df.dtypes)
    log.debug(county_pop_df.head)

    csse_full_counties_norm_cases_df = utils.merge_and_calculate_full_new_cases(csse_county_df, county_pop_df)

def get_county_list() -> list:
    return csse_full_counties_norm_cases_df['Combined_Key'].unique().tolist()