from Agents import Agent
def main():
	f = open("parameters2.txt", "r")
	flines = list(map(lambda x: x.replace('\n','').split(),f.readlines()))
	n = int(flines[0][1])
	deadLine = float(flines[1][1])

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
	print("please enter number of agents: ")
	num_of_agents = 1 #int(input())
	print ("please enter agents details: ")  #list of size numOfAgents of lists of 2 items [type of agent, initial position]
	agents_details =["g V1"] #input().split(',')
	agentDetails = list(map(lambda x: x.split(' '), agents_details))

	agentsList = list()
	for i in range(0,num_of_agents):
		agentsList.append(Agent(agentDetails[i][0], agentDetails[i][1],len(graph)))

	# main loop
	while deadLine>0 and totalNumOfPpl>0 and not allTerminated(agentsList):
		for i in agentsList:
			print(i)
			if i.terminated:
				continue
			if i.type == 's':
				if i.waiting == 0:
					prevVer = i.currentPosition
					i.currentPosition = i.getNextStep(graph)
					if not i.currentPosition:
						i.terminated = True
				else:
					i.waiting -= 1

			elif i.stepsLeft > 0:
				i.stepsLeft -= 1
			else:
				# we reached vertice, evacuating ppl
				verPpl = graph[i.currentPosition]["p"]
				totalNumOfPpl -= verPpl
				i.peopleEvacuated += verPpl
				graph[i.currentPosition]["p"] = 0

				#finding next vertice to travel
				prevVer = i.currentPosition
				i.currentPosition = i.getNextStep(graph)
				if not i.currentPosition:
					i.terminated = True
				else:
					i.stepsLeft = getEdgeWeight(graph,prevVer,i.currentPosition)
			i.numOfActions +=1
		deadLine -= 1
				

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

if __name__ == "__main__":
    main()