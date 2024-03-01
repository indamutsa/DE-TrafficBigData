from datetime import datetime, timedelta
import random
import uuid

from utilities.coordinates import generate_random_movement

random.seed(42)

class Vehicle:
    def __init__(self, vehicle_id, start_location, end_location):
        self.id = uuid.uuid4()
        self.vehicle_id = vehicle_id
        self.location = start_location
        self.start_time = datetime.now()
        self.end_location = end_location

    def generate_vehicle_data(self, current_latitude, current_longitude):
        # Use the generate_random_movement function to get new latitude and longitude
        new_lat, new_lon = generate_random_movement(current_latitude, current_longitude, self.end_location['latitude'], self.end_location['longitude'], 2, 10)

        # Move toward the university
        self.location['latitude'] += new_lat
        self.location['longitude'] += new_lon

        # Simulate Actual Vehicle Trip
        self.timestamp = self.get_current_time().isoformat()
        self.speed = random.randint(10, 40) # km/h
        self.direction = 'North-East'
        self.make = 'Toyota'
        self.model = 'Corolla'
        self.year = 2015
        self.color = 'Red'
        self.license_plate = 'ABC-123'
        self.vehicle_type = 'Sedan'
        self.status = 'Active'
        self.fuel_type = 'Gasoline'
        self.fuel_level = random.randint(10, 100)

        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'location': self.location,
            'timestamp': self.timestamp,
            'speed': self.speed,
            'direction': self.direction,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'license_plate': self.license_plate,
            'vehicle_type': self.vehicle_type,
            'status': self.status,
            'fuel_type': self.fuel_type,
            'fuel_level': self.fuel_level
        }

    def generate_gps_data(self, vehicle_id, timestamp, vehicle_type="private"):
        return {
            "id": uuid.uuid4(),
            "timestamp": timestamp,
            "vehicle_id": vehicle_id,
            "speed": random.randint(0, 40),
            "direction": "North-East",
            "vehicle_type": vehicle_type
        }
    
    def generate_traffic_camera_data(self, vehicle_id, timestamp, location, camera_id):
        return {
            "id": uuid.uuid4(),
            "timestamp": timestamp,
            "vehicle_id": vehicle_id,
            "camera_id": camera_id,
            "location": location, # "latitude": "47.6062", "longitude": "122.3321"
            "snapshot": 'base64EncodedStringImage'
        }

    def generate_weather_data(self, vehicle_id, timestamp, location):
        return {
            "id": uuid.uuid4(),
            "timestamp": self.get_current_time().isoformat(), # timestamp,
            "vehicle_id": vehicle_id, # "vehicle-arsene-212"
            "temperature": random.randint(-10, 44), # -10 to 44 degree celsius
            "humidity": random.randint(10, 100), # 0-100%
            "wind_speed": random.randint(0, 40), # km/h
            "wind_direction": random.choice(["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]), # "North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"
            "location": location, # "latitude": "47.6062", "longitude": "122.3321"
            "weather": random.choice(["Sunny", "Rainy", "Snowy", "Cloudy"]), # "Sunny", "Rainy", "Snowy", "Cloudy"
            "precipitation": random.randint(0, 100), # 0-100%
            "visibility": random.randint(0, 20), # km 
            "pressure": random.randint(1000, 1030), # hPa
            "cloud_cover": random.randint(0, 100), # 0-100%
            "air_quality_index": random.randint(0, 500), # AQL > 300 is hazardous
        }
    
    def generate_emergency_incident_data(self, vehicle_id, timestamp, location):
        return {
            "id": uuid.uuid4(),
            "incident_id": uuid.uuid4(),
            "timestamp": timestamp,
            "vehicle_id": vehicle_id,
            "location": location, # "latitude": "47.6062", "longitude": "122.3321"
            "emergency_type": random.choice(["Accident", "Fire", "Theft", "Medical", "Other", "None"]),
            "description": "Vehicle involved in an accident",
            "severity": random.choice(["Low", "Medium", "High"]),
            "status": "Active"
        }
    
    def get_current_time(self):
        return self.start_time + timedelta(seconds=random.randint(25, 60))
