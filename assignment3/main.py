import sys
from Agents import Agent, saboAct
from graphTools import getAbstract

global persistence
persistence = 0

def main():
    global persistence
    f = open("params.txt", "r")
    flines = list(map(lambda x: x.replace('\n','').split(),f.readlines()))
    n = int(flines[0][1])
    graph = {}
    j=2
    for i in range(2,2+n):
        ppl = float(flines[i][1]) if len(flines[i])>1 else 0.0
        graph[flines[i][0][1:]] = {
                "p": ppl,
                "e":[]
            }
        j = j+1
    graph['Edges'] = []
    for i in range(j+1,len(flines)-2):
        v1 = "V"+flines[i][1] 
        v2 = "V"+flines[i][2]
        w = int(flines[i][3][1:])
        graph[v1]["e"].append({
                "v":v2,
                "w":w,
            }
        )
        graph[v2]["e"].append({
                    "v":v1,
                    "w":w,
                }
        )
        graph['Edges'].append({
            "e": i-j,
            "from": v1,
            "to": v2
        })


    persistence = float(flines[-1][1])
    print(graph,'\nPers:',persistence)
    printBayesNetwork(graph,1)

# query: "V1", "V2", 
# evidence: ["V1","not V2"]
# return: (P(query|evidence),P(~query|evidence))
# P("V1 V2 t+1"|"V1 V2 t") or P("V1 V2 t+1"|"not V1 V2 t"))
def calcP(graph,query1,query2,time,evidence,isEdge):
    if not isEdge:
        return (graph[query1]['p'],1-graph[query1]['p'])
    else:
        if time == 0:
            evidence1 = not (len(evidence[0]) > 3 and evidence[0][:3] == 'not')
            evidence2 = not (len(evidence[1]) > 3 and evidence[1][:3] == 'not')
            if not evidence1 and not evidence2:
                return (0.001,0.999)
            elif evidence1 and evidence2:
                p = calcP(graph,query1,query2,0,["not "+evidence[0],evidence[1]],True)[1]
                return (1-(round(p**2,12)),round(p**2,12))
            else:
                return round(0.6/getEdgeWeight(graph,query1,query2),15),1-(round(0.6/getEdgeWeight(graph,query1,query2),15))                   
        else:
            return persistence if not (len(evidence[0]) > 3 and evidence[0][:3] == 'not') else 0.001
     
def printBayesNetwork(graph,timeLimit):
    for i in range(len(graph)-1):
        print('VERTEX',str(i+1)+':')
        (p,notP) = calcP(graph,list(graph.keys())[i],'',0,[],False)
        print('\tP(Evacuees {0})={1}\n\tP(not Evacuees {0})={2}'.format(i+1,p,notP))
    for i in range(timeLimit):
        for e in graph['Edges']:
            if i == 0:
                print('P(Blocakge {0}| not Evacuees {1}, not Evacuees {2}) ={3}'.format(e['e'],e['from'],e['to'],
                    calcP(graph,e['from'],e['to'],i,['not '+e['from'],'not '+e['to']],True)[0]))
                print('P(Blocakge {0}| Evacuees {1}, not Evacuees {2}) ={3}'.format(e['e'],e['from'],e['to'],
                    calcP(graph,e['from'],e['to'],i,[e['from'],'not '+e['to']],True)[0]))
                print('P(Blocakge {0}| not Evacuees {1}, Evacuees {2}) ={3}'.format(e['e'],e['from'],e['to'],
                    calcP(graph,e['from'],e['to'],i,['not '+e['from'],e['to']],True)[0]))
                print('P(Blocakge {0}| Evacuees {1}, Evacuees {2}) ={3}'.format(e['e'],e['from'],e['to'],
                    calcP(graph,e['from'],e['to'],i,[e['from'],e['to']],True)[0]))
                print('\n')
#                  P(Blocakge 1 | not Evacuees 1, not Evacuees 2) = 0.001
#   P(Blocakge 1 | Evacuees 1, not Evacuees 2) = 0.6
#   P(Blocakge 1 | not Evacuees 1, Evacuees 2) = 0.6
#   P(Blocakge 1 | Evacuees 1, Evacuees 2) = 0.84


    
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
    elif agent.type[0] == 'm':
        return agent.minimaxStep(graph)
    else:
        return agent.getAstarStep(graph)
    return None

if __name__ == "__main__":
    main()