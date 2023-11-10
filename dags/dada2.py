import datetime
import pendulum
import os
import sys

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor

# todo think about global steps like ontology as well
@dag(
    dag_id="dada2",
    schedule_interval=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def dada2():
    @task
    def make_nextflow_config():
        # todo this also needs to happen per study, all these tasks do.. not sure how to do that
        sys.stderr.write("making nextflow config\n")
        base_path = "/opt/airflow/inputDataDir/rRNAReference/SILVA/138_SSURef_NR99/final/"
        training_data_path = base_path + "training_set.138_SSURef_NR99.fa.gz"
        species_assignment_path = base_path + "species_assignment.138_SSURef_NR99.fa.gz"

        config = "workingDir=/opt/airflow/inputDataDir/studies/test-study-dada2/workspace/ \
                trainingSetFile=" + training_data_path + " \
                speciesAssignmentFile=" + species_assignment_path + " \
                resultFile=/opt/airflow/inputDataDir/studies/test-study-dada2/results/"
        
        with open("/opt/airflow/inputDataDir/studies/test-study-dada2/config_file", "w") as f:
            f.write(config)

    @task
    def copy_to_cluster():
        # todo ignore this for test mode somehow?
        # or should there be a run local mode?
        # todo consider templating everything w jinja

        # todo think about how this would work in production when run on pmacs. 
        ## how does the data get to pmacs?
        ## how does it get pmacs config like base dir, login creds, etc?     
       
        sys.stderr.write("copying to cluster\n")

    @task
    def run_dada2_on_cluster():
        # todo this doesnt conform to the current manualDelivery structure. figure that out later
        base_path = "/opt/airflow/inputDataDir/studies/"

        studies = os.listdir(base_path)
        sensor_task = FileSensor(
            task_id="file_sensor", 
            filepath=base_path,
            poke_interval=86400,
        )

        for study in studies:
            study_path = os.path.join(base_path, study)
            task_name = f"dada2_{study}"
            # todo not sure i have the nextflow command right
            nextflow_command = f"nextflow run VEuPathDB/MarkerGeneAnalysis16sDADA2 -with-trace -c  /opt/airflow/inputDataDir/studies/test-study-dada2/config_file -r main --input {study_path}"
            sys.stderr.write(f"running {task_name}\n")
            task_instance = BashOperator(
                task_id=task_name,
                bash_command=nextflow_command,
                dag=dada2
            )

            sensor_task >> task_instance
        

        # todo this def needs looking at again, its missing the cluster base dir from the workflow config
        # it also should be templated for the workflow version at minimum
        # also idk if this is the right workflow version to use, i just sorta put 5 here
        cluster_home_dir = "workflows/MicrobiomeDB/5"

    @task
    def copy_results_to_local():
        sys.stderr.write("copying results to local\n")
        ## todo how does it monitor pmacs and get data back?

    make_nextflow_config() >> copy_to_cluster() >> run_dada2_on_cluster() >> copy_results_to_local()

dada2 = dada2()