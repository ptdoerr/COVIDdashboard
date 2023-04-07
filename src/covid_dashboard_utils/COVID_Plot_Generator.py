# Plot manager 

import logging as log

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import dashboard_utils as utils

class PlotGenerator:    

    def __init__(self, width=8, height=5) -> None:
   
        self.fig_width = width # inches
        self.fig_height = height # inches

        self.csse_current_values_graph, self.csse_current_values_axes = plt.subplots(1, 1, figsize=(self.fig_width, self.fig_height))
        self.csse_ave_cases_graph, self.csse_ave_cases_axes = plt.subplots(1, 1, figsize=(self.fig_width, self.fig_height))
        #csse_current_values_graph.canvas.fig_widthlayout.width = '100%'
        #csse_current_values_graph.canvas.layout.height = '100%' #'900px'

        # define colormap for plotting and map
        # 0-2 green
        # >2 - 10 yellow
        # >10 - 25 orange
        # >25 - 75 red
        # >75 - 150 darkred
        # >150 #380000 - really dark red
        self.color_list = ['green', 'yellow','orange', 'red', 'darkred', '#380000']
        mapping_cmap = colors.ListedColormap(self.color_list)
        boundaries = [0, 2, 10, 25, 75, 150, 1000]
        self.map_color_norm = colors.BoundaryNorm(boundaries, mapping_cmap.N, clip=True)



    # plot bar graph of current case numbers
    # csse_counties_norm_cases_df - Dataframe containing normalized case values of selected counties 
    def plot_current_case_values(csse_counties_norm_cases_df: pd.Dataframe):
        log.info("in plot_current_csse_case_values()")
    
        self.csse_current_values_axes.cla()
        #csse_current_values_graph.clf()
    
        csse_current_county_values = csse_counties_norm_cases_df.iloc[-1, :]
 
        current_date = csse_counties_norm_cases_df.columns[-1] # csse_county_df.columns[-1]

        #find max of current values to size graph appropriately
        cases_set_max = max(csse_current_county_values) #douglas_current, sarpy_current, lancaster_current)
        #print("max; " +str(cases_set_max))

        #current_values_axes = current_new_cases.plot(kind="bar", ax=current_values_axes)
        self.csse_current_values_axes = csse_current_county_values.plot(kind="bar", 
                ax=self.csse_current_values_axes,
                rot=45)
  
        # show values on bar graph, format to display 2 decimal places
        for index, value in enumerate(csse_current_county_values):
            self.csse_current_values_axes.text(index, value,
                '{:.2f}'.format(value))
        #print(value)
        
        self.csse_current_values_axes.set_title("COVID 7 Day Ave Cases/100k for " +str(current_date))
    
        self.csse_current_values_axes.grid()

        # add color bands for severity 
        utils.set_graph_background_color_bands(self.csse_current_values_axes, cases_set_max, self.color_list)
    
        self.csse_current_values_graph.tight_layout()
        #csse_current_values_graph.subplots_adjust(bottom=0.05)
    
        plt.xticks(rotation=45, ha='right')
        #csse_current_values_axes.set_xticklabels(csse_current_values_axes.get_xticks(), rotation = 45)
  
        self.csse_current_values_graph.show()

    def get_current_values_graph_image() -> bytes:
        img_stream = io.BytesIO()
        #if save_loc == SAVE_TO_MONGODB or save_loc == SAVE_TO_S3 or save_loc == SAVE_ALL :
        self.csse_current_values_graph.savefig(img_stream, format='jpg')

        return img_stream.getvalue()

    def plot_time_series(csse_counties_norm_cases_df: pd.DataFrame, plot_range:int):
        print('In plot_time_series()')

        #global csse_counties_norm_cases_df
    
        self.csse_ave_cases_axes.cla()
        #csse_ave_cases_graph.clf()
    
        #print("csse_counties_norm_cases_df type:" +str(type(csse_counties_norm_cases_df)))
        #print(csse_counties_norm_cases_df)
    
        current_date = csse_counties_norm_cases_df.columns[-1]
          
        max_value = csse_counties_norm_cases_df.max().max()
        #print("Max value: ")
        #print(max_value)

    
        self.csse_ave_cases_axes = csse_counties_norm_cases_df.plot(ax=csse_ave_cases_axes, rot=45)
    
        self.csse_ave_cases_axes.set_title("COVID 7 Day Ave Cases/100k as of " +str(current_date))
    
        utils.set_graph_background_color_bands(self.csse_ave_cases_axes, max_value, self.color_list)
    
        self.csse_ave_cases_axes.grid()
    
        #csse_ave_cases_axes.set_xticklabels(csse_ave_cases_axes.get_xticks(), rotation = 45)
        #plt.xticks(rotation=45, ha='right')
        self.csse_ave_cases_graph.tight_layout()
        self.csse_ave_cases_graph.show()
        #print("ave_cases_graph: ")
        #print(type(ave_cases_graph))

        #counties_norm_cases.style

    def get_time_series_graph_image() -> bytes:
        img_stream = io.BytesIO()
        #if save_loc == SAVE_TO_MONGODB or save_loc == SAVE_TO_S3 or save_loc == SAVE_ALL :
        self.csse_ave_cases_graph.savefig(img_stream, format='jpg')

        return img_stream.getvalue()