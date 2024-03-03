import time
import random
import math

# Initial conditions and global variables
current_rate_ms = 400  # Current rate in milliseconds
elapsed_time = 0  # Elapsed time since the start
current_window = 0  # Current time window for change
start_time = 0  # Start time of the simulation

def calculate_current_rate(start_rate, target_rate, transition_duration, elapsed_time):
    """
    Calculate the current rate using exponential decay formula.
    Ensures that the rate does not exceed target limits.
    """
    if transition_duration <= 0:
        return target_rate
    
    rate_of_change = math.log(target_rate / start_rate) / transition_duration
    current_rate = start_rate * math.exp(rate_of_change * elapsed_time)
    current_rate = min(current_rate, target_rate) if start_rate <= target_rate else max(current_rate, target_rate)
    
    return current_rate

def generate_change_intervals(total_duration_sec):
    """
    Generate random intervals for acceleration or deceleration changes within the total simulation duration.
    """
    total_windows = total_duration_sec // 10
    num_changes = random.sample(range(1, total_windows), random.randint(1, total_windows-1))
    return sorted(num_changes)

def print_at_rate(transition_duration, change_type, message="Printing at the machine's rate..."):
    """
    Print current simulation status at the current rate.
    """
    global start_time, current_rate_ms
    elapsed_time = time.time() - start_time
    print(f"{message} | Current Rate: {current_rate_ms:.2f}ms | Elapsed Time: {elapsed_time:.2f}s | Change type: {change_type} | Transition: {transition_duration} | Current Window: {current_window}")
    time.sleep(current_rate_ms / 1000)

def simulate_window_acceleration(start_time, change_windows, transition_duration=6, stable_rate_ms=400, initial_stable_period_sec=10, change_window_size=10, max_acceleration_rate_ms=100, max_deceleration_rate_ms=500):
    """
    Simulates acceleration or deceleration within a given window, adhering to the specified parameters.
    """
    global current_rate_ms, elapsed_time, current_window

    if current_window == 0:
        # Initial acceleration to stable_rate_ms
        simulate_initial_acceleration(initial_stable_period_sec, transition_duration, stable_rate_ms)
    else:
        # Simulate dynamic changes based on the current window and change events
        simulate_dynamic_change(change_windows, change_window_size, transition_duration, stable_rate_ms, max_acceleration_rate_ms, max_deceleration_rate_ms)

def simulate_initial_acceleration(initial_stable_period_sec, transition_duration, stable_rate_ms):
    """
    Handle initial acceleration from the starting rate to the stable rate.
    """
    global current_rate_ms, elapsed_time, start_time
    initial_rate_ms = 1000  # Starting with a slower rate
    while elapsed_time < initial_stable_period_sec:
        elapsed_time = time.time() - start_time
        if elapsed_time <= transition_duration:
            current_rate_ms = calculate_current_rate(initial_rate_ms, stable_rate_ms, transition_duration, elapsed_time)
        else:
            current_rate_ms = stable_rate_ms
        print_at_rate(transition_duration, "accelerate")

def simulate_dynamic_change(change_windows, change_window_size, transition_duration, stable_rate_ms, max_acceleration_rate_ms, max_deceleration_rate_ms):
    """
    Simulate acceleration or deceleration based on dynamic events within the simulation.
    """
    global current_rate_ms, elapsed_time, current_window, start_time
    updated_current_window = current_window + 1
    change_type = random.choice(['accelerate', 'decelerate']) if updated_current_window in change_windows else None

    rand_start, iteration_stop, transition_duration = calculate_dynamic_window_params(updated_current_window, change_window_size, transition_duration)
    simulate_change_behavior(change_type, rand_start, iteration_stop, transition_duration, stable_rate_ms, max_acceleration_rate_ms, max_deceleration_rate_ms)

def calculate_dynamic_window_params(updated_current_window, change_window_size, transition_duration):
    """
    Calculate start, stop, and duration for dynamic changes within a window.
    """
    rand_start = (current_window * change_window_size) + random.randint(1, 8)
    transition_duration = min(((updated_current_window) * change_window_size) - rand_start, transition_duration)
    iteration_stop = rand_start + transition_duration
    return rand_start, iteration_stop, transition_duration

def simulate_change_behavior(change_type, rand_start, iteration_stop, transition_duration, stable_rate_ms, max_acceleration_rate_ms, max_deceleration_rate_ms):
    """
    Apply the calculated rate change based on the type of change event (acceleration or deceleration).
    """
    global current_rate_ms, elapsed_time, start_time
    a = False  # Flag to mark the start of a change event
    window_limit = (current_window + 1) * 10

    while elapsed_time < window_limit:
        elapsed_time = time.time() - start_time
        if change_type and elapsed_time >= rand_start and elapsed_time <= iteration_stop:
            inner_start_time, inner_lapsed_time = mark_change_start(a)
            current_rate_ms = apply_rate_change(change_type, transition_duration, stable_rate_ms, max_acceleration_rate_ms, max_deceleration_rate_ms, inner_lapsed_time)
            a = True
        print_at_rate(transition_duration, change_type)

