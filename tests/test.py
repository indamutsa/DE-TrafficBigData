import math
import time
import random
from time import sleep

SEATTLE_COORDINATES = {"latitude": 47.608013, "longitude": -122.335167}
UNIVERSITY_COORDINATES = {"latitude": 46.7252, "longitude": -117.1596}

def calculate_increment(start, end):
    return end['latitude'] - start['latitude'], end['longitude'] - start['longitude']

def calculate_bearing(start_lat, start_lon, end_lat, end_lon):
    """
    Calculate the bearing between two points on the earth.
    Bearing is the compass direction to travel from the starting point to the end point.
    """
    lat1_rad = math.radians(start_lat)
    lat2_rad = math.radians(end_lat)
    lon_diff_rad = math.radians(end_lon - start_lon)

    # To get X, we calculate the following:
    # X = sin(Δlong) * cos(lat2)
    x = math.sin(lon_diff_rad) * math.cos(lat2_rad)
    # To get Y, we calculate the following:
    # Y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(Δlong)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(lon_diff_rad)
    
    initial_bearing_rad = math.atan2(x, y)
    initial_bearing_deg = math.degrees(initial_bearing_rad)
    bearing = (initial_bearing_deg + 360) % 360  # Normalize bearing
    
    return bearing

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on the earth using the Haversine formula.
    """
    R = 6371.0  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def simulate_acceleration(target_speed_kmh, acceleration_time_sec):
    """
    Simulate acceleration to the target speed over a given time and calculate the distance traveled.
    """
    # Convert speed from km/h to m/s
    target_speed_ms = target_speed_kmh * (1000 / 3600)
    # Acceleration in m/s^2 (initial speed is 0)
    acceleration_mss = target_speed_ms / acceleration_time_sec
    # Distance traveled during acceleration (s = 0.5 * a * t^2)
    distance_m = 0.5 * acceleration_mss * (acceleration_time_sec**2)
    return distance_m / 1000  # Convert to km

def update_position(start_lat, start_lon, distance_km, bearing_deg):
    """
    Calculate the new latitude and longitude based on the starting point, distance, and bearing.
    """
    degrees_per_km_lat = 1 / 110.574
    degrees_per_km_lon = 1 / (111.320 * math.cos(math.radians(start_lat)))
    
    # Calculate the new latitude and longitude
    new_lat = start_lat + (distance_km * degrees_per_km_lat * math.cos(math.radians(bearing_deg)))
    new_lon = start_lon + (distance_km * degrees_per_km_lon * math.sin(math.radians(bearing_deg)))
    
    return new_lat, new_lon

def incremental_movement(start_lat, start_lon, target_lat, target_lon, speed_kmh, time_elapsed_sec):
    """
    Moves the vehicle incrementally towards the target location based on the speed and time elapsed.

    Args:
        start_lat (float): Current latitude of the vehicle.
        start_lon (float): Current longitude of the vehicle.
        target_lat (float): Target latitude.
        target_lon (float): Target longitude.
        speed_kmh (float): Vehicle speed in km/h.
        time_elapsed_sec (int): Time elapsed in seconds for this movement.

    Returns:
        tuple: New latitude and longitude after incremental movement.
    """
    # Calculate the bearing from the current position to the target position
    bearing = calculate_bearing(start_lat, start_lon, target_lat, target_lon)
    
    # Convert speed from km/h to km/s
    speed_kms = speed_kmh / 3600
    
    # Calculate the distance covered in this time period (distance = speed * time)
    distance_covered_km = speed_kms * time_elapsed_sec
    
    # Calculate new position based on this distance and bearing
    new_lat, new_lon = update_position(start_lat, start_lon, distance_covered_km, bearing)
    
    return new_lat, new_lon

# Calculate the distance between two coordinates
def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    # Apply Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# def simulate_journey(start_lat, start_lon, end_lat, end_lon, target_speed_kmh, total_time_sec):
#     """
#     Simulates a journey from start to end, including an acceleration phase to reach the target speed.

#     Args:
#         start_lat, start_lon: Starting coordinates.
#         end_lat, end_lon: Destination coordinates.
#         target_speed_kmh: Target speed in km/h.
#         total_time_sec: Total time allocated for the journey in seconds.

#     Returns:
#         A list of (latitude, longitude) tuples representing the vehicle's path.
#     """
#     path = [(start_lat, start_lon)]
#     current_lat, current_lon = start_lat, start_lon
#     acceleration_time_sec = 20  # Time to reach target speed
#     time_elapsed_sec = 0  # Time tracker

