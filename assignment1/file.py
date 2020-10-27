from Agents import Agent
def main():
	f = open("parameters.txt", "r")
	flines = list(map(lambda x: x.replace('\n','').split(),f.readlines()))
	n = int(flines[0][1])
	dead_line = float(flines[1][1])

	agentsList = {}
	graph = {}
	# 	"V1":{"p":1,"e":[{"v":,"w":}]}
	# 	"V2":
	# 	"V3":3
	# }
	j=2
	totalNumOfPpl = 0
	for i in range(2,2+n):
		ppl = int(flines[i][1][1:]) if len(flines[i])>1 else 0
		graph[flines[i][0][1:]] = {
				"p": ppl ,
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
				"w":w
			}
		)
		graph[v2]["e"].append({
					"v":v1,
					"w":w
				}
		)
	print("please enter number of agents: ")
	num_of_agents = int(input())
	print ("please enter agents details: ")  #list of size numOfAgents of lists of 2 items [type of agent, initial position]
	agents_details = (input()).split(',')
	agentDetails = list(map(lambda x: x.split(' '), agents_details))
	#print(agentDetails)
	#print(graph)

	for i in range(0,num_of_agents):
		agentsList[i] = Agent(agentDetails[i][0], agentDetails[i][1])

	while dead_line>0 and totalNumOfPpl>0 and not allTerminated(agentsList):
		for i in agentsList:
			if (agentsList[i].stepsLeft)>0:
				agentsList[i].stepsLeft -= 1
			else:
				verPpl= graph[agentsList[i].currentPosition]["p"]
				totalNumOfPpl -= verPpl
				agentsList[i].peopleEvacuated += verPpl
				prevVer = agentsList[i].currentPosition
				agentsList[i].currentPosition = agentsList[i].getNextStep(graph)
				agentsList[i].stepsLeft = getEdgeWeight(graph,prevVer,agentsList[i].currentPosition)
			agentsList[i].numOfActions +=1	

def allTerminated(agentsList):
    for i in agentsList:
    	if not agentsList[i].terminated:
    		return False		
def getEdgeWeight(graph,v1,v2):
    for e in graph[v1]['e']:
    	if e['v'] is v2:
    		return e['w']

if __name__ == "__main__":
    main()