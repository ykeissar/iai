from collections import defaultdict
import heapq, bisect
# edges of the form : [(2, 'A', 'B'), (3, 'A', 'C')]
# defaultV = list of vertices that already been visited by the agent, in the curr state
def completeSpanningTree(graph, currentVertex,defaultV):
    sum = 0
    mst = defaultdict(set)
    
    visited = set()
    visited.add(currentVertex)
    edges = []
    for e in graph[currentVertex]['e']:
        if e['v'] not in visited:
            edges.append((e['w'], currentVertex, e['v']))
    
    edges = list(filter((lambda t: t[1] not in defaultV and t[2] not in defaultV), edges))
    edges.sort(key=lambda t: t[0])

    while len(visited) < len(graph) :
        if len(edges) == 0:
            break
        cost, frm, to = heapq.heappop(edges)
        #remove all edges in the form of(_,_,to)
        out = list(filter((lambda t: t[2] == 'V2'), edges))
        for i in out:
            edges.remove(i)
        if to not in visited and to not in defaultV:
            visited.add(to)
            mst[frm].add(to)
            sum += cost
            for e in graph[to]['e']:
                if e['v'] not in visited and to not in defaultV:
                    bisect.insort(edges,(e['w'], to, e['v']))
            edges.sort(key=lambda t: t[0])
    # print("MST - ",mst," SUM - ",sum)
    return mst,sum

def heur(graph,n):
    _,sum = completeSpanningTree(graph,n.vertex,n.visited)
    return sum 