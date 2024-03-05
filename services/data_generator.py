import random
import time
from models.vehicle import Vehicle
from utilities.coordinates import calculate_distance, calculate_increment
from config.settings import SEATTLE_COORDINATES, UNIVERSITY_COORDINATES, VEHICLE_TOPIC, GPS_TOPIC, TRAFFIC_TOPIC, WEATHER_TOPIC, EMERGENCY_TOPIC
from services.kafka_producer import KafkaProducer
from utilities.dynamic_simulator import generate_change_intervals, simulate_window_acceleration

def simulate_journey(vehicle_id):
    """
    Simulates the journey of a vehicle by generating and sending data to Kafka topics.

    Args:
        vehicle_id (str): The ID of the vehicle.

    Returns:
        None
    """
    while True:
        # Initialize Kafka producer and vehicle
        producer = KafkaProducer()
        vehicle = Vehicle(vehicle_id, SEATTLE_COORDINATES.copy(), SEATTLE_COORDINATES.copy())
        latitude_increment, longitude_increment = calculate_increment(SEATTLE_COORDINATES, UNIVERSITY_COORDINATES)
        
        print(f"Vehicle Coordinates:  {vehicle.location}")

        # Generate vehicle data
        vehicle_data = vehicle.generate_vehicle_data(latitude_increment, longitude_increment)

        # Generate GPS data
        gps_data = vehicle.generate_gps_data(vehicle_data['vehicle_id'], vehicle_data['timestamp'])

        # Generate traffic camera data
        traffic_camera_data = vehicle.generate_traffic_camera_data(vehicle_data['vehicle_id'], vehicle_data['timestamp'], vehicle_data['location'], "Nikkon-cam123")

        # Generate weather data
        weather_data = vehicle.generate_weather_data(vehicle_data['location'], vehicle_data['timestamp'], vehicle_data['location'])

        # Generate emergency data
        emergency_data = vehicle.generate_emergency_incident_data(vehicle_data['vehicle_id'], vehicle_data['timestamp'], vehicle_data['location'])

        vehicle_lat = vehicle_data['location']['latitude']
        vehicle_lon = vehicle_data['location']['longitude']
        university_lat = UNIVERSITY_COORDINATES['latitude']
        university_lon = UNIVERSITY_COORDINATES['longitude']

        

        distance_km = calculate_distance(vehicle_lat, vehicle_lon, university_lat, university_lon)

        print(f"Distance left to University Coordinates: {distance_km:.2f} kilometers.")

        # Check if the vehicle has reached the destination
        if distance_km <= 0.1:  # Assuming 100 meters as "close enough"
            print("Vehicle has reached the destination. Simulation ended...")
            break


        # Send data to Kafka topics
        producer.publish(VEHICLE_TOPIC, vehicle_data, 'VEHICLE_TOPIC')
        producer.publish(GPS_TOPIC, gps_data, 'GPS_TOPIC')
        producer.publish(TRAFFIC_TOPIC, traffic_camera_data, 'TRAFFIC_TOPIC')
        producer.publish(WEATHER_TOPIC, weather_data, 'WEATHER_TOPIC')
        producer.publish(EMERGENCY_TOPIC, emergency_data, 'EMERGENCY_TOPIC')
        
        print("Data sent to Kafka")

        time.sleep(random.randint(1, 3)) # Sleep for a random number of seconds between 1 and 3

# ------------------------------

def simulate_dynamic_changes(total_duration_sec=60,  window_size = 10):
    global elapsed_time, current_window, current_rate_ms, start_time

    # Initializating the variables
    start_time = time.time()

    # Generate change intervals 
    change_events = generate_change_intervals(total_duration_sec)

    print(">>>>>>> Change Events:", change_events)

    print(f">>===>: Simulating window acceleration... -->: {current_window}, Elasped Time: {elapsed_time}, Current Rate: {current_rate_ms}")

    while True:
        if elapsed_time > total_duration_sec: 
            break
        simulate_window_acceleration(start_time, change_events)
        current_window = (elapsed_time // window_size)
        print(f">>===>: Simulating window acceleration... -->: {current_window}, Elasped Time: {elapsed_time}, Current Rate: {current_rate_ms}")