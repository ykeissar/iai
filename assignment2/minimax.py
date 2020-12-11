from heuristic import minimaxHeur

global trace_id
trace_id=0

def minmax(problem,h,vA,vB,cutoff):
    global trace_id
    currNodes = [Node(trace_id,vA,vB,None,True)]
    root = currNodes[0]
    trace_id +=1

    while cutoff > 0:
        nextNodes = []
        for node in currNodes:
            adjecList = getAdjec(problem,node.myVertex if node.myTurn else node.otherVertex)
            for adj in adjecList:
                if node.myTurn:
                    nt = Node(trace_id,adj,node.otherVertex,node,not node.myTurn)
                    node.sons.append(nt)
                    nextNodes.append(nt)
                else:
                    nt = Node(trace_id,node.myVertex,adj,node,not node.myTurn)
                    node.sons.append(nt)
                    nextNodes.append(nt)
                trace_id +=1
            
        currNodes = nextNodes
        # printNodes(currNodes)
        cutoff -= 1
    
    
    dfs(root,problem,2)
    # print(len(currNodes))
    # for i in currNodes:
    #     print('#####################')
    #     print(i,minimaxHeur(graph,i))
    #     print('$$$$$$$')



    
class Node:
    def __init__(self, stateId, myVertex, otherVertex, prevNode, myTurn):
        self.stateId = stateId
        self.myVertex = myVertex
        self.otherVertex = otherVertex
        self.prevNode = prevNode
        self.myTurn = myTurn
        self.scores = (0,0)
        self.sons = []
        self.color = 'white'
    
    def __repr__(self):
        return "[---({0},{1})---[myVertex: {0}, otherVertex: {1}, prevNode:({2},{3}), myTurn:{4}, score:{5}]]".format(
            self.myVertex,self.otherVertex,self.prevNode.myVertex, self.prevNode.otherVertex, self.myTurn, self.scores
        ) if self.prevNode != None else "[[myVertex: {0}, otherVertex: {1}, prevNode:(None), myTurn:{2}, score:{3}]]".format(
            self.myVertex,self.otherVertex,self.myTurn, self.scores
        )

    def __gt__(self,other):
        self

def getAdjec(graph,vertex):
    return list(map(lambda x: x['v'],graph[vertex]['e']))

def printNodes(nodes):
    for i in nodes:
        print(i,'\n')

def main():
    graph = {'V1': {'p': 0, 'e': [{'v': 'V2', 'w': 1}, {'v': 'V7', 'w': 1}]}, 'V2': {'p': 0, 'e': [{'v': 'V1', 'w': 1}, {'v': 'V5', 'w': 1}]}, 'V3': {'p': 2, 'e': [{'v': 'V4', 'w': 1}, {'v': 'V6', 'w': 1}]}, 'V4': {'p': 0, 'e': [{'v': 'V5', 'w': 1}, {'v': 'V3', 'w': 1}]}, 'V5': {'p': 2, 'e': [{'v': 'V4', 'w': 1}, {'v': 'V2', 'w': 1}]}, 'V6': {'p': 0, 'e': [{'v': 'V3', 'w': 1}, {'v': 'V7', 'w': 1}]}, 'V7': {'p': 0, 'e': [{'v': 'V6', 'w': 1}, {'v': 'V1', 'w': 1}]}}
    #graph = {'V1': {'p': 0, 'e': [{'v': 'V2', 'w': 1}, {'v': 'V3', 'w': 4}]}, 'V2': {'p': 1, 'e': [{'v': 'V1', 'w': 1}, {'v': 'V5', 'w': 2}]}, 'V3': {'p': 2, 'e': [{'v': 'V1', 'w': 4}, {'v': 'V4', 'w': 8}]}, 'V4': {'p': 0, 'e': [{'v': 'V3', 'w': 8}, {'v': 'V5', 'w': 1}]}, 'V5': {'p': 0, 'e': [{'v': 'V4', 'w': 1}, {'v': 'V2', 'w': 2}, {'v': 'V6', 'w': 7}]}, 'V6': {'p': 3, 'e': [{'v': 'V5', 'w': 7}]}}

    minmax(graph,None,'V1','V4',4)
    
def dfs(node,graph,typeOfGame):
    if node.sons == []:
        node.scores = minimaxHeur(graph,node)
        print('leaf: ',node)
    else:
        for i in node.sons:
            dfs(i,graph,typeOfGame)
        if typeOfGame ==  1: #TODO add pruning
            minmaxScores = node.sons[0].scores
            for j in range(1,len(node.sons)):
                if node.myTurn:
                    if node.sons[j].scores[0] - node.sons[j].scores[1] > minmaxScores[0] - minmaxScores[1]:
                        minmaxScores = node.sons[j].scores
                else:
                    if node.sons[j].scores[1] - node.sons[j].scores[0] > minmaxScores[1] - minmaxScores[0]:
                        minmaxScores = node.sons[j].scores
            node.scores = minmaxScores
            print('\n',node)

        elif typeOfGame ==  2:
            minmaxScores = node.sons[0].scores
            for j in range(1,len(node.sons)):
                if node.myTurn:
                    if node.sons[j].scores[0] > minmaxScores[0]:
                        minmaxScores=node.sons[j].scores
                    elif node.sons[j].scores[0] == minmaxScores[0]:
                        if node.sons[j].scores[1] > minmaxScores[1]:
                            minmaxScores=node.sons[j].scores
                        # node.sons[j].scores[0] == minmaxScores[0]
                else:
                    if node.sons[j].scores[1] < minmaxScores[1]:
                        minmaxScores=node.sons[j].scores
                    elif node.sons[j].scores[1] == minmaxScores[1]:
                        if node.sons[j].scores[0] > minmaxScores[0]:
                            minmaxScores=node.sons[j].scores
            node.scores = minmaxScores
            print(node)

        else:
            minmaxScores = node.sons[0].scores
            for j in range(1,len(node.sons)):
                if node.sons[j].scores[0] + node.sons[j].scores[1] > minmaxScores[0] + minmaxScores[1]:
                    minmaxScores = node.sons[j].scores
            node.scores = minmaxScores   
            print(node)

if __name__ == "__main__":
    main()