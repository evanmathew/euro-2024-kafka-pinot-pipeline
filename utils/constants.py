
# Kafka settings
KAFKA_BOOTSTRAP_SERVERS = 'redpanda:9092'

# Local Schema Directory
SCHEMA_DIRECTORY = '/opt/airflow/schemas/'

# API settings
API_URLS = {
    'players': "https://euro-20242.p.rapidapi.com/players",
    'teams': "https://euro-20242.p.rapidapi.com/teams",
    'groups': "https://euro-20242.p.rapidapi.com/groups",
    'matches': "https://euro-20242.p.rapidapi.com/matches"
    # 'events': "https://euro-20242.p.rapidapi.com/matches"
}

# Define Kafka topics
KAFKA_TOPICS = {
    'players': 'euro2024_players_data',
    'teams': 'euro2024_teams_data',
    'groups': 'euro2024_groups_data',
    'matches': 'euro2024_matches_data'
    # 'events': 'euro2024_events_data'
}

HEADERS = {
    "x-rapidapi-key": "e0eb80aa38msh107f8c2e6a04f50p122a48jsnb234ea4f46b2",
    "x-rapidapi-host": "euro-20242.p.rapidapi.com"
}

PINOT_CONTROLLER_URL = 'http://pinot-controller:9000'
