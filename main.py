from services.data_generator import simulate_journey

if __name__ == "__main__":
    try:
        simulate_journey("vehicle-arsene-212")
    except KeyboardInterrupt:
        print("Simulation ended by the user")
    except Exception as e:
        print(f"Unexpected Error Occurred: {e}")
