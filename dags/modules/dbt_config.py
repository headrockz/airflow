from os import getenv

from cosmos import ExecutionConfig, ProfileConfig, ProjectConfig, RenderConfig
from cosmos.profiles import get_automatic_profile_mapping


def get_execution_config() -> ExecutionConfig:
    """
    Retrieves the executable path for dbt based on the given project ID.

    Returns:
        ExecutionConfig: An instance of ExecutionConfig containing the dbt executable path.
    """
    dbt_executable = getenv("DBT_EXECUTABLE_PATH", "/home/airflow/.local/bin/dbt")

    return ExecutionConfig(
        dbt_executable_path=dbt_executable,
    )   


def get_render_config(select: list) -> RenderConfig:
    """
    Returns the render configuration for the dbt project.
    Args:
        select (str): The selection criteria for the dbt project.
    Returns:
        RenderConfig: The render configuration object for the dbt project.
    """
    return RenderConfig(
        select=select
    )


def get_profile_config(schema: str = "public", target: str = "dev") -> ProfileConfig:
    """"
    Returns the profile configuration for the dbt project.
    Args:
        schema (str): The schema to use for the dbt project.
        conn (str): The connection ID to use for the dbt project.
    Returns:
        ProfileConfig: The profile configuration object for the dbt project.
    """
    conn = getenv("DBT_CONNECTION_ID", "postgres")
    return ProfileConfig(
        profile_name="cosmos",
        target_name=target,
        profile_mapping=get_automatic_profile_mapping(
            conn_id=conn,
            profile_args={"schema": schema},
   
        )
    )


def get_project_config(env_vars: dict = {}, dbt_vars: dict = {}) -> ProjectConfig:
    """
    Returns the project configuration for the dbt project.

    Returns:
        ProjectConfig: The project configuration object for the dbt project.
    """
    dbt_path = getenv("DBT_PROJECT_PATH", "/opt/airflow/dags/cosmos")

    return ProjectConfig(
        dbt_project_path=dbt_path,
        manifest_path=(f"{dbt_path}/target/manifest.json"),
        env_vars=env_vars,
        dbt_vars=dbt_vars
    )
