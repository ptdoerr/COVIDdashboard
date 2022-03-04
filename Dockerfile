FROM continuumio/miniconda3:4.10.3p1

WORKDIR /project

RUN conda install \
    numpy \
    pandas \
    matplotlib \
    geopandas \
    geoplot \
    mapclassify \
    jupyterlab
COPY ./README.md /project
#COPY ./data /project/data
COPY ./notebooks /project/notebooks

CMD ["jupyter-lab","--ip=0.0.0.0","--no-browser","--allow-root"]