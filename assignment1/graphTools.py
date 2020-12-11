import sys 
import bisect,heapq

global trace_id
trace_id=0
def minDistance(graph, dist, sptSet): 
    min = sys.maxsize 
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
        u = minDistance(graph,dist, sptSet) 
        sptSet[u] = True 
        for e in graph[u]["e"]: 
            if sptSet[e['v']] == False and dist[e['v']] > dist[u] + e['w']: 
                dist[e['v']] = dist[u] + e['w']
                prevVer[e['v']] = u

    return dist,prevVer

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

def astar(problem,h,currPos,limit,type):
    expantions = 0
    print("\nAstar calculation begin @@")
    firstNode= Node(trace_id,currPos,[],None,0)
    open = [(h(problem,firstNode),firstNode)]
    closed = []
    x = 0 if type == 'greedy' else 1
    while limit > 0:
        if len(open) == 0:
            return "Failure"
        (_,_next) = heapq.heappop(open)
        print("Next Node: ", _next.printState())
        #we reached a goal
        if h(problem,_next) == 0:
            print("Astar calculation finished @@\n")
            return getSol(_next),expantions 
        closed.append(_next)
        expantions += 1
        for n in expand(_next,problem,x):
            if n not in closed:
                bisect.insort(open,(h(problem,n)+x*n.g,n))
        limit -= 1
        open.sort(key=lambda t: t[0])
    (_,_next) = heapq.heappop(open)
    print("Astar calculation finished @@\n")
    return getSol(_next),expantions

def matchHeuristic(h,problem,node,isG):
    return (h(problem,node)+isG*node.g)

def getSol(node):
    path = [node.vertex]
    while node.prevNode is not None:
        path = [node.prevNode.vertex] + path
        node =  node.prevNode
    return path

def expand(node,problem,useG):
    verticesToVisit = [n for n in getNodesWithPeoples(problem) if n not in node.visited and n != node.vertex]
    newNodes = []
    global trace_id
    for __nextVer in verticesToVisit:
        trace_id +=1
        gn = (node.g+getEdgeWeigh(problem,node.vertex,__nextVer))*useG
        newNode = Node(trace_id, __nextVer,node.visited+[node.vertex],node,gn)
        newNodes.append(newNode)        
    return newNodes
class Node:
    def __init__(self,stateId,vertex,visited, prevNode,g):
        self.stateId = stateId
        self.vertex = vertex
        self.visited = visited
        self.prevNode = prevNode
        self.prevStateId = prevNode.stateId if prevNode is not None else -1
        self.g = g
    def __repr__(self):
        return "[[vertex: {0}, visited: {1}, prevNode:{2}, g:{3}]]".format(
            self.vertex,self.visited,self.prevNode,self.g
        )
    def __gt__(self,other):
        self
    def printState(self):
        return "[[stateId: {0}, currPos: {1}, prevState: {2}, prevPos: {3}, currGval: {4}, visited:{5}]]".format(
            self.stateId,self.vertex,self.prevStateId, self.prevNode.vertex if self.prevNode != None else "", self.g, self.visited
        )

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

def printOpen(open):
    print("Starting open:")
    for i in open:
        print("\n",i[1].printState())
