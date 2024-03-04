import math
import time
import random

def calculate_increment(start, end):
    return end['latitude'] - start['latitude'], end['longitude'] - start['longitude']



SEATTLE_COORDINATES = {"latitude": 47.608013, "longitude": -122.335167}
UNIVERSITY_COORDINATES = {"latitude": 46.7252, "longitude": -117.1596}

def calculate_increment(start, end):
    return end['latitude'] - start['latitude'], end['longitude'] - start['longitude']

def calculate_bearing(start_coordinate, end_current_coordinate):
    start_lat, start_lon = start_coordinate
    end_lat, end_lon = end_current_coordinate

    """
    Calculate the bearing between two points on the earth.
    Bearing is the compass direction to travel from the starting point to the end point.
    """
    print(start_coordinate)
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

def haversine_distance(start_coordinate, end_current_coordinate):
    """
    Calculate the great circle distance between two points on the earth using the Haversine formula.
    """
    lat1, lon1 = start_coordinate
    lat2, lon2 = end_current_coordinate

    R = 6371.0  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def simulate_acceleration(target_speed_kmh, acceleration_time_sec):
    """
    Simulate acceleration and deceleration to the target 
    speed over a given time and calculate the distance traveled.
    """
    # Convert speed from km/h to m/s
    target_speed_ms = target_speed_kmh * (1000 / 3600)
    
    # Acceleration in m/s^2 (initial speed is 0)
    acceleration_mss = target_speed_ms / acceleration_time_sec
    
    # Distance traveled during acceleration (s = 0.5 * a * t^2)
    distance_m = 0.5 * acceleration_mss * (acceleration_time_sec**2)
    
    return distance_m / 1000  # Convert to km

def update_position(start_coordinate, distance_km, bearing_deg):
    """
    Calculate the new latitude and longitude based on the starting point, distance, and bearing,
    taking into account the curvature of the Earth.

    Args:
        start_coordinate (tuple): Starting latitude and longitude.
        distance_km (float): Distance to move in kilometers.
        bearing_deg (float): Bearing in degrees.

    Returns:
        tuple: New latitude and longitude.
    """
    R = 6371.0  # Earth's radius in kilometers
    delta = distance_km / R  # Angular distance in radians

    lat1 = math.radians(start_coordinate[0])
    lon1 = math.radians(start_coordinate[1])
    theta = math.radians(bearing_deg)

    lat2 = math.asin(math.sin(lat1) * math.cos(delta) +
                     math.cos(lat1) * math.sin(delta) * math.cos(theta))
    lon2 = lon1 + math.atan2(math.sin(theta) * math.sin(delta) * math.cos(lat1),
                             math.cos(delta) - math.sin(lat1) * math.sin(lat2))

    return math.degrees(lat2), math.degrees(lon2)

def generate_movement_with_rate(start_coord, target_coord, total_time_sec):
    """
    Moves towards a target location based on the total time to arrival,
    calculating the required speed to arrive within that time.

    Args:
        start_coord (tuple): Starting latitude and longitude.
        target_coord (tuple): Target latitude and longitude.
        total_time_sec (float): Total time to reach the target in seconds.

    Returns:
        tuple: New latitude, new longitude, and speed rate in km/s.
    """
    # Calculate the total distance to the target
    total_distance_km = haversine_distance(start_coord, target_coord)
    
    # Calculate required speed in km/s to cover the distance within the given time
    speed_kms = total_distance_km / total_time_sec
    
    # Calculate the bearing from the current position to the target position
    bearing = calculate_bearing(start_coord, target_coord)
    
    # Calculate distance covered in one second at the calculated speed
    distance_covered_km = speed_kms  # Since speed is km/s, distance covered in one second is the speed value
    
    # Update position based on this distance and bearing
    new_lat, new_lon = update_position(start_coord, distance_covered_km, bearing)
    
    # Return the new position and the speed rate in km/s
    return new_lat, new_lon, speed_kms

print(generate_movement_with_rate((47.608013, -122.335167), (46.7319, -117.1542), 40))

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

# def simulate_dynamic_journey_fine_grained(start_coord, end_coord, total_distance_km, total_time_sec):
    # current_lat, current_lon = start_coord['latitude'], start_coord['longitude']
    # end_lat, end_lon = end_coord['latitude'], end_coord['longitude']

    # print(start_coord)

    # time_step_sec = 0.1  # Time step for the simulation, in seconds
    # total_steps = int(total_time_sec / time_step_sec)
    # distance_covered_km = 0
    # speed_kmh = 0  # Initial speed

    # # Initial and max speeds in km/h. These could be adjusted to simulate different scenarios
    # max_speed_kmh = 3000  # Max speed for demonstration purposes
    # acceleration_phase_steps = total_steps * 0.25  # 25% of the time for acceleration
    # deceleration_phase_steps = total_steps * 0.25  # 25% of the time for deceleration
    # constant_phase_steps = total_steps - acceleration_phase_steps - deceleration_phase_steps

    # # Calculate required speed to cover the distance during the constant phase
    # constant_speed_kmh = (total_distance_km / (constant_phase_steps * time_step_sec / 3600))

    # print("Starting dynamic journey simulation...")
    # for step in range(total_steps):
    #     # Acceleration phase
    #     if step < acceleration_phase_steps:
    #         speed_kmh += (max_speed_kmh / acceleration_phase_steps)  # Linearly increase speed
    #     # Deceleration phase
    #     elif step > total_steps - deceleration_phase_steps:
    #         speed_kmh -= (max_speed_kmh / deceleration_phase_steps)  # Linearly decrease speed
    #     # Constant speed phase
    #     else:
    #         speed_kmh = constant_speed_kmh  # Maintain constant speed

    #     # Calculate distance covered in this time step
    #     distance_covered_this_step_km = (speed_kmh / 3600) * time_step_sec
    #     distance_covered_km += distance_covered_this_step_km

    #     print(f"{current_lat}, {current_lon}, {end_lat}, {end_lon  }")
    #     # Update position based on speed and bearing
    #     bearing = calculate_bearing((current_lat, current_lon), (end_lat, end_lon))
    #     current_lat, current_lon = update_position((current_lat, current_lon), distance_covered_this_step_km, bearing)

    #     # Print current time and position
    #     current_time_sec = step * time_step_sec
    #     print(f"Time: {current_time_sec:.1f}s, Position: ({current_lat}, {current_lon})")

    #     # Sleep to simulate real-time progression
    #     time.sleep(time_step_sec)

# simulate_dynamic_journey_fine_grained(SEATTLE_COORDINATES, 
#                                       UNIVERSITY_COORDINATES, 
#                                       400, 10)


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