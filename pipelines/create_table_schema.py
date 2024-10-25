import requests
import json

def create_pinot_table(schema_type):
    schema_file = f"/opt/airflow/schemas/{schema_type}_schema.json"
    config_file = f"/opt/airflow/table-configs/{schema_type}_table.json"
    
    # Pinot Controller endpoint
    pinot_controller_host = "http://pinot-controller:9000"
    
    # Create Schema
    with open(schema_file, 'r') as sf:
        schema_data = sf.read()
    schema_response = requests.post(
        f"{pinot_controller_host}/schemas/",
        headers={"Content-Type": "application/json"},
        data=schema_data
    )
    if schema_response.status_code != 200:
        raise Exception(f"Failed to create schema for {schema_type}: {schema_response.text}")
    print(f"Schema created for {schema_type}")

    # Create Table Configuration
    with open(config_file, 'r') as cf:
        config_data = cf.read()
    config_response = requests.post(
        f"{pinot_controller_host}/tables",
        headers={"Content-Type": "application/json"},
        data=config_data
    )
    if config_response.status_code != 200:
        raise Exception(f"Failed to create table config for {schema_type}: {config_response.text}")
    print(f"Table config created for {schema_type}")