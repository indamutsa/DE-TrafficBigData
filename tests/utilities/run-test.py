
import time
import random
import math

current_rate_ms = 400
elapsed_time = 0
current_window = 0
start_time = 0

def calculate_current_rate(start_rate, target_rate, transition_duration, elapsed_time):
    if transition_duration <= 0:
        return target_rate
    
    # Calculate the rate of change
    rate_of_change = math.log(target_rate / start_rate) / transition_duration
    
    # Calculate the current rate based on elapsed time
    current_rate = start_rate * math.exp(rate_of_change * elapsed_time)

    # Ensure the current rate does not overshoot in either direction
    if start_rate < target_rate:
        current_rate = min(current_rate, target_rate)
    else:
        current_rate = max(current_rate, target_rate)
    
    return current_rate

def generate_change_intervals(total_duration_sec):
    total_windows = total_duration_sec // 10
    num_changes = [i + 1 for i in range(1, total_windows)]
    randomized_sample = random.sample(num_changes, random.randint(1, total_windows-1))

    return sorted(randomized_sample)


def print_at_rate( transition_duration, change_type,message="Printing at the machine's rate..."):
    elapsed_time = time.time() - start_time  # Calculate elapsed time since the start
    print(f"{message} | Current Rate: {current_rate_ms:.2f}ms | Elapsed Time: {elapsed_time:.2f}s | Change type: {change_type} |Transition: {transition_duration}| Current Window: {current_window}")
    time.sleep(current_rate_ms / 1000)




def simulate_window_acceleration( start_time,change_windows, transition_duration=6, stable_rate_ms=400, initial_stable_period_sec = 10, change_window_size=10, max_acceleration_rate_ms=100, max_deceleration_rate_ms=500):
    # Initialize the global elapsed_time variable
    global current_rate_ms, elapsed_time, current_window

    initial_rate_ms = 1000  # Starting with a slower rate   

    if current_window == 0:
        # Initial acceleration to stable_rate_ms
        while elapsed_time < initial_stable_period_sec:
            elapsed_time = time.time() - start_time
            if elapsed_time <= transition_duration:
                current_rate_ms = calculate_current_rate(initial_rate_ms, stable_rate_ms, transition_duration, elapsed_time)
            else:
                current_rate_ms = stable_rate_ms
            print_at_rate(transition_duration, "accelerate")
    else:
        updated_current_window = current_window + 1
        change_type = random.choice(['accelerate', 'decelerate']) if updated_current_window in change_windows else None

        rand_start = (current_window * change_window_size) + random.randint(1,8)
        transition_duration =  min(((updated_current_window) * change_window_size) - rand_start, transition_duration)
        iteration_stop = rand_start + transition_duration
        window_limit = (updated_current_window) * change_window_size

        a = False

        while elapsed_time < window_limit:

            elapsed_time = time.time() - start_time

            if change_type == 'accelerate' and updated_current_window in change_windows:                             
                if elapsed_time >= rand_start and elapsed_time <= iteration_stop:
                    if a == False:
                        inner_start_time = time.time()
                        a = True                    
                    if  current_rate_ms <= stable_rate_ms:
                            
                        inner_lapsed_time = time.time() - inner_start_time 
                        current_rate_ms = calculate_current_rate(current_rate_ms, max_acceleration_rate_ms, transition_duration, inner_lapsed_time) 
                    else:
                        inner_lapsed_time = time.time() - inner_start_time
                        current_rate_ms = calculate_current_rate( current_rate_ms, stable_rate_ms, transition_duration, inner_lapsed_time)
 
            elif change_type == 'decelerate' and updated_current_window in change_windows:
                if elapsed_time >= rand_start and elapsed_time <= iteration_stop:
                    if a == False:
                        inner_start_time = time.time()
                        a = True
                    if current_rate_ms >= stable_rate_ms:
                        inner_lapsed_time = time.time() - inner_start_time
                        current_rate_ms = calculate_current_rate(current_rate_ms, max_deceleration_rate_ms, transition_duration, inner_lapsed_time) 
                    
                    else:                        
                        inner_lapsed_time = time.time() - inner_start_time
                        current_rate_ms = calculate_current_rate(current_rate_ms, stable_rate_ms, transition_duration, inner_lapsed_time)

            print_at_rate(transition_duration, change_type)



def get_event(window, change_events):
    try:
        """Retrieve the event type ('accelerate' or 'decelerate') for the given window."""
        return next((event for event in change_events if list(event.keys())[0] == window), None)
    except Exception as e:
        print("Error:", e)
        return None

def simulate_dynamic_changes(total_duration_sec=60):
    global elapsed_time, current_window, current_rate_ms, start_time

    # Initializating the variables
    start_time = time.time()
    window_change_size = 10  # The size of the window for change in seconds

    # Generate change intervals 
    change_events = generate_change_intervals(total_duration_sec)

    print(">>>>>>> Change Events:", change_events)

    print(f">>===>: Simulating window acceleration... -->: {current_window}, Elasped Time: {elapsed_time}, Current Rate: {current_rate_ms}")

    while True:
        if elapsed_time > total_duration_sec - 10:
            break
        simulate_window_acceleration(start_time, change_events)
        current_window = (elapsed_time // window_change_size)
        print(f">>===>: Simulating window acceleration... -->: {current_window}, Elasped Time: {elapsed_time}, Current Rate: {current_rate_ms}")
 

simulate_dynamic_changes(60)


