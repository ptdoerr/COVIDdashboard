# COVIDdashboard
This is primarily a Jupyter Notebook with some support for running a subset of functions as Flask services. The motivation for this project was that local COVID data was only reported as raw data which is pretty useless. I also wanted to learn Python so the this code documents my journey in that endeavour. I found a standard county level dataset that was upated daily

## Sections

### Load and Normalize

Loads COVID and county population data and combine into single DataFrame. Perform 7 day moving average and normalize per 100k using conty population data.

### Current Graphs

Display current case counts for selected counties. Any set of CONUS counties can be displayed.

<img src="/data/current-images/current-cases.jpg" width="300">

Display graph of case counts for selected counties. Any set of CONUS counties can be displayed. Date range is also selectable.

<img src="/data/current-images/current-graph.jpg" width="300">

### Current Map

<img src="/data/current-images/current-map.jpg" width="300">

### GIF Builder

Builds animated GIF of maps over selected date range. 

### Image Browser

Pick map image to display by date.

## Environment
- Jupyter Lab
Interactive notebook
- Flask

## Installation

### Required Software 
- Python 3.7
- conda 22.9

## Environment Variables
- AWS
AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY
- MongoDb


## Running

### Notebook
`conda env create -f config/test_geo.yml`

`conda activate test_geo`

`jupyter lab`

### Flask Server
`conda env create -f config/flask_env.yml`

`conda activate flask_env`

`flask run`
