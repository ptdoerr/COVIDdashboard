import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
import os
import time
import us_state_codes as stcd

# print entire DataFrame or Series
def print_full(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')
    
    
def test_function1():
    print('in test_function')
    
# normalize value to local cases per 100k
def pop_normalize(value, pop):
    return value * 100000/pop
    
# normalize value to local cases per 100k
def pop_normalize_internal(row):
    #pop = 
    return value * 100000/pop

#@graphs_out.capture()
#Normalize county to population and calculate 7 day average / 100k
#Returns normalized Dataframe
def merge_and_calculate_full_new_cases(county_case_df, county_pop_df):
    start = time.time()
    global csse_full_counties_norm_cases_df
    
    # convert both FIPS columns to integer
    #print_full(county_pop_df) #["FIPS Code"])
    #print("county_pop_df[FIPS Code]:" +str(county_pop_df["FIPS Code"].astype(int)))
    #print("csse_county_df[FIPS]:" +str(csse_county_df["FIPS"].astype(int)))
    print("fixing pop FIPS Code format...")
    county_pop_df["FIPS Code"] = pd.to_numeric(county_pop_df["FIPS Code"], downcast='integer', errors='coerce')
    #print(county_pop_df.head)
    print("fixing case FIPS format...")
    county_case_df["FIPS"] = pd.to_numeric(county_case_df["FIPS"], downcast='integer', errors='coerce')
    #print(csse_county_df.head)
    
    print("Merging Case and Population data...")
    csse_w_pop_df = county_pop_df.merge(county_case_df, left_on='FIPS Code', right_on='FIPS').set_index('FIPS')
    print(csse_w_pop_df.columns)
    print(csse_w_pop_df.shape)
    #print(csse_w_pop_df.head)
    #print_full(csse_w_pop_df)
    #col_list = list(csse_w_pop_df)
    #print(col_list)
    
    row_list = list()
    
    print("Calculating normalized ave new cases...")
    for idx, row in csse_w_pop_df.iterrows():
        #print(idx, row['Population'], row['Combined_Key'])
        #print(row)
        county_pop = row['Population']
        county_new_cases_series = row.iloc[16:].diff().rolling(7).mean().apply(pop_normalize, args=(county_pop,))
        #print(type(county_new_cases_series))
        #print(county_new_cases_series)
        #insert county name
        county = row['Combined_Key']
        county_new_cases_series_w_name = pd.Series({'Combined_Key':row['Combined_Key']})
        element_list = [county_new_cases_series_w_name, county_new_cases_series]
        county_new_cases_series_w_name = pd.concat(element_list, axis=0)
        #print('county_new_cases_series_w_name', type(county_new_cases_series_w_name),county_new_cases_series_w_name.shape)
        #pd.concat(pd.Series([county_name]), county_new_cases_series)
        #set series name as fips id
        county_new_cases_series_w_name.name = row['FIPS Code']
        #print(county_new_cases_series)
        row_list.append(county_new_cases_series_w_name)#county_new_cases_series)
        #csse_full_counties_norm_cases_df.append(county_new_cases_series)
    
    transposed_df = pd.concat(row_list, axis=1)
    #print(transposed_df.head)
    norm_cases_df = transposed_df.transpose()
    print(norm_cases_df.shape)
    #print(csse_full_counties_norm_cases_df.head)
    end = time.time()
    print("merge_and_calculate_full_new_cases() completed:", end-start)
    
    return norm_cases_df

#extract rows to plot from full normalized data based on selected counties    
#@graphs_out.capture()    
def extract_plot_counties(normalized_df, counties_list, plot_days):
    print('in extract_plot_counties')
    #global csse_plot_days
    #global csse_full_counties_norm_cases_df
    #global csse_counties_norm_cases_df
    
    num_days_index = -plot_days
    
    #df.loc[df['column_name'].isin(some_values)]
    test_df = normalized_df.loc[
        normalized_df['Combined_Key'].isin(counties_list)]
    print('test_df' , test_df.shape, ' num_days_index: ', num_days_index)
    test_df.set_index('Combined_Key', inplace=True)
    test_df1 = test_df.iloc[:, num_days_index:]
    out_df = test_df1.transpose()
    
    new_columns = []
    columns = out_df.columns
    
    for col in columns:
        terms = col.split(', ')
        st_code = stcd.us_state_to_abbrev[terms[1]]
        new_name = terms[0] +', ' +st_code
        print(new_name)
        new_columns.append(new_name)
        
    out_df.columns = new_columns #rename(columns=new_columns, inplace=True)
        

    print('out_df:', out_df.shape)
    return(out_df)


    #print(csse_counties_norm_cases_df)
    #current_values = csse_counties_norm_cases_df.iloc[-1, :]
    #print('current Values: ', type(current_values), current_values) 
    
    

# set graph background colors based on cases range
def set_graph_background_color_bands(graph_axes, max_value, color_list):
    print("in set_graph_background_color_bands() max_value = " +str(max_value))
    graph_axes.axhspan(0, 2, facecolor=color_list[0], alpha=0.3)
    graph_axes.axhspan(2, 10, facecolor=color_list[1], alpha=0.3)
    graph_axes.axhspan(10, 25, facecolor=color_list[2], alpha=0.3)

    if(max_value > 150):
        graph_axes.axhspan(25, 75, facecolor=color_list[3], alpha=0.3)
        graph_axes.axhspan(75, 150, facecolor=color_list[4], alpha=0.3)
        graph_axes.axhspan(150, float(max_value)+5, facecolor=color_list[5], alpha=0.3)
    elif(max_value > 75):
        graph_axes.axhspan(25, 75, facecolor=color_list[3], alpha=0.3)
        graph_axes.axhspan(75, float(max_value)+5, facecolor=color_list[4], alpha=0.3)
    else:
        graph_axes.axhspan(25, float(max_value)+5, facecolor=color_list[3], alpha=0.3)
     
        
# currently not used
def calculate_full_rolling_averages_with_fips_index():
    print('in calculate_full_rolling_averages_with_fips_index()')
    global csse_county_df
    global county_pop_df
    
    # CSSE id:      'FIPS' col 4
    # pop id:       'FIPS Code' col 2
    # county polys: 'GEO_ID' col 1
    
    csse_full_county_list = csse_county_df['FIPS'].unique()
    
    for county_fips in csse_full_county_list:
    
        county_pop = county_pop_df.loc[county_pop_df['FIPS Code'] == county_fips].iat[0,3]
        
        county_counts_only_df = csse_county_df.loc[csse_county_df['fips'] == county_fips].iloc[0, 11:]
        
        print(county_fips +' pop: ' +str(county_pop))
    
        #county_norm_series = county_counts_only_df.diff().rolling(7).mean().apply(pop_normalize, args=(county_pop,))
        
# gets time series and latest value data from county DataFrame for a list of counties
# latest values are put in global current_county_values
# time series data is put in global counties_norm_cases
# 
#deprecated 2/16/21 now using merge_and_calculate_full_new_cases() and extract_plot_counties()
#@graphs_out.capture()
#def get_latest_csse_county_values(counties_list):
#    print("in get_latest_csse_county_values()")
#    #current_county_values
#    global csse_current_county_values
#   #current_county_values.clear()
#    global csse_counties_norm_cases_df
#    global csse_full_counties_norm_cases_df
#    global csse_series_list
#    global csse_plot_days
#    csse_series_list.clear()
    
#    appended_data = []
#    appended_current_data = dict()    
       
#    for county in counties_list:
#        print("County: " +str(county))
 
        # get county population
#        county_loc_terms = county.split(', ')
#        print(county_loc_terms[0] +':' +county_loc_terms[1])
        #county_pop = county_pop_df.query('County==county_loc_terms[0] & State==county_loc_terms[1] ')
        
#        fips_code_value = csse_county_df.loc[(csse_county_df['Admin2'] == county_loc_terms[0]) & 
#                                             (csse_county_df['Province_State'] == county_loc_terms[1]) ].FIPS.iat[0]
        
#        print("FIPS: " +str(fips_code_value) +" " +str(type(fips_code_value)))
        
        # get all counts for selected county
 #       county_pop_series = county_pop_df[
#            (county_pop_df.County==county_loc_terms[0] +' County') & (county_pop_df.State==county_loc_terms[1])]
#            #(county_pop_df['County']==county_loc_terms[0]) & (county_pop_df['State']==county_loc_terms[1])]
#        county_pop = county_pop_series.iat[0,3]

        # extract just the daily case counts from selected row
#        county_counts_only_df = csse_county_df.loc[csse_county_df['Combined_Key'] == county].iloc[0, 11:]
        #print(county_counts_only_df)
        
        # get rolling average of daily difference in cases
#        print("calculating normalized rolling average")
        #county_full_series = county_counts_only_df.diff().shift().rolling(7).mean().apply(pop_normalize, args=(county_pop,))
#        county_full_series = county_counts_only_df.diff().rolling(7).mean().apply(pop_normalize, args=(county_pop,))
        #print(type(county_full_series))
        #print(county_full_series)
        
        # extract selected number of days for plot
#        num_days_index = -csse_plot_days
#        norm_cases_list = pd.Series(county_full_series.iloc[num_days_index:], name=county)
#        norm_cases_df = pd.DataFrame(norm_cases_list.astype(np.float16))
        #print(county_full_series.shape)
        #print(county_full_series)
#        csse_series_list.append(county_full_series)
        
        
#        county_latest_value = county_full_series.iat[-1]
        
#        appended_current_data.update({county : county_latest_value});
        #print(county +" : " +str(county_latest_value))
        
        #county_series_slice = get_county_norm_new_cases(county_full_series, county, plot_days)
#        appended_data.append(norm_cases_df)
    
#    csse_current_county_values = pd.Series(appended_current_data, 
#                             dtype='float16')
##    print(csse_current_county_values)
    #counties_norm_cases = counties_norm_cases.iloc[0:0]
#    csse_counties_norm_cases_df = pd.concat(appended_data, axis=1) #series_list)
    #print('csse_counties_norm_cases_df set type:' +str(type(csse_counties_norm_cases_df)))
#    print(csse_counties_norm_cases_df)
