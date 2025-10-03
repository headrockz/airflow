from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
from datetime import datetime


default_args = {
    'owner': 'asafe',
    'retries': 1,            
}


def get_ip():
    try:
        response = requests.get("https://ifconfig.me")
        response.raise_for_status()  
        ip = response.text
        print(f"The Airflow worker's external IP is: {ip}")
        return ip
    except requests.exceptions.RequestException as e:
        print(f"Error getting external IP: {e}")
        raise

with DAG(
    dag_id='dag_get_ip',
    default_args=default_args,
    schedule=None,  
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:
    get_ip_task = PythonOperator(
        task_id='get_ip',
        python_callable=get_ip,
    )
