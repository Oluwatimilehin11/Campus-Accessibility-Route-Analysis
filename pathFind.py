class Graph:
   
    def __init__(self):
        self.locations = {
            1: "Parking Garage",
            2: "EN-1054",
            3: "Panda Foods",
            4: "Library",
            5: "ED-1020",
            6: "Field House"
        }

        # Edge format: (node1, node2) or (node1, node2, descriptor): {'time': x, 'accessibility': y}
        # Accessibility scale: 1 (least accessible) to 5 (most accessible)
        self.edges = {
            (1, 2): {'time': 322, 'accessibility': 4},
            (1, 3): {'time': 400, 'accessibility': 3},
            (1, 5): {'time': 185, 'accessibility': 3},
            (1, 6): {'time': 413, 'accessibility': 2},
            (2, 3): {'time': 111, 'accessibility': 1},
            (2, 3, 'indoor'): {'time': 332, 'accessibility': 5},
            (3, 4): {'time': 254, 'accessibility': 4},
            (4, 5): {'time': 242, 'accessibility': 3},
            (4, 6): {'time': 218, 'accessibility': 3},
            (5, 6): {'time': 248, 'accessibility': 4}
        }

        # Make edges undirected
        new_edges = self.edges.copy()
        for key, attrs in self.edges.items():
            if len(key) == 2:
                u, v = key
                if (v, u) not in new_edges:
                    new_edges[(v, u)] = attrs
            elif len(key) == 3:
                u, v, descriptor = key
                if (v, u, descriptor) not in new_edges:
                    new_edges[(v, u, descriptor)] = attrs

        self.edges = new_edges

    def get_neighbors(self, node):
        """Return all neighbors of a given node"""
        neighbors = []
        for edge in self.edges:
            if node in edge[:2]:
                other = edge[1] if edge[0] == node else edge[0]
                neighbors.append((other, edge))
        return neighbors

    def dijkstra(self, start, end, metric='time'):
        
        weights = {node: float('inf') for node in self.locations}
        previous = {node: None for node in self.locations}
        weights[start] = 0

        unvisited = list(self.locations.keys())
        n_unvisited = len(unvisited)
        current = None

        while n_unvisited > 0 and current != end:
            min_weight = float('inf')
            current_index = -1
            i = 0
            while i < n_unvisited:
                node = unvisited[i]
                if weights[node] < min_weight:
                    min_weight = weights[node]
                    current = node
                    current_index = i
                i += 1

            if current is not None:
                unvisited.pop(current_index)
                n_unvisited -= 1

                neighbors_data = self.get_neighbors(current)
                j = 0
                n_neighbors = len(neighbors_data)
                while j < n_neighbors:
                    neighbor, edge = neighbors_data[j]
                    if neighbor in weights:
                        weight = 0
                        if metric == 'time':
                            weight = self.edges[edge]['time']
                        elif metric == 'accessibility':
                            accessibility_value = self.edges[edge]['accessibility']
                            if accessibility_value > 0:
                                weight = 6 - accessibility_value
                            else:
                                weight = float('inf') # Ignore inaccessible edges

                        alt = weights[current] + weight
                        if alt < weights[neighbor]:
                            weights[neighbor] = alt
                            previous[neighbor] = (current, edge)
                    j += 1
            else:
                break

        path = []
        current_path_node = end
        while previous[current_path_node] is not None:
            path.insert(0, current_path_node)
            current_path_node, edge_used = previous[current_path_node]
        if path and current_path_node == start:
            path.insert(0, current_path_node)
        elif current_path_node == start and not path:
            path = [start] if start == end else [start]
        else:
            path = []

        return path, weights[end] if end in weights else float('inf')

    def describe_path(self, path):
        """Generate a descriptive text for the path"""
        if not path or len(path) < 2:
            return "No path found or already at destination."

        description = "Start at " + self.locations[path[0]] + "\n"

        i = 0
        path_len = len(path)
        while i < path_len - 1:
            from_node = path[i]
            to_node = path[i+1]

            edge = None
            for e in self.edges:
                if (from_node in e[:2] and to_node in e[:2]):
                    edge = e
                    break

            if not edge:
                description += "→ Error: No edge found between " + self.locations[from_node] + " and " + self.locations[to_node] + "\n"
                i += 1
                continue

            edge_type = ""
            if len(edge) > 2:
                edge_type = " (" + edge[2] + ")"

            time = self.edges[edge]['time']
            accessibility = self.edges[edge]['accessibility']

            description += ("→ Go from " + self.locations[from_node] + " to " + self.locations[to_node] + edge_type +
                            " (Time: " + str(time) + " seconds, Accessibility: " + str(accessibility) + "/5)\n")
            i += 1

        description += "Arrive at " + self.locations[path[-1]]
        return description
