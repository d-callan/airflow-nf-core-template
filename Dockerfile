FROM apache/airflow:2.9.1-python3.10 as base

USER root

COPY --chown=airflow:root bin/nextflow /bin/nextflow

# Install base utilities
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         openjdk-17-jre-headless \
    && apt-get autoremove -yqq --purge \
    && apt-get install -y build-essential \
    && apt-get install -y wget \
    && apt-get install -y procps \
#    && apt-get install -y libblas-dev \
#    && apt-get install -y liblapack-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda
RUN chown airflow:root /opt/conda
# TODO figure something better than this
# it seems unsafe, and isnt doing what i want besides
# basically conda, airflow need to be able to modify this dir and subidr, files
# right now new files in /opt/conda/pkgs/cache dont inherit these very permissive perms
RUN chmod -R a+w /opt/conda/pkgs
# conda couldnt find it when install w apt-get, suspect they are named slightly differently or something
RUN /opt/conda/bin/conda install conda-forge::libblas

USER airflow

# Put conda in path so we can use conda activate
ENV PATH=/bin/nextflow:$CONDA_DIR/bin:$PATH
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

FROM base as production-base
COPY --chown=airflow:root /data/MicrobiomeDB/common /opt/airflow/inputDataDir

FROM base as dev-base
COPY --chown=airflow:root test_data/ /opt/airflow/inputDataDir
