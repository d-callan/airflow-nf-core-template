import datetime
import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="nf_core_test2",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
) as dag:
    BashOperator(
        task_id="ampliseq",
        bash_command="/bin/nextflow run nf-core/ampliseq -profile test,conda --outdir out"
    )

if __name__ == "__main__":
    dag.test()

