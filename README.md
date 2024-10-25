
# Real Time Data Warehouse Streaming

This repository contains the code and configuration for the **EURO 2024 Real-Time Data Streaming and Visualization** project. 
The project leverages a real-time data pipeline to stream football data (teams, players, matches, groups, and events) from an API into Kafka. 
The data is processed and stored in **Apache Pinot** for fast analytics and visualized using **Apache Superset**.

## Project Overview

The primary goal of this project is to demonstrate how to build and manage a **real-time data warehouse** using modern tools and technologies. 
The data includes dynamic football statistics like live match events, player performance, and group standings for EURO 2024.

### Key Components

- **Apache Kafka**: Message broker used for real-time streaming of data.
- **Apache Pinot**: OLAP data store for fast querying and analytics.
- **Apache Superset**: Data visualization platform to create dashboards and monitor statistics.
- **Apache Airflow**: Workflow orchestration for automated data extraction and streaming.

## Architecture

The project consists of the following pipeline:

1. **API Extraction**: Data is fetched from a JSON-based API.
2. **Kafka Streaming**: Extracted data is streamed into Kafka topics.
3. **Processing with Pinot**: Kafka feeds the data into Apache Pinot for storage and querying.
4. **Visualization in Superset**: Real-time dashboards are created to visualize football statistics.

## Repository Structure

```
📦 Real Time Data Warehouse Streaming
├── dags/                    # Airflow DAGs for orchestration
│   ├── euro2024_data_streaming.py
├── pipelines                # ETL Pipline Definition Script
│   ├── euro2024_function.py
│   ├── create_table_schema.py
├── schemas/                 # Schemas definitions 
│   ├── groups_schema.json          # Schema for group data
│   ├── matches_schema.json         # Schema for match data
│   ├── players_schema.json         # Schema for player data
│   └── teams_schema.json           # Schema for team data
├── table-configs/           # Table definitions 
│   ├── groups_table.json           # Table configs for group data
│   ├── matches_table.json          # Table configs for match data
│   ├── players_table.json          # Table configs for player data
│   └── teams_table.json            # Table configs for team data
├── utils/                   # Utility files (constants, helper functions)
│   ├── constants.py
├── superset                 # Open Source Data Visualizer
│   ├── dockerfile                  # Docker File for Apache Superset
│   ├── superset_config.py          # Superset Image Config File
│   └── superset-init.sh            # To Initiate Bash Script For Superset  
├── Dockerfile               # Docker setup for containerized deployment
├── requirements.txt         # Python dependencies
├── .env
├── airflow.cfg
└── README.md                # Project documentation
```

## Installation and Setup

### Prerequisites

- Docker and Docker Compose installed.
- Apache Kafka, Pinot, and Superset configured.
- Airflow environment set up with Python 3.10.

### Steps to Run the Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/euro-2024-kafka-pinot-pipeline.git
   cd euro-2024-kafka-pinot-pipeline
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the Docker containers**:
   ```bash
   docker-compose up
   ```
4. **Access Superset**:
   - Visit `http://localhost:8088` in your browser.

5. **Launch Airflow**:
   - Visit `http://localhost:8080` to view and manage DAGs.

## Usage

- **Airflow DAGs** orchestrate the extraction of data from the API and stream it to Kafka.
- **Pinot** stores the streamed data for fast querying.
- **Superset Dashboards** visualize the real-time statistics, offering insights into player performance, match events, and group standings.

## Topics and Schemas

- **players**: Contains player statistics like goals, assists, and appearances.
- **teams**: Stores team details such as coach, captain, and championships.
- **matches**: Holds match details including scores, lineups, and winners.
- **groups**: Tracks group standings, points, and goal differences.

---

## Architecture

Below is the high-level architecture of the real-time data streaming pipeline:

![Architecture Diagram](./images/architecture.png)

---

## Airflow DAG Pipeline

The following diagram shows the Airflow DAG for orchestrating the data pipeline:

![DAG Pipeline Diagram](./images/dag_pipeline.png)

---

## Contributing

Feel free to open issues or submit pull requests for any feature improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Happy Streaming!
