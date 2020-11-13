from collections import defaultdict
import heapq

# defaultV = list of vertices that already been visited by the agent, in the curr state
def completeSpanningTree(graph, currentVertex,defaultV):
    mst = defaultdict(set)
    visited = set(defaultV)
    visited.add(currentVertex)
    edges = [
        (e['w'], currentVertex, e['v'])
        for e in graph[currentVertex]['e']
    ]
    # edges of the form : [(2, 'A', 'B'), (3, 'A', 'C')]
    sum = 0
    print(edges)
    heapq.heapify(edges)
    while len(visited) < len(graph) :
        cost, frm, to = heapq.heappop(edges)
        print("from, cost, to", frm, cost, to)
        print("visited  ", visited)
        print ("edges", edges)
        if to not in visited:
            visited.add(to)
            mst[frm].add(to)
            sum += cost
            for e in graph[to]['e']:
                if e['v'] not in visited:
                    heapq.heappush(edges, (e['w'], to, e['v']))
        print("MST      " ,mst,sum)
    return mst,sum

def heur(graph,n):
    _,sum = completeSpanningTree(graph,n.vertex,n.visited)
    return sum 