import json
import random
from heapq import heapify, heappop, heappush


class Dungeon:
    def __init__(self):
        self.graph = {}
        self.grid = []
        self.connections = {}



    def generate(self, dungeon_size: int, num_rooms: int, extra_vertexes: float) -> tuple[list, list]:
        if num_rooms < 1 or num_rooms > dungeon_size**2:
            return [], []

        # Initialize grid (0 = empty, 1 = room, 2 = corridor)
        self.grid = [[0 for _ in range(dungeon_size)] for _ in range(dungeon_size)]
        rooms = []
                
        self.grid[dungeon_size//2][dungeon_size//2] = 1
        rooms.append((dungeon_size//2, dungeon_size//2))
        
        while len(rooms) < num_rooms:
            random.shuffle(rooms)
            
            for room_x, room_y in rooms:
                neighbors = []
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx = room_x + dx
                    ny = room_y + dy
                    if 0 <= nx < dungeon_size and 0 <= ny < dungeon_size and self.grid[ny][nx] == 0:
                        neighbors.append((nx, ny))
                
                if neighbors:
                    new_x, new_y = random.choice(neighbors)
                    self.grid[new_y][new_x] = 1
                    rooms.append((new_x, new_y))
                    break
            
        # Connect every rooms (use tree logic)
        unconnected = set(rooms)
        connected = set()
        self.connections = []
        
        if rooms:
            start = rooms[0]
            connected.add(start)
            unconnected.remove(start)
            
            while unconnected:
                min_dist = float('inf')
                best_pair = None
                
                for (cx, cy) in connected:
                    for (ux, uy) in unconnected:
                        dx, dy = ux - cx, uy - cy
                        dist = abs(dx) + abs(dy)
                        if dist < min_dist:
                            min_dist = dist
                            best_pair = ((cx, cy), (ux, uy))
                
                if best_pair:
                    (x1, y1), (x2, y2) = best_pair

                    if x1 != x2:
                        step = 1 if x2 > x1 else -1
                        for x in range(x1, x2 + step, step):
                            if self.grid[y1][x] == 0:
                                self.grid[y1][x] = 2
                    if y1 != y2:
                        step = 1 if y2 > y1 else -1
                        for y in range(y1, y2 + step, step):
                            if self.grid[y][x2] == 0:
                                self.grid[y][x2] = 2
                    
                    self.connections.append(best_pair)
                    connected.add((x2, y2))
                    unconnected.remove((x2, y2))
        
        # Add some extra random connections

        for i in range(len(rooms)):
            for j in range(i+1, len(rooms)):
                x1, y1 = rooms[i]
                x2, y2 = rooms[j]

                if (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2):
                    if random.random() < extra_vertexes and ((x1, y1), (x2, y2)) not in self.connections:
                        if x1 == x2:  # Vertical connection
                            y_min, y_max = min(y1, y2), max(y1, y2)
                            for y in range(y_min, y_max + 1):
                                if self.grid[y][x1] == 0:
                                    self.grid[y][x1] = 2
                        else:  # Horizontal connection
                            x_min, x_max = min(x1, x2), max(x1, x2)
                            for x in range(x_min, x_max + 1):
                                if self.grid[y1][x] == 0:
                                    self.grid[y1][x] = 2
                        self.connections.append(((x1, y1), (x2, y2)))
        
        return self.grid, self.connections


    def prepare_dungeon_graph(self):
        room_coords = [(y, x) for y in range(len(self.grid)) for x in range(len(self.grid[0])) if self.grid[y][x] == 1]
        
        # Create graph dictionary
        self.graph = {room_coord: {} for room_coord in room_coords} 

        # Add all connections
        for (x1, y1), (x2, y2) in self.connections:
            room1 = (y1, x1)
            room2 = (y2, x2)
            self.graph[room1][room2] = 1
            self.graph[room2][room1] = 1
        
        return self.graph


    def calculate(self, start_node: tuple[int, int], end_node: tuple[int, int]) -> tuple[float, list[str]]:
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

        # backtracking the path
        path: list[str] = [end_node]
        current_node = end_node

        while predecessors[current_node]:
            path.append(predecessors[current_node])
            current_node = predecessors[current_node]

        
        return (times[end_node], path[::-1])
   

    def __str__(self):
        return json.dumps(self.graph, sort_keys=True, indent=4)

