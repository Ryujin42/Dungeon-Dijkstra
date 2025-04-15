import json
from os import TFD_TIMER_CANCEL_ON_SET
import random
from heapq import heapify, heappop, heappush

class Dungeon:
    """
    A class to represent a dungeon and calculate the shortest path in the dungeon
    using dijkstra algorithm.

        Methods:
            add_node(name): Create a new node in the graph.
            add_edge(nodeA, nodeB, weight): Create a new edge in the graph.
            calculate(start_node, end_node): calculate the shortest path from 
                `start_node` to `end_node` using dijkstra algorithm.
    """
    
    def __init__(self):
        self.graph = {}


    def add_node(self, name: str) -> bool:
        """
        Create a new node in the graph.

            Parameters:
                name (str): The name of the node

            Returns:
                bool: `True` if success, `False` otherwise
        """

        if name in self.graph:
            print(f"[Error]: name {name}  already used in graph")
            return False

        self.graph[name] = {}

        return True


    def add_edge(self, nodeA: str, nodeB: str, weight: float) -> bool:
        """
        Create a new edge in the graph.

            Parameters:
                nodeA (str): The name of the first node
                nodeB (str): The name of the second node
                weight (float): The weight of the edge

            Returns:
                bool: `True` if success, `False` otherwise
        """

        if nodeA not in self.graph:
            print(f"[Error]: node `{nodeA}` is not in graph")
            return False

        if nodeB not in self.graph:
            print(f"[Error]: node `{nodeB}` is not in graph")

        self.graph[nodeA][nodeB] = weight
        self.graph[nodeB][nodeA] = weight

        return True


    def generate_dungeon(self, num_rooms=2, max_time_cost=10):
        """
        Generate a new dungeon with a `Start` and a `Boss` rooms.

        Parameters:
            num_rooms (int): The total number of rooms
            max_time_cost (int): The maximum weight of travel in a room
        """

        self.graph = {}

        connected = ['Start']
        unconnected = [f'Room{i}' for i in range(1, num_rooms-1)]
        unconnected.append('Boss')

        while len(unconnected):
            existing_room = random.choice(connected)
            new_room = random.choice(unconnected)

            if existing_room == 'Start' and new_room == 'Boss':
                continue

            time_cost = random.randint(1, max_time_cost)

            if existing_room not in self.graph:
                self.graph[existing_room] = {}
            self.graph[existing_room][new_room] = time_cost
            
            if new_room not in self.graph:
                self.graph[new_room] = {}
            self.graph[new_room][existing_room] = time_cost

            connected.append(new_room)
            unconnected.remove(new_room)

        # optional: add extra paths
        extra_edges = random.randint(0, num_rooms//3*2)
        for _ in range(extra_edges):
            room1, room2 = random.sample(connected, 2)
            if room2 not in self.graph[room1]:
                time_cost = random.randint(1, max_time_cost)
                self.graph[room1][room2] = time_cost
                self.graph[room2][room1] = time_cost
       

    def generate_dungeon_graph_adjacency(self, cols, rows, num_rooms):
        DIRECTIONS = {
            'N': (0, -1),
            'S': (0, 1),
            'E': (1, 0),
            'W': (-1, 0)
        }
        OPPOSITE = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

        all_positions = [(x, y) for x in range(cols) for y in range(rows)]
        initial = random.choice(all_positions)

        visited = set()
        graph = {}
        stack = [initial]

        while stack and len(visited) < num_rooms:
            current = stack.pop()
            if current in visited:
                continue

            visited.add(current)
            graph[current] = set()

            x, y = current
            neighbors = []
            for dir_name, (dx, dy) in DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                neighbor = (nx, ny)
                if 0 <= nx < cols and 0 <= ny < rows and neighbor not in visited and neighbor not in graph:
                    neighbors.append((dir_name, neighbor))

            random.shuffle(neighbors)
            if neighbors:
                allowed_links = random.randint(1, min(3, len(neighbors)))
                for dir_name, neighbor in neighbors[:allowed_links]:
                    graph[current].add(dir_name)
                    graph.setdefault(neighbor, set()).add(OPPOSITE[dir_name])
                    stack.append(neighbor)

        # Ensure total room count
        while len(graph) < num_rooms:
            remaining = [pos for pos in all_positions if pos not in graph]
            if not remaining:
                break
            new_room = random.choice(remaining)
            graph[new_room] = set()

        # Randomize start and end
        room_positions = list(graph.keys())
        start, end = random.sample(room_positions, 2)

        # Label rooms
        room_labels = {}
        count = 1
        for pos in room_positions:
            if pos == start:
                room_labels[pos] = "Start"
            elif pos == end:
                room_labels[pos] = "Boss"
            else:
                room_labels[pos] = f"room{count}"
                count += 1

        # Create adjacency list
        adj_list = {label: {} for label in room_labels.values()}
        for pos, directions in graph.items():
            from_label = room_labels[pos]
            x, y = pos
            for dir in directions:
                dx, dy = DIRECTIONS[dir]
                neighbor_pos = (x + dx, y + dy)
                if neighbor_pos in graph:
                    to_label = room_labels[neighbor_pos]
                    adj_list[from_label][to_label] = 1

        self.graph = adj_list


    def calculate(self, start_node: str = 'Start', end_node: str = 'Boss') -> tuple[float, list[str]]:
        """
        Calculate the shortest path from `start_node` to `end_node` in the graph
        using dijkstra algorithm.

        Parameters: 
            start_node (str): The name of the starting node
            end_node (str): The name of the ending node

        Returns:
            tuple[float, list[str]]: (total_time, path) or (None, []) if no path exists.
        """
        
        times = {node: float("inf") for node in self.graph}
        times[start_node] = 0

        pq = [(0, start_node)]
        heapify(pq)

        visited = []

        # calculate shortest time
        while pq:
            current_time, current_node = heappop(pq)

            if current_node in visited:
                continue
            visited.append(current_node)

            for neighbor, weigth in self.graph[current_node].items():
                tentative_time = current_time + weigth
                if tentative_time < times[neighbor]:
                    times[neighbor] = tentative_time
                    heappush(pq, (tentative_time, neighbor))

        # get nodes in path
        predecessors = {node: None for node in self.graph}

        for node, time in times.items():
           for neighbor, weight in self.graph[node].items():
               if times[neighbor] == time + weight:
                   predecessors[neighbor] = node

        print(predecessors)

        # backtracking the path
        path: list[str] = [end_node]
        current_node = end_node

        while predecessors[current_node]:
            path.append(predecessors[current_node])
            current_node = predecessors[current_node]

        
        return (times[end_node], path[::-1])
    
    
    def __str__(self):
        return json.dumps(self.graph, sort_keys=True, indent=4)


dungeon = Dungeon()

dungeon.generate_dungeon_graph_adjacency(6, 6, 19)

print(dungeon)
print(dungeon.calculate())
