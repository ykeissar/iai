import sys
from Agents import Agent, saboAct
from graphTools import getAbstract

global blocked
global L
L = 5

def main():
    f = open("parameters2.txt", "r")
    flines = list(map(lambda x: x.replace('\n','').split(),f.readlines()))
    n = int(flines[0][1])
    deadLine = float(flines[1][1])
    cDeadLine = deadLine
    graph = {}
    j=2
    totalNumOfPpl = 0
    for i in range(2,2+n):
        ppl = int(flines[i][1][1:]) if len(flines[i])>1 else 0
        graph[flines[i][0][1:]] = {
                "p": ppl,
                "e":[]
            }
        j = j+1
        totalNumOfPpl += ppl
    for i in range(j+1,len(flines)):
        v1 = "V"+flines[i][1] 
        v2 = "V"+flines[i][2]
        w = int(flines[i][3][1:])
        graph[v1]["e"].append({
                "v":v2,
                "w":w,
                "blocked":False
            }
        )
        graph[v2]["e"].append({
                    "v":v1,
                    "w":w,
                    "blocked":False
                }
        )
    
    print("please enter number of agents:")
    num_of_agents = int(input())
    print ("please enter agents details: ")
    agents_details = input().split(',')
    agentDetails = list(map(lambda x: x.split(' '), agents_details))
        
    agentsList = list()
    for i in range(0,num_of_agents):
        agentsList.append(Agent(agentDetails[i][0], agentDetails[i][1],len(graph),L))
    # main loop
    print("Agents: \n",agentsList)
    print("Graph: \n",graph)
    while deadLine>0 and totalNumOfPpl>0 and not allTerminated(agentsList):
        for i in agentsList:
            if i.terminated:
                continue
            elif i.stepsLeft > 0:
                i.stepsLeft -= 1
            elif i.calcTime > 0:
                i.calcTime -= 1
            elif i.type == 's':
                saboAct(i,graph)
            else:
			    # we reached vertice, evacuating ppl
                verPpl = graph[i.currentPosition]["p"]
                totalNumOfPpl -= verPpl
                i.peopleEvacuated += verPpl
                graph[i.currentPosition]["p"] = 0
                if totalNumOfPpl == 0:
                    break
                #finding next vertice to travel
                prevVer = i.currentPosition
                i.currentPosition = getNextStep(i,graph)
                print("Next step: ",i.currentPosition)
                if not i.currentPosition:
                    i.terminated = True
                else:
                    i.stepsLeft = getEdgeWeight(graph,prevVer,i.currentPosition)
                i.numOfActions +=1
        deadLine -= 1
    feedback = "Well Done!!! Agent: "
    if agentsList[0].peopleEvacuated == 0:
        feedback = "Too Bad.. You could've done better, "
    print(feedback, agentsList[0].type,"\nevacuated ",agentsList[0].peopleEvacuated," people! And it took ",cDeadLine-deadLine," rounds.")

def allTerminated(agentsList):
    for i in agentsList:
    	if not i.terminated:
    		return False	
    return True	

def getEdgeWeight(graph,v1,v2):
    for e in graph[v1]['e']:
        if e['v'] == v2:
            return e['w']
    return -1

def getNextStep(agent,graph):
    if agent.type == 'h':
        return agent.humanStep(graph)
    elif agent.type == 'g':
        return agent.greedyStep(graph)
    else:
        return agent.getAstarStep(graph)
    return None

if __name__ == "__main__":
    main()