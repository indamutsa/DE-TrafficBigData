import random
import math

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


# # Usage example
# current_latitude = 47.608013  # Seattle latitude
# current_longitude = -122.335167  # Seattle longitude
# end_latitude = 46.7252       # WSU latitude
# end_longitude = -117.1596     # WSU longitude
# target_speed_kmh = 100  # Target speed in km/h

# new_latitude, new_longitude = generate_random_movement(current_latitude, current_longitude, end_latitude, end_longitude, 2, 10, target_speed_kmh)

# print(f"New coordinates: {new_latitude}, {new_longitude}")


# # Usage example
# start_lat = 47.608013  # Seattle latitude
# start_lon = -122.335167  # Seattle longitude
# end_lat = 46.7252       # WSU latitude
# end_lon = -117.1596     # WSU longitude
# bearing = calculate_bearing(start_lat, start_lon, end_lat, end_lon)
# acceleration_distance_km = simulate_acceleration(100, 20)
# total_distance_km = acceleration_distance_km + random.uniform(2, 10)
# new_lat, new_lon = update_position(start_lat, start_lon, total_distance_km, bearing)

# print(f"New coordinates: {new_lat}, {new_lon}")




# def generate_random_movement(start_lat, start_lon, end_lat, end_lon, min_distance_km, max_distance_km):
#     # Approximate conversion values
#     degrees_per_km_lat = 1 / 110.574
#     degrees_per_km_lon = 1 / (111.320 * math.cos(math.radians(start_lat)))
    
#     # Random distance in km
#     distance_km = random.uniform(min_distance_km, max_distance_km)
    
#     # Calculate the bearing from the start point to the end point
#     lat1_rad = math.radians(start_lat)
#     lat2_rad = math.radians(end_lat)
#     lon_diff_rad = math.radians(end_lon - start_lon)
#     x = math.sin(lon_diff_rad) * math.cos(lat2_rad)
#     y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(lon_diff_rad)
#     initial_bearing_rad = math.atan2(x, y)
    
#     # Convert bearing to degrees
#     initial_bearing_deg = math.degrees(initial_bearing_rad)
#     bearing = (initial_bearing_deg + 360) % 360  # Normalize bearing
    
#     # Calculate the new latitude
#     new_lat = start_lat + (distance_km * degrees_per_km_lat * math.cos(math.radians(bearing)))
#     # Calculate the new longitude
#     new_lon = start_lon + (distance_km * degrees_per_km_lon * math.sin(math.radians(bearing)))
    
#     return new_lat, new_lon

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


