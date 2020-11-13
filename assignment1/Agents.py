from graphTools import dijkstra,getPath,astar,getAbstract
from heuristic import heur
import sys
class Agent:
    def __init__(self,type, currentPosition, waiting,limit):
        self.type = type
        self.currentPosition = currentPosition
        self.numOfActions = 0
        self.peopleEvacuated = 0
        self.stepsLeft = 0
        self.terminated = False
        self.waiting = waiting
        self.strategy = []
        self.limit = 10000 if type == "A*" else limit

    def traverse(self,dest):
        return 0
    def terminate(self):
        return 0
    def __repr__(self):
        return "type:{0},\n currentPosition: {1},\n numOfActions: {2},\n peopleEvacuated: {3},\n stepsLeft = {4},\n terminated ={5}\n wating ={6}\n strategy ={7}\n llimit={8}\n".format(
            self.type, self.currentPosition, self.numOfActions,self.peopleEvacuated, self.stepsLeft, self.terminated, self.waiting, self.strategy, self.limit)
    
    def humanStep(self,graph):
        print(graph)
        print(self)
        return input("Enter Node to travel: ")
    
    def greedyStep(self,graph):
        distList,p = dijkstra(graph,self.currentPosition)
        distList = {k: v for k,v in sorted(distList.items(), key= lambda item: item[1])}
        
        filteredDict = {}
        for k,v in distList.items():
            if graph[k]['p'] > 0 and k!=self.currentPosition:
                filteredDict[k] = v
        
        dest = list(filteredDict)[0]
        print(dest)
        if len(getPath(p,self.currentPosition,dest)) > 0:
            return getPath(p,self.currentPosition,dest)[1]  
        else: 
            return ""

    def getAstarStep(self, graph):# ["v1","v2"]
        if len(self.strategy) < 2:
            absStrag = astar(getAbstract(graph,self.currentPosition),heur,self.currentPosition,self.limit, self.type is not'greedy')
            self.strategy = deAbstractPath(graph,absStrag)
            if len(self.strategy) < 2:
                return ""
            if self.type == 'rta':
                ret = self.strategy[1]
                self.strategy = []
                return ret
        self.strategy = self.strategy[1:]
        return self.strategy[0] 

def deAbstractPath(graph,absPath):
    strategy = [absPath[0]]
    for i in range(len(absPath)-1):
        distList,p = dijkstra(graph,absPath[i])
        distList = {k: v for k,v in sorted(distList.items(), key= lambda item: item[1])}

        if len(getPath(p,absPath[i],absPath[i+1])) > 0:
            strategy = strategy + getPath(p,absPath[i],absPath[i+1])[1:] 
        else:
            return []

    return strategy