from collections import defaultdict
import heapq

# defaultV = list of vertices that already been visited by the agent, in the curr state
def completeSpanningTree(graph, currentVertex,defaultV):
    mst = defaultdict(set)
    visited = set(defaultV)
    
    edges = [
        (cost, currentVertex, to)
        for to, cost in graph[currentVertex].items()
    ]
    # edges of the form : [(2, 'A', 'B'), (3, 'A', 'C')]
    sum = 0
    heapq.heapify(edges)
    for i in range(len(graph)-1):
        cost, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst[frm].add(to)
            sum += cost
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    heapq.heappush(edges, (cost, to, to_next))

    return mst,sum

example_graph = {
    'A': {'B': 2, 'C': 3},
    'B': {'A': 2, 'C': 1, 'D': 1, 'E': 4},
    'C': {'A': 3, 'B': 1, 'F': 5},
    'D': {'B': 1, 'E': 1},
    'E': {'B': 4, 'D': 1, 'F': 1},
    'F': {'C': 5, 'E': 1, 'G': 1},
    'G': {'F': 1},
}

print(dict(completeSpanningTree(example_graph, 'B', ['A','B','C'])))