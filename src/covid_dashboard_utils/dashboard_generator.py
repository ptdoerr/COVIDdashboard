import os
import sys
import time
from datetime import datetime, timedelta
import logging as log
from pathlib import Path
import io
import base64
import importlib
import math

import dashboard_utils as utils
from . import CSSE_COVID_County_Processor
from . import COVID_Plot_Generator

county_processor = CSSE_COVID_County_Processor()

csse_plot_days = 400

full_county_df = county_processor.csse_full_counties_norm_cases_df

selected_counties = ['Douglas, Nebraska, US', 'Sarpy, Nebraska, US', 'Lancaster, Nebraska, US']

extracted_counties_norm_cases_df = utils.extract_plot_counties(full_county_df, selected_counties, csse_plot_days)

plot_generator = COVID_Plot_Generator()

plot_generator.plot_current_case_values(extracted_counties_norm_cases_df)

plot_generator.plot_time_series(extracted_counties_norm_cases_df)