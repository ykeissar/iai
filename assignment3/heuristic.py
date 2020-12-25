from collections import defaultdict
from graphTools import getEdgeWeigh

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
    
def minimaxHeur(graph,node):
    sumA=0
    sumB=0
    myPath,otherPath, plyfirst = getPaths(node)
    # print('Paths: ',myPath,otherPath)
    for i,val in enumerate(myPath):
        if val not in myPath[:i]:
            if val not in otherPath:
                sumA += graph[val]['p']
            else:
                if calcPath(otherPath, val, graph) > calcPath(myPath, val, graph):
                    sumA += graph[val]['p']
                elif calcPath(otherPath, val, graph) < calcPath(myPath, val, graph):
                    sumB += graph[val]['p']
                else:
                    if plyfirst:
                        sumA += graph[val]['p']
                    else:
                        sumB += graph[val]['p']
            # print('Aval: ',val,'Asum: ',sumA)
       
    for i,val in enumerate(otherPath):
        if val not in otherPath[:i] and val not in myPath:
            sumB += graph[val]['p']
            # print('Bval: ',val,'Bsum: ',sumB)
    # print(sumA,sumB)
    return sumA, sumB

def calcPath(path, val, graph):
    sum = 0
    for i in range(len(path)-1):
        sum += getEdgeWeigh(graph,path[i],path[i+1])
        if path[i+1] == val:
            break
    return sum

graph = {'V1': {'p': 0, 'e': [{'v': 'V2', 'w': 1}, {'v': 'V3', 'w': 4}]}, 'V2': {'p': 1, 'e': [{'v': 'V1', 'w': 1}, {'v': 'V5', 'w': 2}]}, 'V3': {'p': 2, 'e': [{'v': 'V1', 'w': 4}, {'v': 'V4', 'w': 8}]}, 'V4': {'p': 0, 'e': [{'v': 'V3', 'w': 8}, {'v': 'V5', 'w': 1}]}, 'V5': {'p': 0, 'e': [{'v': 'V4', 'w': 1}, {'v': 'V2', 'w': 2}, {'v': 'V6', 'w': 7}]}, 'V6': {'p': 3, 'e': [{'v': 'V5', 'w': 7}]}}

def heur(graph,n):
    _,sum = completeSpanningTree(graph,n.vertex,n.visited)
    return sum 


def getPaths(node):
    myPath = []
    otherPath = []
    while node != None:
        # print(node)
        # print("Before - my: ",myPath,'other: ',otherPath)
        if node.prevNode == None:
            myPath.insert(0,node.myVertex)
            otherPath.insert(0,node.otherVertex)

        elif not node.myTurn:
            myPath.insert(0,node.myVertex)
        else:
            otherPath.insert(0,node.otherVertex)
            
        tempPrev = node
        node = node.prevNode
        # print("Afrer - my: ",myPath,'other: ',otherPath)
        
    return myPath,otherPath,tempPrev.myTurn

