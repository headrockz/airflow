import os

from cosmos import DbtTaskGroup

from modules.dbt_config import get_profile_config, get_project_config, get_execution_config, get_render_config
from pendulum import datetime, duration

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator


DBT_PROJECT_PATH = os.getenv("DBT_PROJECT_PATH", "/opt/airflow/dags/cosmos")
DBT_EXECUTABLE_PATH = os.getenv("DBT_EXECUTABLE_PATH", "/home/airflow/.local/bin/dbt")


default_args = {
    "owner": "Asafe",
    "depens_on_past": False,
    "retries": 2,
    "retry_delay": duration(minutes=5),
}


@dag(
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["load", "seeds"],
)
def dag_dolar_models():

    start_dag = EmptyOperator(task_id="start_dag")
    end_dag = EmptyOperator(task_id="end_dag")

    run_dbt_models = DbtTaskGroup(
        group_id="run-dbt-model-transfers",
        project_config=get_project_config(),
        execution_config=get_execution_config(),
        profile_config=get_profile_config(schema="trusted"),
        render_config=get_render_config(select=["tag:dolar"]),
        operator_args={
            "install_deps": True,
            "should_store_compiled_sql": True,
        },
    )

    start_dag >> run_dbt_models >> end_dag

dag_dolar_models()
