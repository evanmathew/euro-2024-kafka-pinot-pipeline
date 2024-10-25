"""
Extract, flatten, and stream data from the API to Kafka.

This script fetches data from the API, flattens it according to the schema type, and
streams it to Kafka.
"""

from kafka import KafkaProducer
import requests
import json
import os

from utils.constants import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPICS,
    API_URLS,
    HEADERS,
    SCHEMA_DIRECTORY,
)


def get_kafka_producer():
    """Initialize Kafka producer."""
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer


def load_schema(schema_name):
    """Load schema from the local directory."""
    schema_path = os.path.join(SCHEMA_DIRECTORY, f'{schema_name}.json')
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    return schema


def flatten_data(record, schema_type):
    """
    Flatten data based on the schema type.

    Args:
        record (dict): A single record from the API response.
        schema_type (str): The type of schema to flatten the data for.

    Returns:
        dict: The flattened record.
    """
    if schema_type == "players":
        return {
            "player_id": record["_id"],
            "player_name": record.get("name", ""),
            "position": record.get("position", ""),
            "club": record.get("club", ""),
            "team_name": record.get("team", {}).get("name", 0),
            "age": record.get("age", 0),
            "goals": record.get("goals", 0),
            "assists": record.get("assists", 0),
            "appearances": record.get("appearances", 0),
            "firstTeamAppearances": record.get("firstTeamAppearances", 0),
            "minutesPlayed": record.get("minutesPlayed", 0),
            "redCards": record.get("redCards", 0),
            "yellowCards": record.get("yellowCards", 0),
            "dateOfBirth": record.get("dateOfBirth", "")
        }
    elif schema_type == "matches":
        # Extract main match information
        date = record.get("date", "")
        stage = record.get("stage","unknown")
        stadium = record.get("stadium","unknown")
        city = record.get("city", "")
        winning_team = record.get("winningTeam","unknown")
        is_finished = record.get("isFinished", False)

        # Extract Team A details
        team_a = record.get("teamA", {})
        team_a_id = team_a.get("team", {}).get("_id", "")
        team_a_name = team_a.get("team", {}).get("name", "")
        team_a_score = team_a.get("score", 0)
        team_a_formation = team_a.get("lineup", {}).get("formation", "")

        # Extract Team B details
        team_b = record.get("teamB", {})
        team_b_id = team_b.get("team", {}).get("_id", "")
        team_b_name = team_b.get("team", {}).get("name", "")
        team_b_score = team_b.get("score", 0)
        team_b_formation = team_b.get("lineup", {}).get("formation", "")

        return {
            "match_id": record["_id"],
            "date": date,
            "stage": stage,
            "stadium": stadium,
            "city": city,
            "winning_team": winning_team,
            "is_finished": is_finished,
            "team_a_id": team_a_id,
            "team_a_name": team_a_name,
            "team_a_score": team_a_score,
            "team_a_formation": team_a_formation,
            "team_b_id": team_b_id,
            "team_b_name": team_b_name,
            "team_b_score": team_b_score,
            "team_b_formation": team_b_formation
        }
    elif schema_type == "teams":
        return {
            "team_id": record["_id"],
            "team_name": record.get("name", ""),
            "coach": record.get("coach", ""),
            "captain": record.get("captain", ""),
            "championships": record.get("championships", 0),
            "runnersUp": record.get("runnersUp", 0),
            "group_id": record.get("group",{}).get("_id", ""),
            "group_name": record.get("group",{}).get("name", "")
        }
    elif schema_type == "groups":
        teams_info = record.get("teams", [])
        
        # Flatten team information
        flattened_teams = [
            {
                "group_id": record["_id"],
                "group_name": record.get("name", ""),
                "team_id": team.get("team", {}).get("_id", ""),
                "team_name": team.get("team", {}).get("name", ""),
                "points": team.get("points", 0),
                "matches_played": team.get("matchesPlayed", 0),
                "matches_won": team.get("wins", 0),
                "matches_drawn": team.get("draws", 0),
                "matches_lost": team.get("losses", 0),
                "goals_scored": team.get("goalsScored", 0),
                "goals_conceded": team.get("goalsConceded", 0),
                "goal_difference": team.get("goalDifference", 0),
            }
            for team in teams_info
        ]
        
        # Return the flattened list of all teams
        return flattened_teams
    else:
        raise ValueError(f"Unknown schema type: {schema_type}")



def extract_and_stream_data(schema_type):
    """Fetch data from API, flatten it, and stream it to Kafka."""
    url = API_URLS[schema_type]
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()  # Adjust structure as per the API response

        # Initialize Kafka producer
        producer = get_kafka_producer()

        if isinstance(data, list):
            # Flatten and stream each record for lists
            for record in data:
                flat_records = flatten_data(record, schema_type)

                # Handle 'groups' schema by sending each team individually
                if schema_type == "groups":
                    for team in flat_records:
                        print(f"Sending: {team}")
                        producer.send(KAFKA_TOPICS[schema_type], value=team)
                else:
                    print(f"Sending: {flat_records}")
                    producer.send(KAFKA_TOPICS[schema_type], value=flat_records)
        elif isinstance(data, dict):
            # Handle dictionary responses
            for record in data.get(schema_type, []):
                flat_records = flatten_data(record, schema_type)

                if schema_type == "groups":
                    for team in flat_records:
                        print(f"Sending: {team}")
                        producer.send(KAFKA_TOPICS[schema_type], value=team)
                else:
                    print(f"Sending: {flat_records}")
                    producer.send(KAFKA_TOPICS[schema_type], value=flat_records)
        else:
            print(f"Unexpected data format for {schema_type}: {type(data)}")

        producer.flush()
        print(f"Successfully streamed {schema_type} data to Kafka.")
    else:
        print(f"Failed to retrieve {schema_type} data. Status code: {response.status_code}")
