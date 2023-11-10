FROM apache/airflow:2.7.2-python3.8 as base

FROM base as production-base
COPY --chown=airflow:root /eupath/data/EuPathDB/manualDelivery/MicrobiomeDB/common /opt/airflow/inputDataDir

FROM base as dev-base
COPY --chown=airflow:root test_data/ /opt/airflow/inputDataDir