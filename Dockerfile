FROM apache/airflow:2.7.2-python3.8 as base

COPY --chown=airflow:root bin/nextflow /bin/nextflow

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-11-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

FROM base as production-base
COPY --chown=airflow:root /eupath/data/EuPathDB/manualDelivery/MicrobiomeDB/common /opt/airflow/inputDataDir

FROM base as dev-base
COPY --chown=airflow:root test_data/ /opt/airflow/inputDataDir
