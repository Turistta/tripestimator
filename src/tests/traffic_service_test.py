import bs4


def run():
    start_coords = "37.7680296,-122.4375126"
    end_coords = "37.7749295,-122.4194155"
    try:
        wrc = WazeRouteCalculator(start_coords, end_coords)
        route_time, route_distance, traffic_delay = wrc.calc_route_info()

        print(f"Origin: {start_coords}")
        print(f"Destination: {end_coords}")
        print(f"Distance (km): {route_distance:.2f}")
        print(f"Duration (minutes): {route_time:.2f}")
        print(f"Traffic Delay (minutes): {traffic_delay:.2f}")

    except WRCError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run()
