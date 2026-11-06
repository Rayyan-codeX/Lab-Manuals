graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}
def dls(node, goal, limit, path):
    if node == goal:
        return "FOUND", path
    if len(path) - 1 == limit:
        if len(graph[node]) > 0:
            return "CUTOFF", None
        else:
            return "FAILURE", None
    cutoff = False
    for child in graph[node]:
        if child not in path:
            status, new_path = dls(child, goal, limit, path + [child])
            if status == "FOUND":
                return status, new_path
            if status == "CUTOFF":
                cutoff = True
    if cutoff == True:
        return "CUTOFF", None
    return "FAILURE", None
for limit in range(1, 5):
    status, path = dls("A", "G", limit, ["A"])
    print("Depth Limit:", limit)
    if path == None:
        print("Status:", status)
        print("Path: Not Found")
    else:
        print("Status:", status)
        print("Path:", " -> ".join(path))
    print()
