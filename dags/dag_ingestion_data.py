import os

from cosmos.operators import DbtRunOperationOperator, DbtSeedOperator
# adjust for other database types

from modules.dbt_config import get_profile_config, get_project_config
from pendulum import datetime, duration

from airflow.datasets import Dataset
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup


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
def dag_ingestion_data():

    start_dag = EmptyOperator(task_id="start_dag")
    end_dag = EmptyOperator(task_id="end_dag")

    with TaskGroup(group_id="drop_seeds_if_exist") as drop_seeds:
        for seed in ["pokemons", "moves", "moves_pokemons", "raw_customers", "raw_payments", "raw_orders", "dolar_ibov", "usd_brl"]:
            DbtRunOperationOperator(
                task_id=f"drop_{seed}_if_exists",
                macro_name="drop_table_by_name",
                args={"table_name": seed},
                project_dir=DBT_PROJECT_PATH,
                # project_config=ProjectConfig(DBT_PROJECT_PATH),
                profile_config=get_profile_config(schema="raw"),
                install_deps=True,
            )

    dbt_seeds = DbtSeedOperator(
        task_id="dbt_seeds",
        project_dir=DBT_PROJECT_PATH,
        outlets=[Dataset("SEED://teste")],
        profile_config=get_profile_config(schema="raw"),
        operator_args={"install_deps": True},
    )

    start_dag >> drop_seeds >> dbt_seeds >> end_dag

dag_ingestion_data()