def mark_change_start(a):
    """
    Mark the start time of a change event and calculate the elapsed time since the start.
    """
    if not a:
        inner_start_time = time.time()
    else:
        inner_start_time = None
    inner_lapsed_time = time.time() - inner_start_time if inner_start_time else 0
    return inner_start_time, inner_lapsed_time

def apply_rate_change(change_type, transition_duration, stable_rate_ms, max_acceleration_rate_ms, max_deceleration_rate_ms, inner_lapsed_time):
    """
    Calculate the new rate based on the type of change (accelerate or decelerate) and the current state.
    """
    if change_type == 'accelerate':
        target_rate = max_acceleration_rate_ms if current_rate_ms <= stable_rate_ms else stable_rate_ms
    else:
        target_rate = max_deceleration_rate_ms if current_rate_ms >= stable_rate_ms else stable_rate_ms
    return calculate_current_rate(current_rate_ms, target_rate, transition_duration, inner_lapsed_time)

def main():
    """
    Main function to run the car simulation.
    """
    global start_time, elapsed_time, current_window
    total_duration_sec = 60  # Total duration of the simulation in seconds
    start_time = time.time()

    change_events = generate_change_intervals(total_duration_sec)
    print("Change Events:", change_events)

    while elapsed_time <= total_duration_sec:
        simulate_window_acceleration(start_time, change_events)
        elapsed_time = time.time() - start_time
        current_window = elapsed_time // 10
        print(f"Window {current_window}: Elapsed Time: {elapsed_time:.2f}s, Current Rate: {current_rate_ms:.2f}ms")

if __name__ == "__main__":
    main()




# import sys
# import time
# from time import sleep
# import random
# import math

# current_rate_ms = 400
# elapsed_time = 0
# current_window = 0
# start_time = 0

# def calculate_current_rate(start_rate, target_rate, transition_duration, elapsed_time):
#     if transition_duration <= 0:
#         return target_rate
#     # Calculate the rate of change
#     rate_of_change = math.log(target_rate / start_rate) / transition_duration
#     # Calculate the current rate based on elapsed time
#     current_rate = start_rate * math.exp(rate_of_change * elapsed_time)

#     # Ensure the current rate does not overshoot in either direction
#     if start_rate < target_rate:
#         current_rate = min(current_rate, target_rate)
#         # print("Current Rate>>>: ", current_rate)
#     else:
#         current_rate = max(current_rate, target_rate)
#         # print("Current Rate: ", current_rate, target_rate)

#     # Optional: Adjust to integer if necessary
#     # current_rate = int(current_rate)
    
#     return current_rate

# def generate_change_intervals(total_duration_sec):
#     total_windows = total_duration_sec // 10
#     num_changes = [i + 1 for i in range(1, total_windows)]
#     randomized_sample = random.sample(num_changes, random.randint(1, total_windows-1))

#     return sorted(randomized_sample)


# def print_at_rate( transition_duration, change_type,message="Printing at the machine's rate..."):
#     elapsed_time = time.time() - start_time  # Calculate elapsed time since the start
#     print(f"{message} | Current Rate: {current_rate_ms:.2f}ms | Elapsed Time: {elapsed_time:.2f}s | Change type: {change_type} |Transition: {transition_duration}| Current Window: {current_window}")
#     time.sleep(current_rate_ms / 1000)




# def simulate_window_acceleration( start_time,change_windows, transition_duration=6, stable_rate_ms=400, initial_stable_period_sec = 10, change_window_size=10, max_acceleration_rate_ms=100, max_deceleration_rate_ms=500):
#     # Initialize the global elapsed_time variable
#     global current_rate_ms
#     global elapsed_time
#     global current_window



#     initial_rate_ms = 1000  # Starting with a slower rate   


#     if current_window == 0:
#         # Initial acceleration to stable_rate_ms
#         while elapsed_time < initial_stable_period_sec:
#             elapsed_time = time.time() - start_time
#             if elapsed_time <= transition_duration:
#                 current_rate_ms = calculate_current_rate(initial_rate_ms, stable_rate_ms, transition_duration, elapsed_time)
#             else:
#                 current_rate_ms = stable_rate_ms
#             print_at_rate(transition_duration, "accelerate")
#         # return current_rate_ms, elapsed_time
#     else:
#         # Change type: accelerate or decelerate
#         updated_current_window = current_window + 1
#         change_type = random.choice(['accelerate', 'decelerate']) if updated_current_window in change_windows else None

