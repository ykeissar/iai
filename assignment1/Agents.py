class Agent:
    def __init__(self,type, currentPosition):
        self.type = type
        self.currentPosition = currentPosition
        self.numOfActions = 0
        self.peopleEvacuated = 0
        self.stepsLeft = 0
        self.terminated = False
    
    def getNextStep(self,graph):
        return 0
    def traverse(self,dest):
        return 0
    def terminate(self):
        return 0
    def __repr__(self):
        return "type:{0},\n currentPosition: {1},\n numOfAcitions: {2},\n peopleEvacuated: {3},\n stepsLeft = {4},\n terminated ={5}\n ".format(
            self.type, self.currentPosition, self.numOfActions,self.peopleEvacuated, self.stepsLeft, self.terminated)