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
    #print(graph,'\nPers:',persistence)
    # printBayesNetwork(graph,2)
    # print(enumerationAsk(graph,'V1 V2 4',[]))    
    evidence = []
    while True:
        print("Evidence: "+str(evidence))
        inp = input('Enter your choice: ')
        if inp == 'quit':
            break
        elif inp == 'reset':
            evidence=[]
        elif inp[:3] == 'add':# "add V1 V2 3" => (1,2) is blocked at time 3,"add V1" -v1 has ppl, "add not V3","add not V1 V5 0" => (1,5) isnt blocked
            evidence.append(inp[4:])
        else:   #pr1 - all vertices has ppl; pr2 - all edges blocked;; pr3- certain path isnt blocked; pr4-;
            if inp[2] == '1':
                printVertices(graph,evidence)
            if inp[2] == '2':
                printEdges(graph,evidence,int(inp.split()[1]))


#maybe need to add normalization
def enumerationAsk(graph,q,e): #q = Vi  | q = Vi Vj
    time = q.split(' ')[2] if len(q.split(' '))>1 else 0
    return (enumerateAll(graph,constructVars(graph, int(time)),e + [q]),
                enumerateAll(graph,constructVars(graph, int(time)),e + ['not ' + q]))

def enumerateAll(graph,vars,e):
    if not vars:
        return 1.0
    y = vars[0]
    # print('ea('+str(vars)+','+str(e)+')')
    if y in e or 'not '+y in e:
        pIndex = 0 if y in e else 1
        # print('y:'+y+' in e')
        splited = y.split(' ')
        if len(splited) == 1 :
            p = calcP(graph, splited[0], '', 0, parents(y), False)[pIndex]
            # print(str(p)+' * EnumAll('+str(vars[1:])+','+str(e)+')')
            s = p * enumerateAll(graph,vars[1:],e)
            # print(s)
            return s

        p = calcP(graph, splited[0],splited[1],int(splited[2]),parents(y),True)[pIndex]
        # print(str(p)+' * EnumAll('+str(vars[1:])+','+str(e)+')')
        s1 = calcP(graph, splited[0],splited[1],int(splited[2]),parents(y),True)[pIndex] * enumerateAll(graph,vars[1:],e)
        # print(s1)
        return s1
    else:
        # print('y:'+y+' not in e')
        splited = y.split(' ')
        if len(splited) == 1 :
            p1 = calcP(graph, splited[0], '', 0, parents(y), False)[0]
            p2 = calcP(graph, splited[0], '', 0, parents(y), False)[1]
            # print(str(p1)+' * EnumAll('+str(vars[1:])+','+str(e+[y])+')')
            # print(str(p2)+' * EnumAll('+str(vars[1:])+','+str(e+['not '+y])+')')
            s1 = (calcP(graph, splited[0], '', 0, parents(y), False)[0] * enumerateAll(graph,vars[1:],e+[y])+
                    calcP(graph, splited[0], '', 0, parents(y), False)[1] * enumerateAll(graph,vars[1:],e+['not '+y]))
            # print(s1)
            return s1
        p1 = calcP(graph, splited[0],splited[1],int(splited[2]),parents(y),True)[0]
        p2 = calcP(graph, splited[0],splited[1],int(splited[2]),parents(y),True)[1]
        # print(str(p1)+' * EnumAll('+str(vars[1:])+','+str(e+[y])+')')
        # print(str(p2)+' * EnumAll('+str(vars[1:])+','+str(e+['not '+y])+')')

        s1 = (calcP(graph, splited[0],splited[1],int(splited[2]),parents(y),True)[0] * enumerateAll(graph,vars[1:],e+[y])+
                calcP(graph, splited[0],splited[1],int(splited[2]),parents(y),True)[1] * enumerateAll(graph,vars[1:],e+['not '+y]))
        # print(s1)
        return s1
    


def parents(query):
    q = query.split(' ')
    if len(q) == 1:
        return []
    elif q[2] == '0':
        return [q[0],q[1]]
    else:
        return [q[0]+ ' ' + q[1] + ' ' + str(int(q[2])-1)] 

def constructVars(graph,t):
    vars = []
    tn = 0
    for key in (list(graph.keys())):
        if key != 'Edges':
            vars.append(key)
        else:
            while(tn<=t):
                for e in graph['Edges']:
                    vars.append(e['from'] +' '+e['to'] + ' '+ str(tn))
                tn += 1
    return vars

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
            return (persistence,1-persistence) if not (len(evidence[0]) > 3 and evidence[0][:3] == 'not') else (0.001,0.999)

def printVertices(graph,evidence):
    for i in range(len(graph)-1):
        print('VERTEX',str(i+1)+':')
        if list(graph.keys())[i] not in evidence and 'not '+list(graph.keys())[i] not in evidence:
            (p,notP) = calcP(graph,list(graph.keys())[i],'',0,[],False)
        else:
            (p,notP) = (1.0,0.0) if list(graph.keys())[i] in evidence else (0.0,1.0)
        print('\tP(Evacuees {0})={1}\n\tP(not Evacuees {0})={2}'.format(i+1,p,notP))

def printEdges(graph,evidence,time):
    for e in graph['Edges']:
        q = e['from']+' '+e['to']+" " +str(time)
        if q not in evidence and 'not '+q not in evidence:
            (p,notP) = enumerationAsk(graph,q,evidence)
        else:
            (p,notP) = (1.0,0.0) if q in evidence else (0.0,1.0)
        print('P(Blocakge {0},{1}) ={2}'.format(e['e'],time,p))
                 

def printBayesNetwork(graph,timeLimit):
    for i in range(len(graph)-1):
        print('VERTEX',str(i+1)+':')
        (p,notP) = calcP(graph,list(graph.keys())[i],'',0,[],False)
        print('\tP(Evacuees {0})={1}\n\tP(not Evacuees {0})={2}'.format(i+1,p,notP))
    for i in range(timeLimit):
        for e in graph['Edges']:
            print('EDGE',str(e['e'])+',','time',i)
            if i == 0:
                print('P(Blocakge {0}| not Evacuees {1}, not Evacuees {2}) ={3}'.format(e['e'],e['from'],e['to'],
                    calcP(graph,e['from'],e['to'],i,['not '+e['from'],'not '+e['to']],True)[0]))
                print('P(Blocakge {0}| Evacuees {1}, not Evacuees {2}) ={3}'.format(e['e'],e['from'],e['to'],
                    calcP(graph,e['from'],e['to'],i,[e['from'],'not '+e['to']],True)[0]))
                print('P(Blocakge {0}| not Evacuees {1}, Evacuees {2}) ={3}'.format(e['e'],e['from'],e['to'],
                    calcP(graph,e['from'],e['to'],i,['not '+e['from'],e['to']],True)[0]))
                print('P(Blocakge {0}| Evacuees {1}, Evacuees {2}) ={3}'.format(e['e'],e['from'],e['to'],
                    calcP(graph,e['from'],e['to'],i,[e['from'],e['to']],True)[0]))
                
            else:
                print('P(B({0},{1})| B({0},{2}))={3}'.format(e['e'],i,i-1,
                    calcP(graph,e['from'],e['to'],i,[e['from']+" "+e['to']+" "+str(i-1)],True)[0]))
                print('P(B({0},{1})| not B({0},{2}))={3}'.format(e['e'],i,i-1,
                    calcP(graph,e['from'],e['to'],i,["not "+e['from']+" "+e['to']+" "+str(i-1)],True)[0]))
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