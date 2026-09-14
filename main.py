from pathFind import Graph

def display_locations(graph):
    
    print("\nAvailable Locations:")
    for num, name in graph.locations.items():
        print(str(num) + ": " + name)

def get_user_choice(prompt, options):
    """Get valid user input from given options"""
    while True:
        try:
            choice = int(input(prompt))
            if choice in options:
                return choice
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")

def main():
    print("=== Campus Path Finder ===")
    print("Find the best route between campus locations\n")

    graph = Graph()
    display_locations(graph)

    # Get user inputs
    start = get_user_choice("\nEnter starting location number: ", graph.locations.keys())
    end = get_user_choice("Enter destination location number: ", graph.locations.keys())

    if start == end:
        print("You're already at your destination!")
        return

    print("\nChoose path finding metric:")
    print("1: Shortest time")
    print("2: Most accessible")
    metric_choice = get_user_choice("Enter your choice (1 or 2): ", [1, 2])
    metric = 'time' if metric_choice == 1 else 'accessibility'

    # Find path
    path, total_weight = graph.dijkstra(start, end, metric)

    if not path:
        print("\nNo valid path found between these locations.")
    else:
        if metric == 'time':
            total_time_minutes = total_weight // 60
            total_time_seconds = total_weight % 60
            print("\nShortest path (Total time: " + str(total_time_minutes) + " minutes " + str(total_time_seconds) + " seconds):")
        else:
            # Calculate total accessibility score for the path
            total_accessibility_score = 0
            i = 0
            path_len = len(path)
            while i < path_len - 1:
                from_node = path[i]
                to_node = path[i+1]
                edge = None
                for e in graph.edges:
                    if (from_node in e[:2] and to_node in e[:2]):
                        edge = e
                        break
                if edge:
                    total_accessibility_score += graph.edges[edge]['accessibility']
                i += 1
            avg_accessibility = total_accessibility_score / (len(path) - 1) if len(path) > 1 else 0
            print("\nMost accessible path (Average accessibility: " + "{:.1f}".format(avg_accessibility) + "/5):")

        print(graph.describe_path(path))

if __name__ == "__main__":
    main()
