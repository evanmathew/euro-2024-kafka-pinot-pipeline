from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import os
import sys


sys.path.insert(0,os.path.dirname((os.path.dirname(os.path.abspath(__file__))))) # insert parent directory (which will be the project root) into sys.path
from pipelines.euro2024_function import extract_and_stream_data
from pipelines.create_table_schema import create_pinot_table



# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
with DAG(
    'euro2024_data_streaming',
    default_args=default_args,
    schedule_interval=timedelta(minutes=10),
    catchup=False,
) as dag:

    # Start and End Dummy tasks for structure
    start = PythonOperator(
        task_id='start',
        python_callable=lambda: print("DAG Started"),
    )
    
    end = PythonOperator(
        task_id='end',
        python_callable=lambda: print("DAG Completed"),
    )

    # # Stream Data From API to Kafka
    with TaskGroup('stream_data_tasks', tooltip='Streaming Tasks') as stream_data_group:
        stream_players_data = PythonOperator(
            task_id='stream_players_data',
            python_callable=extract_and_stream_data,
            op_kwargs={'schema_type': 'players'}
        )

        stream_teams_data = PythonOperator(
            task_id='stream_teams_data',
            python_callable=extract_and_stream_data,
            op_kwargs={'schema_type': 'teams'}
        )
        
        stream_groups_data = PythonOperator(
        task_id='stream_groups_data',
        python_callable=extract_and_stream_data,
        op_kwargs={'schema_type': 'groups'}
        )

        stream_matches_data = PythonOperator(
            task_id='stream_matches_data',
            python_callable=extract_and_stream_data,
            op_kwargs={'schema_type': 'matches'}
        )
        
        # Define task dependencies inside the group
        stream_players_data >> stream_teams_data >> stream_groups_data >> stream_matches_data

    # # Create Pinot Tables & Schema Tasks
    with TaskGroup('create_tables_pinot_tasks', tooltip='Create Pinot Tables Tasks') as create_tables_schema_group:

    # Tasks to create schema and table config for each topic
        create_players_table = PythonOperator(
            task_id='create_players_table',
            python_callable=create_pinot_table,
            op_kwargs={'schema_type': 'players'}
        )

        create_teams_table = PythonOperator(
            task_id='create_teams_table',
            python_callable=create_pinot_table,
            op_kwargs={'schema_type': 'teams'}
        )

        create_groups_table = PythonOperator(
            task_id='create_groups_table',
            python_callable=create_pinot_table,
            op_kwargs={'schema_type': 'groups'}
        )

        create_matches_table = PythonOperator(
            task_id='create_matches_table',
            python_callable=create_pinot_table,
            op_kwargs={'schema_type': 'matches'}
        )

        create_players_table >> create_teams_table >> create_groups_table >> create_matches_table
        

    # DAG structure
    start  >> stream_data_group >> create_tables_schema_group >>  end
