import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
import random

def Normalize(p):
    total=0
    prob=[]
    for x in p: total+=x
    for i in range(len(p)): prob.append(p[i]/total)
    print(prob)
    return(prob)
    
similar = 0.5  #percentage of similar neighbors required for satisfaction
empty = 0.1    #chance of an empty element

#the number of groups is defined by the following probability list
# [0.3, 0.4, 0.3] will run the program for 3 groups (respective probabilities)
probabilities=[0.25,0.25,0.25,0.25]
num_group=len(probabilities)
probabilities=Normalize(probabilities)  #avoid problems with probabilities input


class Board:
    def __init__(self, size):
        self.s = size           # size of region
        self.n = num_group      # number of groups
        self.emtpy = empty      # chance of having an empty space
        ##
        self.prob = [empty]     #list assigning a probability to each group
        for p in probabilities: #prob[0] = probability of 'empty'
            self.prob.append(p) #prob[i] = probability of 'Group i' 
        ##
        self.r = np.zeros(shape=(size+2, size+2))  # define the region
        self.satisfiedPerc = 0

        for i in range(0, self.s+2):  # define a larger region
            for j in range(0, self.s+2):
                # only iterate the inner region
                if i in range(1, self.s + 1) and j in range(1, self.s + 1):
                    # in case it is not empty, decide group
                    if np.random.random() > empty:
                        ##  attribute to each non-empty slot a group element
                        r_nb=npr.random()
                        k=0
                        while(r_nb>0): #substract each prob to determine its interval
                            k+=1 #take care with prob[] index, prob[0]=empty
                            r_nb-=self.prob[k]
                        self.r[i][j] = float(k)
                        ##
                    else:
                        self.r[i][j] = 0
                else:           # else gives 0 for empty
                    self.r[i][j] = 0

    def iterate(self):
        # for every list: list[0] means nothing, list[i] = information for 'Group i'
        uS_C = [0]              # unsatisfied counter for each group
        eGroup=[0]              # coordinates of each group's unsatisfied elements 
        for i in range(1,num_group+1): #declares the object shape of uS_C and eGroup
            uS_C.append(0)
            eGroup.append([])   
        eS = []                 # empty slots
        # find all the non-satisfied agents
        for i in range(1, self.s+1):  # iterate over all non-boundary points
            for j in range(1, self.s+1):
                if self.r[i][j] == 0:
                    eS.append([i, j])  # append to empty slots
                else: #if the element is not empty
                    simi_C = 0  # counter for similar agents
                    # all the neighbours
                    neighbours = [self.r[i-1][j-1],
                                  self.r[i-1][j],
                                  self.r[i-1][j+1],
                                  self.r[i][j-1],
                                  self.r[i][j+1],
                                  self.r[i+1][j-1],
                                  self.r[i+1][j],
                                  self.r[i+1][j+1]]

                    for n in range(len(neighbours)):
                        if neighbours[n] == self.r[i][j]:
                            # count the number of similar neighbours
                            simi_C += 1
                    if simi_C/8 < similar:  #if agent is unsatisfied
                        uS_C[int(self.r[i][j])] += 1
                        eGroup[int(self.r[i][j])].append([i, j])
                        
        TotalUnsatisfied=0
        for l in uS_C: TotalUnsatisfied+=l 
        self.satisfiedPerc = 1 - TotalUnsatisfied/(self.s**2)
        print('Satisfaction: ', self.satisfiedPerc)
        
        
        if len(eS) > TotalUnsatisfied:  # in case there are more empty slots than unsatisfied agents
                                        # randomly assigned the moved agents to available slots
            eS = random.sample(eS, TotalUnsatisfied)  #TotalUnsat # of empty slots
            agent_empty=[0]               #agent_empty assigns the correct number of empty slots coordinates that`ll be filled by each group 
            random.shuffle(eS)            #shuffle the empty coordinates list
            for i in range(1,num_group+1):          #for every group
                agent_empty.append([])              #declares another group information on angent_empty
                for j in range(uS_C[i]):            #for every unsatisfied agent of the group
                    agent_empty[i].append(eS.pop()) #assign a random empty slot and removes it from the empty list
                for e in agent_empty[i]:            #assigns an agent of the group i to the empty slots
                    self.r[e[0]][e[1]] = float(i)
                for e in eGroup[i]:                 #sets as 'empty' the previous slots occupied by the agents
                    self.r[e[0]][e[1]] = float(0)
                   

                
        else:                   # more unsatisfied agents than empty slots
            quota=[0]           #number of unsatisfied agents that will move from each group
            agent_empty=[0]     #the reserved empty slots that will be occupied
            agent_selected=[0]  #the selected agents that will move
            random.shuffle(eS)  #shuffle the list of empty slots
            for i in range(1,num_group+1):
                random.shuffle(eGroup[i])   #shuffles the list of unsatisfied agents of 'Group i'
                quota.append(int(round(uS_C[i]/TotalUnsatisfied * len(eS))))  #the number of each group's moved agents is proportinal to the amount of unsatisfied agents
                agent_empty.append([])
                agent_selected.append([])
                for j in range(quota[i]):                       #for every unsatisfied agent that will move from group i
                    agent_empty[i].append(eS.pop())             #assigns a random empty slot (it's shuffled) and remove it from the empty list
                    agent_selected[i].append(eGroup[i].pop())   #assings a random chosen unsatisfied agent from group i and remove it from the list

                for e in agent_empty[i]:            #assigns an agent of the group i to the empty slots
                    self.r[e[0]][e[1]] = float(i)
                for e in agent_selected[i]:         #sets as 'empty' the previous slots occupied by the agents
                    self.r[e[0]][e[1]] = float(0)


board = Board(size=100,)
plt.imshow(board.r)

plt.savefig("start.png")

count=0
max_iterations=200
while board.satisfiedPerc < 0.95 and count<max_iterations:
    board.iterate()
    count+=1

plt.imshow(board.r)

plt.savefig("end.png")
plt.close()

print("End\n")
