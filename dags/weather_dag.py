from airflow import DAG
from datetime import datetime
from airflow.operators.python import ( PythonOperator )

# Python ETL method
from weather_data import (
    get_previous_hour_weather_data,
    transform_data,
    load_data
)

# Default arguments for DAGs
default_args = {
    'owner': 'Saurabh',
    'start_date': datetime(2023, 10, 7),
    'retries': 1
}

# Create weather DAG instance
dag = DAG(
    'weather-etl-dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

# Tasks for Extract function
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=get_previous_hour_weather_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    op_args=[extract_task.output],
    provide_context=True,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    op_args=[transform_task.output],
    provide_context=True,
    dag=dag,
)

# Task dependencies
extract_task >> transform_task >> load_task