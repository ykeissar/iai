from graphTools import dijkstra,getPath
import sys
class Agent:
    def __init__(self,type, currentPosition, waiting):
        self.type = type
        self.currentPosition = currentPosition
        self.numOfActions = 0
        self.peopleEvacuated = 0
        self.stepsLeft = 0
        self.terminated = False
        self.waiting = waiting

    def traverse(self,dest):
        return 0
    def terminate(self):
        return 0
    def __repr__(self):
        return "type:{0},\n currentPosition: {1},\n numOfActions: {2},\n peopleEvacuated: {3},\n stepsLeft = {4},\n terminated ={5}\n wating ={6}\n".format(
            self.type, self.currentPosition, self.numOfActions,self.peopleEvacuated, self.stepsLeft, self.terminated, self.waiting)
    
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

    