#     # Phase 1: Acceleration
#     acceleration_distance_km = simulate_acceleration(target_speed_kmh, acceleration_time_sec)
#     # Assuming immediate acceleration to target speed for simplicity in path calculation
#     # In a more detailed model, you could calculate incremental positions during acceleration
#     current_lat, current_lon = update_position(current_lat, current_lon, acceleration_distance_km, calculate_bearing(current_lat, current_lon, end_lat, end_lon))
#     path.append((current_lat, current_lon))
#     time_elapsed_sec += acceleration_time_sec

#     # Phase 2: Constant speed movement towards the destination
#     while time_elapsed_sec < total_time_sec:
#         time_step_sec = min(60, total_time_sec - time_elapsed_sec)  # Use 60-second intervals or remaining time
#         current_lat, current_lon = incremental_movement(current_lat, current_lon, end_lat, end_lon, target_speed_kmh, time_step_sec)
#         path.append((current_lat, current_lon))
#         time_elapsed_sec += time_step_sec

#     return path

# # Example usage
# path = simulate_journey(47.608013, -122.335167, 46.7252, -117.1596, 100, 240)  # 4 minutes journey
# for lat, lon in path:
#     print(f"Position: {lat}, {lon}")


# import requests

# def get_osrm_route_full(start_lat, start_lon, end_lat, end_lon):
#     base_url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"
#     params = {
#         "overview": "full",  # Request the full route geometry
#         "geometries": "geojson"  # Get the route geometry in GeoJSON format
#     }
#     response = requests.get(base_url, params=params)
#     route = response.json()
#     return route

# route = get_osrm_route_full(47.608013, -122.335167, 46.7319, -117.1542)  # Seattle to WSU
# coordinates = route['routes'][0]['geometry']['coordinates']
# for coord in coordinates:
#     print(coord)

def simulate_dynamic_journey_fine_grained(start_lat, start_lon, end_lat, end_lon, total_distance_km, total_time_sec):
    current_lat, current_lon = start_lat, start_lon
    time_step_sec = 0.1  # Time step for the simulation, in seconds
    total_steps = int(total_time_sec / time_step_sec)
    distance_covered_km = 0
    speed_kmh = 0  # Initial speed

    # Initial and max speeds in km/h. These could be adjusted to simulate different scenarios
    max_speed_kmh = 3000  # Max speed for demonstration purposes
    acceleration_phase_steps = total_steps * 0.25  # 25% of the time for acceleration
    deceleration_phase_steps = total_steps * 0.25  # 25% of the time for deceleration
    constant_phase_steps = total_steps - acceleration_phase_steps - deceleration_phase_steps

    # Calculate required speed to cover the distance during the constant phase
    constant_speed_kmh = (total_distance_km / (constant_phase_steps * time_step_sec / 3600))

    print("Starting dynamic journey simulation...")
    for step in range(total_steps):
        # Acceleration phase
        if step < acceleration_phase_steps:
            speed_kmh += (max_speed_kmh / acceleration_phase_steps)  # Linearly increase speed
        # Deceleration phase
        elif step > total_steps - deceleration_phase_steps:
            speed_kmh -= (max_speed_kmh / deceleration_phase_steps)  # Linearly decrease speed
        # Constant speed phase
        else:
            speed_kmh = constant_speed_kmh  # Maintain constant speed

        # Calculate distance covered in this time step
        distance_covered_this_step_km = (speed_kmh / 3600) * time_step_sec
        distance_covered_km += distance_covered_this_step_km

        # Update position based on speed and bearing
        bearing = calculate_bearing(current_lat, current_lon, end_lat, end_lon)
        current_lat, current_lon = update_position(current_lat, current_lon, distance_covered_this_step_km, bearing)

        # Print current time and position
        current_time_sec = step * time_step_sec
        print(f"Time: {current_time_sec:.1f}s, Position: ({current_lat}, {current_lon})")

        # Sleep to simulate real-time progression
        time.sleep(time_step_sec)

# simulate_dynamic_journey_fine_grained(SEATTLE_COORDINATES["latitude"], SEATTLE_COORDINATES["longitude"], 
#                                       UNIVERSITY_COORDINATES["latitude"], UNIVERSITY_COORDINATES["longitude"], 
#                                       400, 60)

