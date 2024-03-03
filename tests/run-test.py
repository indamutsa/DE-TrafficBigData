import sys
import time
from time import sleep
import random
import math

current_rate_ms = 400
elapsed_time = 0
current_window = 0
start_time = 0

def calculate_current_rate(start_rate, target_rate, transition_duration, elapsed_time):
    if transition_duration <= 0:
        # print("Transition duration must be greater than 0 ==> Current: ",current_rate, "Target: ",target_rate,"Start: ", start_rate, "Elapsed: ", elapsed_time, "Transition: ", transition_duration)
        return target_rate
    b = math.log(start_rate / target_rate) / transition_duration
    current_rate = (start_rate - target_rate) * math.exp(-b * elapsed_time) + target_rate
    # print("|| ==> Current: ",current_rate, "Target: ",target_rate,"Start: ", start_rate, "Elapsed: ", elapsed_time, "Transition: ", transition_duration)

    if start_rate < target_rate:
        current_rate = int(min(current_rate, target_rate))
        # print("Start is less than target ==> Current: ",current_rate, "Target: ",target_rate,"Start: ", start_rate, "Elapsed: ", elapsed_time, "Transition: ", transition_duration)
    else:
        current_rate = int(max(current_rate, target_rate))
        # print("Target is greater than start ==> Current: ",current_rate, "Target: ",target_rate,"Start: ", start_rate, "Elapsed: ", elapsed_time, "Transition: ", transition_duration)

    return current_rate

def generate_change_intervals(total_duration_sec):
    total_windows = total_duration_sec // 10
    num_changes = [i + 1 for i in range(1, total_windows)]
    randomized_sample = random.sample(num_changes, random.randint(1, total_windows-1))

    return sorted(randomized_sample)


def print_at_rate(message="Printing at the machine's rate..."):
    elapsed_time = time.time() - start_time  # Calculate elapsed time since the start
    print(f"{message} | Current Rate: {current_rate_ms:.2f}ms | Elapsed Time: {elapsed_time:.2f}s | Current Window: {current_window}")
    time.sleep(current_rate_ms / 1000)




def simulate_window_acceleration( start_time,change_windows, transition_duration=6, stable_rate_ms=400, initial_stable_period_sec = 10, change_window_size=10, max_acceleration_rate_ms=100, max_deceleration_rate_ms=500):
    # Initialize the global elapsed_time variable
    global current_rate_ms
    global elapsed_time
    global current_window



    initial_rate_ms = 1000  # Starting with a slower rate   


    if current_window == 0:
        # Initial acceleration to stable_rate_ms
        while elapsed_time < initial_stable_period_sec:
            elapsed_time = time.time() - start_time
            if elapsed_time <= transition_duration:
                current_rate_ms = calculate_current_rate(initial_rate_ms, stable_rate_ms, transition_duration, elapsed_time)
            else:
                current_rate_ms = stable_rate_ms
            print_at_rate()
        # return current_rate_ms, elapsed_time
    else:
        # Change type: accelerate or decelerate
        change_type_ = random.choice(['accelerate', 'decelerate']) if current_window + 1 in change_windows else None

        rand_start = (current_window * change_window_size) + random.randint(1,8)
        transition_duration =  min(((current_window + 1) * change_window_size) - rand_start, transition_duration)
        window_limit = (current_window + 1) * change_window_size
        change_type = 'accelerate'

        print(f"Change Type: {change_type_} | Rand_start: {rand_start} | Transition Duration: {transition_duration} | Elapsed Time: {elapsed_time} | Window Limit: {window_limit}")
        

        while elapsed_time < window_limit:
            elapsed_time = time.time() - start_time
            inner_lapsed_time = elapsed_time % 10

            if change_type == 'accelerate':
                # print("We are accelerating... from 400ms to 100ms, Elaspesd Time:", inner_lapsed_time)
    
                if elapsed_time <= 16:
                #    print("000000===  Elapsed_time:", elapsed_time, "Rand Start:", rand_start-10, "Transition Duration:", transition_duration, "Inner Lapsed Time:", inner_lapsed_time)
                   current_rate_ms = calculate_current_rate(stable_rate_ms, max_acceleration_rate_ms, transition_duration, inner_lapsed_time)
                else:
                    current_rate_ms = max_acceleration_rate_ms
                    # print("we are out of the transition period")
                    
            elif change_type == 'decelerate':
                # print("We are decelerating... from 100ms to 400ms, Elaspesd Time:", elapsed_time)

                current_rate_ms = calculate_current_rate(max_deceleration_rate_ms, stable_rate_ms, transition_duration, elapsed_time)
            print(f"Change Type: {change_type_} | Rand_start: {rand_start} | Transition Duration: {transition_duration} | Elapsed Time: {elapsed_time} | Window Limit: {window_limit}")
            print_at_rate()
        sys.exit(0)    
        # return current_rate_ms, elapsed_time


def get_event(window, change_events):
    try:
        """Retrieve the event type ('accelerate' or 'decelerate') for the given window."""
        return next((event for event in change_events if list(event.keys())[0] == window), None)
    except Exception as e:
        print("Error:", e)
        return None

def simulate_dynamic_changes(total_duration_sec=60):
    global elapsed_time
    global current_window
    global current_rate_ms
    global start_time

    # Initializating the variables
    start_time = time.time()
    window_change_size = 10  # The size of the window for change in seconds

    # Generate change intervals 
    change_events = generate_change_intervals(total_duration_sec)

    print(">>>>>>> Change Events:", change_events)
    # current_window = 1
    # current_rate_ms = 0
    # elapsed_time = 0
    print(f">>===>: Simulating window acceleration... -->: {current_window}, Elasped Time: {elapsed_time}, Current Rate: {current_rate_ms}")

    while True:
        if elapsed_time > total_duration_sec - 10:
            break
        simulate_window_acceleration(start_time, change_events)
        current_window = (elapsed_time // window_change_size)
        print(f">>===>: Simulating window acceleration... -->: {current_window}, Elasped Time: {elapsed_time}, Current Rate: {current_rate_ms}")
 

simulate_dynamic_changes(60)


