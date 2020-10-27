import sys 
# A utility function to find the vertex with  
# minimum distance value, from the set of vertices  
# not yet included in shortest path tree 
def minDistance(graph, dist, sptSet): 
    # Initilaize minimum distance for next node 
    min = sys.maxsize 
    # Search not nearest vertex not in the  
    # shortest path tree 
    min_index = ""
    print(dist,sptSet)
    for key in graph: 
        if dist[key] <= min and sptSet[key] == False: 
            min = dist[key] 
            min_index = key 
    return min_index

def dijkstra(graph, src): 
    dist = {}
    sptSet = {}
    prevVer = {} 
    for key in graph:
        dist[key] = sys.maxsize
        sptSet[key] = False
    dist[src] = 0 
    prevVer[src] = src
    for cout in range(len(graph)): 

        # Pick the minimum distance vertex from  
        # the set of vertices not yet processed.  
        # u is always equal to src in first iteration 
        u = minDistance(graph,dist, sptSet) 

        # Put the minimum distance vertex in the  
        # shotest path tree 
        sptSet[u] = True

        # Update dist value of the adjacent vertices  
        # of the picked vertex only if the current  
        # distance is greater than new distance and 
        # the vertex in not in the shotest path tree 
        for e in graph[u]["e"]: 
            if sptSet[e['v']] == False and dist[e['v']] > dist[u] + e['w']: 
                dist[e['v']] = dist[u] + e['w']
                prevVer[e['v']] = u

    return dist,prevVer

graph = {'V1': {'p': 0, 'e': [{'w': 1, 'v': 'V2'}, {'w': 4, 'v': 'V3'}]}, 'V2': {'p': 1, 'e': [{'w': 1, 'v': 'V1'},{'w':0,'v':'V4'}, {'w': 1, 'v': 'V3'}, {'w': 5, 'v': 'V4'}]}, 'V3': {'p': 0, 'e': [{'w': 1, 'v': 'V4'}, {'w': 1, 'v': 'V2'}, {'w': 4, 'v': 'V1'}]}, 'V4': {'p': 2, 'e': [{'w': 1, 'v': 'V3'}, {'w':0,'v':'V2'}]}}

def getPath(prevVer,src,dst):
    print(prevVer,src,dst)
    if src == dst:
        return [src]
    elif dst not in prevVer:
        return []
    elif prevVer[dst] == src:
        return [src,dst]
    else:
        return getPath(prevVer,src,prevVer[dst]) + [dst]
