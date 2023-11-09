FROM apache/airflow:2.7.2-python3.8

ARG TEST_MODE=false
RUN if [ "$TEST_MODE" = "true" ]; then \
        COPY --chown=airflow:root test_data/ /opt/airflow/inputDataDir; \
    else \
        COPY --chown=airflow:root /eupath/data/EuPathDB/manualDelivery/MicrobiomeDB/common /opt/airflow/inputDataDir; \
    fi

