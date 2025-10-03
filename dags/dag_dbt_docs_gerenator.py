from os import getenv
from modules.dbt_config import get_profile_config
from pendulum import datetime, duration

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator


# The path to the dbt project
from cosmos.operators import DbtDocsOperator


DBT_PROJECT_PATH = getenv("DBT_PROJECT_PATH", "/opt/airflow/dags/cosmos")




default_args = {
    "owner": "Asafe",
    "depens_on_past": False,
    "retries": 2,
    "retry_delay": duration(minutes=5),
}


@dag(
    start_date=datetime(2023, 8, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["moves", "types"],
)
def dag_dbt_docs_gerenator():

    start_dag = EmptyOperator(task_id="start_dag")
    end_dag = EmptyOperator(task_id="end_dag")

    generate_dbt_docs_gcs = DbtDocsOperator(
        task_id="generate_dbt_docs_gcs",
        project_dir=DBT_PROJECT_PATH,
        profile_config=get_profile_config(schema="raw"),
        operator_args={
            "install_deps": True,
        },
    )

    start_dag >> generate_dbt_docs_gcs >> end_dag


dag_dbt_docs_gerenator()
