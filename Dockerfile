FROM continuumio/miniconda3

WORKDIR /project

#RUN conda install \
#    numpy \
#    pandas \
#    matplotlib \
#    geopandas \
#    geoplot \
#    mapclassify \
#    pillow \
#    jupyterlab
    
#conda create -n geo_env
#conda activate geo_env
#conda config --env --add channels conda-forge
#conda config --env --set channel_priority strict
#conda install python=3 geopandas
#conda install geoplot mapclassify pillow jupyterlab
#conda install -c conda-forge ipywidgets ipympl nodejs

# create .yml from environment
# conda env export --no-builds > test_geo.yml

# Create Conda environment from the YAML file
COPY config/test_geo.yml .
RUN conda env create -f test_geo.yml

# Override default shell and use bash
SHELL ["conda", "run", "-n", "env", "/bin/bash", "-c"]

#COPY ./README.md /project
#COPY ./data /project/data
COPY ./config/jupyter_lab_config.py ./project/config
COPY ./notebooks /project/notebooks

EXPOSE 8888

CMD ["conda", "run", "-n", "test_geo", "jupyter-lab","--ip=0.0.0.0","--no-browser","--allow-root" "--config=./project/config/jupyter_lab_config.py", "notebooks/CSSE COVID Dashboard.ipynb"]

# Run this to get token where cdash is container name
# docker exec -it cdash conda run -n test_geo jupyter-lab list