import numpy as np

similar = 0.3
chance = 0.5
empty = 0.1


class Agent:
    def __init__(self, similar, chance):
        self.group = "a" if (np.random.random() > chance) else "b"

    def checkSimilarity(self):
