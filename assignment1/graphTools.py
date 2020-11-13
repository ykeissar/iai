import sys 
import heapq

# A utility function to find the vertex with  
# minimum distance value, from the set of vertices  
# not yet included in shortest path tree 
def minDistance(graph, dist, sptSet): 
    # Initilaize minimum distance for next node 
    min = sys.maxsize 
    # Search not nearest vertex not in the  
    # shortest path tree 
    min_index = ""
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
    for _ in range(len(graph)): 

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
    if src == dst:
        return [src]
    elif dst not in prevVer:
        return []
    elif prevVer[dst] == src:
        return [src,dst]
    else:
        return getPath(prevVer,src,prevVer[dst]) + [dst]

def getAbstract(graph,currPos):
    vTag = []
    newGraph = {}
    for key in graph:
        if graph[key]['p']>0 or key == currPos:
            vTag.append(key)
            newGraph[key]={
                "p": graph[key]['p'],
                "e": []
            }
    for key in newGraph:
        dist = dijkstra(graph,key)[0]
        for v in vTag:
            if not (v == key or ({'v':v,'w':dist[v]} in newGraph[key]['e'])):
                newGraph[key]['e'].append({
                    'v':v,
                    'w':dist[v]
                })
    return newGraph


def astar(problem,h,currPos,limit,useG):
    firstNode= Node(currPos,[],None,0)
    open = [(h(problem,firstNode),firstNode)] # sorted list - (f(n),Node), sort by f(n)
    heapq.heapify(open)
    closed = []
    while limit > 0:
        if len(open) == 0:
            return "Failure"
        (_,next) = heapq.heappop(open)
        if h(problem,next) == 0:
            retPath = getSol(next)
            return retPath 
            
        closed.append(next)
        for n in expand(next,problem,useG):
            if n not in closed:
                heapq.heappush(open,(h(problem,n)+n.g,n))
        limit -= 1

def getSol(node):
    path = [node.vertex]
    while node.prevNode is not None:
        path = [node.prevNode.vertex] + path
        node =  node.prevNode
    return path

def expand(node,problem,useG):
    verticesToVisit = [n for n in getNodesWithPeoples(problem) if n not in node.visited and n != node.vertex]
    newNodes = []
    for nextVer in verticesToVisit:
        gn = node.g+getEdgeWeigh(problem,node.vertex,nextVer) if useG else 0
        newNode = Node(nextVer,node.visited+[node.vertex],node,gn)
        newNodes.append(newNode)        
    return newNodes
class Node:
    def __init__(self,vertex,visited, prevNode,g):
        self.vertex = vertex
        self.visited = visited
        self.prevNode = prevNode
        self.g = g
    def __repr__(self):
        return "[[vertex: {0}, visited: {1}, prevNode:{2}, g:{3}]]".format(
            self.vertex,self.visited,self.prevNode,self.g
        )
    def __gt__(self,other):
        self

def getNodesWithPeoples(graph):
    a = []
    for v in graph:
        if graph[v]['p'] > 0:
            a.append(v)    
    return a

def getEdgeWeigh(graph,frm,to):
    for i in graph[frm]['e']:
        if i['v'] == to:
            return i['w']
    return sys.maxsize


gr = {
    "V1": {
        "p": 0,
        "e": [
            {
                "v": "V2",
                "w": 4,
                "blocked": "False"
            },
            {
                "v": "V3",
                "w": 3,
                "blocked": "False"
            }
        ]
    },
    "V2": {
        "p": 1,
        "e": [
            {
                "v": "V1",
                "w": 4,
                "blocked": "False"
            },
            {
                "v": "V3",
                "w": 1,
                "blocked": "False"
            },
            {
                "v": "V4",
                "w": 5,
                "blocked": "False"
            }
        ]
    },
    "V3": {
        "p": 0,
        "e": [
            {
                "v": "V4",
                "w": 1,
                "blocked": "False"
            },
            {
                "v": "V2",
                "w": 1,
                "blocked": "False"
            },
            {
                "v": "V1",
                "w": 3,
                "blocked": "False"
            }
        ]
    },
    "V4": {
        "p": 2,
        "e": [
            {
                "v": "V3",
                "w": 1,
                "blocked": "False"
            },
            {
                "v": "V2",
                "w": 5,
                "blocked": "False"
            }
        ]
    }
}