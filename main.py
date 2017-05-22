import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
import random


similar = 0.5
chance = 0.5
empty = 0.1


class Board:
    def __init__(self, size, chance=0.5, num_group=2, empty=0.1):
        self.s = size           # size of region
        self.c = chance         # chance of falling into either group
        self.n = num_group      # number of groups
        self.emtpy = empty      # chance of having empty space
        self.r = np.zeros(shape=(size+2, size+2))  # define the region
        self.satisfiedPerc = 0

        for i in range(0, self.s+2):  # define a larger region
            for j in range(0, self.s+2):
                # only iterate the inner region
                if i in range(1, self.s + 1) and j in range(1, self.s + 1):
                    # in case it is not empty, decide group
                    if np.random.random() > empty:
                        self.r[i][j] = 2 if (npr.random() > chance) else 1
                    else:
                        self.r[i][j] = 0
                else:           # else give 0 for empty
                    self.r[i][j] = 0

    def iterate(self):
        uS_C = [0, 0]           # unsatisfied counter
        eS = []                 # empty slots
        eA = []                 # empty A
        eB = []                 # empty B
        # find all the non-satisfied agents
        for i in range(1, self.s+1):  # iterate over all non-boundary points
            for j in range(1, self.s+1):
                if self.r[i][j] == 0:
                    eS.append([i, j])  # append to empty slots
                else:
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

                    for n in range(0, len(neighbours)):
                        if neighbours[n] == self.r[i][j]:
                            # count the number of similar neighbours
                            simi_C += 1
                    if simi_C/8 < similar:
                        # print("Unsatisfied: [%i, %i] \n"% (i,j))
                        # decide whether satisfied
                        if self.r[i][j] == 1:
                            uS_C[0] += 1
                            eA.append([i, j])  # empty A
                        if self.r[i][j] == 2:
                            uS_C[1] += 1
                            eB.append([i, j])  # empty B
        self.satisfiedPerc = 1 - (uS_C[0] + uS_C[1])/(self.s**2)
        print(self.satisfiedPerc)

        # in caes there are more empty slots than unsatisfied agents
        if len(eS) > uS_C[0] + uS_C[1]:
            # randomly assigned the moved agents to available slots
            eS = random.sample(eS, uS_C[0] + uS_C[1])  # narrow down
            agent_A_slots = random.sample(eS, uS_C[0])
            for e in agent_A_slots:
                self.r[e[0]][e[1]] = 1
            for e in eS:    # empty slots
                if self.r[e[0]][e[1]] != 1:  # if not assigned 1
                    self.r[e[0]][e[1]] = 2   # assign 2
            for e in eA:                     # make the origins empty
                self.r[e[0]][e[1]] = 0
            for e in eB:
                self.r[e[0]][e[1]] = 0
        else:                   # more unsatisfied agents than empty slots
            A_quota = int(round(uS_C[0]/(uS_C[0] + uS_C[1]) * len(eS)))
            B_quota = len(eS) - A_quota
            agent_A_slots = random.sample(eS, A_quota)
            # assign some A to empty slots
            for e in agent_A_slots:
                self.r[e[0]][e[1]] = 1
            # sample some A to move out
            agent_A_moved = random.sample(eA, A_quota)
            for e in agent_A_moved:
                self.r[e[0]][e[1]] = 0
            # for empty slots, if not occupied by A, assign B
            for e in eS:
                if self.r[e[0]][e[1]] != 1:
                    self.r[e[0]][e[1]] = 2
            # sample some B to move out
            agent_B_moved = random.sample(eB, B_quota)
            for e in agent_B_moved:
                self.r[e[0]][e[1]] = 0


board = Board(size=100)
plt.imshow(board.r)

plt.savefig("start.png")

while board.satisfiedPerc < 1:
    board.iterate()

plt.imshow(board.r)

plt.savefig("end.png")
plt.close()

print("End\n")
