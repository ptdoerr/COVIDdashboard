# Load county level COVID data from Github and county population data into DataFrames
# Perform 7 day average cases / 100k for full dataset

import pandas as pd
import numpy as np
import logging as log
from . import dashboard_utils as utils

class CountyDataProcessor:

    csse_us_county_cases_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv';

    county_pop_url = 'https://raw.githubusercontent.com/balsama/us_counties_data/main/data/counties.csv'

    def __init__(self) -> None:
        self.csse_current_county_values = dict()
        self.csse_counties_norm_cases_df = pd.DataFrame()
        self.csse_full_counties_norm_cases_df = pd.DataFrame()
        self.csse_series_list = list() # global list of extracted county time series

        log.info("Loading CSSE County CSV data...")

        try:
            self.csse_county_df = pd.read_csv(CountyDataProcessor.csse_us_county_cases_URL, parse_dates=True)
        except:
            log.error("ERROR: Can't load CSSE data")
    
        log.info(self.csse_county_df.shape)
        log.debug(self.csse_county_df.dtypes)
        log.debug(self.csse_county_df.head)

        log.info("this is log.info")
        log.info("Loading US population data...")

        try:
            self.county_pop_df = pd.read_csv(
                CountyDataProcessor.county_pop_url, parse_dates=True) #, usecols=['FIPS Code', 'Population'])
        except:
            log.error("ERROR: Can't load Population data")

        log.debug(self.county_pop_df.shape)
        log.debug(self.county_pop_df.dtypes)
        log.debug(self.county_pop_df.head)

        self.csse_full_counties_norm_cases_df = utils.merge_and_calculate_full_new_cases(
            self.csse_county_df, self.county_pop_df)

    def get_county_list() -> list:
        county_list = self.csse_full_counties_norm_cases_df['Combined_Key'].unique().tolist()
        return county_list