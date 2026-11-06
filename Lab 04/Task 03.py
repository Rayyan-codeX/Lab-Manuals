
import heapq

def astar(graph, h, start, goal):
    pq = [(h[start], 0, start, [start])]
    visited = {start: 0}

    while pq:
        f, cost, current, path = heapq.heappop(pq)

        if current == goal:
            return cost, path

        if cost > visited[current]:
            continue

        for next_node, weight in graph[current]:
            new_cost = cost + weight

            if next_node not in visited or new_cost < visited[next_node]:
                visited[next_node] = new_cost
                new_path = path + [next_node]
                new_f = new_cost + h[next_node]

                heapq.heappush(pq, (new_f, new_cost, next_node, new_path))


# Graph
graph = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": []
}

# Heuristic values
h = {
    "S": 5,
    "A": 4,
    "B": 4,
    "C": 2,
    "G": 0
}

# Calling A* algorithm
result = astar(graph, h, "S", "G")
print("A* Result (Cost, Path):", result)
