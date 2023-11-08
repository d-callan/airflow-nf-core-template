import datetime
import pendulum
import os

import requests
from airflow.decorators import dag, task

@dag(
    dag_id="reference-databases",
    schedule_interval=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def dada2():
    @task
    def copy_silva_to_cluster():
        
        # todo think about how this would work in production when run on pmacs. 
        ## how does the data get to pmacs?
        ## how does it monitor pmacs and get data back?
        ## how does it get pmacs config like base dir, login creds, etc?

        # todo think about global steps like ontology as well
        
        # todo how to make it run for every study we put in some dir? 
        ## check for new ones on some interval?
        ## run the same dag for each new study in that dir

        # todo consider templating this (and everything else lol) w jinja
        base_path = "/opt/airflow/inputDataDir/rRNAReference/SILVA/138_SSURef_NR99/final/"
        training_data_path = base_path + "training_set.138_SSURef_NR99.fa.gz"
        species_assignment_path = base_path + "species_assignment.138_SSURef_NR99.fa.gz"

        # todo this def needs looking at again, its missing the cluster base dir from the workflow config
        # it also should be templated for the workflow version at minimum
        # also idk if this is the right workflow version to use, i just sorta put 5 here
        cluster_home_dir = "workflows/MicrobiomeDB/5"