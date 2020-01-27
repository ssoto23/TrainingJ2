from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.zeppelin_plugin import ZeppelinNotebookOperator
from zeppelin_plugin.helper.Helpers import *

default_args = {
    'owner': 'Airflow',
    'depends_on_past': True,
    'start_date': datetime(2020, 1, 25, 20, 50),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
    'max_active_runs': 1,
    'schedule_interval': timedelta(minutes=30)
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('TrainingJ2', default_args=default_args, schedule_interval=timedelta(minutes=20), max_active_runs=1)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t0 = ZeppelinNotebookOperator(
    task_id='set_up_spark',
    notebook_id=Notebooks.SetUpClusterDeps.value,
    restart_interpreter=False,
    restart_before_start=True,
    interpreter_used=[Interpreters.SPARK.value, Interpreters.POSTGRES.value]
    ,
    dag=dag)

t1 = ZeppelinNotebookOperator(
    task_id='fetch_kafka_tweet_data',
    notebook_id=Notebooks.KafkaReader.value,
    restart_interpreter=False,
    interpreter_used=[Interpreters.SPARK.value, Interpreters.POSTGRES.value]
    ,
    dag=dag)

t2 = ZeppelinNotebookOperator(
    task_id='export_as_training_schema',
    notebook_id=Notebooks.ExportToSchema.value,
    restart_interpreter=False,
    interpreter_used=[Interpreters.SPARK.value, Interpreters.POSTGRES.value, Interpreters.REDSHIFT.value]
    ,
    dag=dag)

t3 = ZeppelinNotebookOperator(
    task_id='verify_s3_schema',
    notebook_id=Notebooks.PrepareRedshiftDb.value,
    restart_interpreter=True,
    interpreter_used=[Interpreters.POSTGRES.value, Interpreters.REDSHIFT.value]
    ,
    dag=dag)

t4 = ZeppelinNotebookOperator(
    task_id='prepare_redshift_load_manifest_files',
    notebook_id=Notebooks.PrepareFilesToLoad.value,
    restart_interpreter=True,
    interpreter_used=[Interpreters.POSTGRES.value, Interpreters.REDSHIFT.value]
    ,
    dag=dag)

t5 = ZeppelinNotebookOperator(
    task_id='load_data_redshift',
    notebook_id=Notebooks.RedshiftLoadFiles.value,
    restart_interpreter=True,
    interpreter_used=[Interpreters.POSTGRES.value, Interpreters.REDSHIFT.value]
    ,
    dag=dag)

t1.set_upstream(t0)
t2.set_upstream(t1)
t3.set_upstream(t2)
t4.set_upstream(t2)
t5.set_upstream(t4)
t5.set_upstream(t3)
