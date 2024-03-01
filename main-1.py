import os
from datetime import datetime, timedelta
import random
import uuid
from confluent_kafka import SerializingProducer
import simplejson as json

# End Points coordinates
SEATTLE_COORDINATES = { "latitude": 47.608013, "longitude": -122.335167 }
UNIVERSITY_COORDINATES = { "latitude": 47.655548, "longitude": -122.303200 }

# Calculating the movements
LATITUDE_INCREMENT = (UNIVERSITY_COORDINATES['latitude'] - SEATTLE_COORDINATES['latitude'])
LONGITUDE_INCREMENT = (UNIVERSITY_COORDINATES['longitude'] - SEATTLE_COORDINATES['longitude'])

# Env configuration
KAFKA_BOOTSTRAP_SERVER = os.environ.get('KAFKA_BOOTSTRAP_SERVER', 'localhost:9092')
VEHICLE_TOPIC = os.environ.get('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.environ.get('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.environ.get('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.environ.get('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.environ.get('EMERGENCY_TOPIC', 'emergency_data')

# Vehicle data
start_time = datetime.now()
start_location = SEATTLE_COORDINATES.copy() # Initial location, Copy to avoid reference

def getCurrentTime():
    global start_time
    return start_time + timedelta(seconds=random.randint(25, 60))

def generate_vehicle_data(vehicle_id):
    global start_location

    # Move toward the university
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT

    # Simulate Actual Vehicle Trip
    start_location['latitude'] += random.uniform(-0.005, 0.0005)
    start_location['longitude'] += random.uniform(-0.005, 0.0005)

    return start_location

def simulate_journey(producer, vehicle_id):
    while True:
        # Vehicle data
        vehicle_data = generate_vehicle_data(vehicle_id)

        return {
            "id": uuid.uuid4(),
            "vehicle_id": vehicle_id,
            "timestamp": getCurrentTime().isoformat(),
            "location": vehicle_data
        
        }

if __name__ == "main":
    # Kafka Producer
    producer_conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER,
        'key.serializer': 'org.apache.kafka.common.serialization.StringSerializer',
        'value.serializer': 'org.apache.kafka.common.serialization.StringSerializer'
    }
    producer = SerializingProducer(producer_conf)

    try:
        simulate_journey(producer, "vehicle-arsene-212")
    except KeyboardInterrupt:
        print("Simulation ended by the user")
    except Exception as e:
        print(f"Unexpected Error Occurred: {e}")

        # Close the producer
        producer.flush()
        producer.close()