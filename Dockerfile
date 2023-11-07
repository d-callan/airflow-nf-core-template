FROM apache/airflow:2.7.2-python3.8

COPY --chown=airflow:root /eupath/data/EuPathDB/manualDelivery/MicrobiomeDB/common /opt/airflow/inputDataDir
