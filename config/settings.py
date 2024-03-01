import os

# Coordinates
SEATTLE_COORDINATES = {"latitude": 47.608013, "longitude": -122.335167}
UNIVERSITY_COORDINATES = {"latitude": 46.7252, "longitude": -117.1596}

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVER = os.environ.get('KAFKA_BOOTSTRAP_SERVER', 'localhost:9092')
VEHICLE_TOPIC = os.environ.get('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.environ.get('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.environ.get('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.environ.get('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.environ.get('EMERGENCY_TOPIC', 'emergency_data')