#         rand_start = (current_window * change_window_size) + random.randint(1,8)
#         transition_duration =  min(((updated_current_window) * change_window_size) - rand_start, transition_duration)
#         iteration_stop = rand_start + transition_duration
#         window_limit = (updated_current_window) * change_window_size
#         # change_type = random.choice(['accelerate', 'decelerate'])
#         # change_windows = [2, 3, 4, 5, 6]
#         # rand_start = 12
#         print("Change Type: ", change_type, " Rand Start, Stop: ", rand_start, iteration_stop)

#         # print(f"Change Type: {change_type} | Rand_start: {rand_start} | Stopping at {iteration_stop} | Transition Duration: {transition_duration} | Elapsed Time: {elapsed_time} | Window Limit: {window_limit}")
#         a = False

#         while elapsed_time < window_limit:

#             elapsed_time = time.time() - start_time
#             # inner_lapsed_time = elapsed_time % 10 

#             if change_type == 'accelerate' and updated_current_window in change_windows:               
#                 if elapsed_time >= rand_start and elapsed_time <= iteration_stop:
                    
#                     if  current_rate_ms <= stable_rate_ms:
#                         if a == False:
#                             inner_start_time = time.time()
#                             a = True
                            
#                         inner_lapsed_time = time.time() - inner_start_time 
#                         # print("Inner Lapsed Time: ", inner_lapsed_time)

#                         current_rate_ms = calculate_current_rate(current_rate_ms, max_acceleration_rate_ms, transition_duration, inner_lapsed_time) 
#                         # print("***1", current_rate_ms)

                       
#                     else:
#                         if a == False:
#                             inner_start_time = time.time()
#                             a = True
                            
#                         inner_lapsed_time = time.time() - inner_start_time
#                         # print("Inner Lapsed Time: ", inner_lapsed_time) 
#                         current_rate_ms = calculate_current_rate( current_rate_ms, stable_rate_ms, transition_duration, inner_lapsed_time)
#                         # print("***2", current_rate_ms)

#                 else:
#                     current_rate_ms = current_rate_ms
#             elif change_type == 'decelerate' and updated_current_window in change_windows:
#                 if elapsed_time >= rand_start and elapsed_time <= iteration_stop:
                    
#                     if current_rate_ms >= stable_rate_ms:
#                         if a == False:
#                             inner_start_time = time.time()
#                             a = True
                            
#                         inner_lapsed_time = time.time() - inner_start_time
#                         # print("Inner Lapsed Time: ", inner_lapsed_time)                        
#                         current_rate_ms = calculate_current_rate(current_rate_ms, max_deceleration_rate_ms, transition_duration, inner_lapsed_time) 
#                         # print("***3", current_rate_ms)
                    
#                     else:

#                         if a == False:
#                             inner_start_time = time.time()
#                             a = True
                            
#                         inner_lapsed_time = time.time() - inner_start_time
#                         # print("Inner Lapsed Time: ", inner_lapsed_time) 
#                         current_rate_ms = calculate_current_rate(current_rate_ms, stable_rate_ms, transition_duration, inner_lapsed_time)
#                         # print("***4", current_rate_ms)

#             # print(f"Change Type: {change_type} | Rand_start: {rand_start} | Transition Duration: {transition_duration} | Elapsed Time: {elapsed_time} | Window Limit: {window_limit}")
#             print_at_rate(transition_duration, change_type)
#         # sys.exit(0)    
#         # return current_rate_ms, elapsed_time


# def get_event(window, change_events):
#     try:
#         """Retrieve the event type ('accelerate' or 'decelerate') for the given window."""
#         return next((event for event in change_events if list(event.keys())[0] == window), None)
#     except Exception as e:
#         print("Error:", e)
#         return None

<<<<<<< HEAD
def simulate_dynamic_changes(total_duration_sec=60):
    global elapsed_time, current_window, current_rate_ms, start_time
=======
# def simulate_dynamic_changes(total_duration_sec=60):
#     global elapsed_time
#     global current_window
#     global current_rate_ms
#     global start_time
>>>>>>> cd40c4983b5fccb51c58f99eea97ec0a5045e8cf

#     # Initializating the variables
#     start_time = time.time()
#     window_change_size = 10  # The size of the window for change in seconds

#     # Generate change intervals 
#     change_events = generate_change_intervals(total_duration_sec)

#     print(">>>>>>> Change Events:", change_events)
#     # current_window = 1
#     # current_rate_ms = 0
#     # elapsed_time = 0
#     print(f">>===>: Simulating window acceleration... -->: {current_window}, Elasped Time: {elapsed_time}, Current Rate: {current_rate_ms}")

#     while True:
#         if elapsed_time > total_duration_sec - 10:
#             break
#         simulate_window_acceleration(start_time, change_events)
#         current_window = (elapsed_time // window_change_size)
#         print(f">>===>: Simulating window acceleration... -->: {current_window}, Elasped Time: {elapsed_time}, Current Rate: {current_rate_ms}")
 

# simulate_dynamic_changes(60)


