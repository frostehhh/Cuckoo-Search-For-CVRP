from CVRP import CVRPInfo as CVRP
import operator as o
import math
import random
from scipy.stats import levy

class CuckooSearch:
    """
    For this implementation of Cuckoo Search for the CVRP, the given pseudocode will be followed:
    - Initialize randomly generated solutions
    - With fraction Pc (fraction of cuckoos to perform levy flights), randomly select a cuckoo to
      perform levy flights. If the new solution found is better than a randomly selected nest, 
      replace the randomly selected nest.
    - The worse Pa (fraction of nest to be abandoned) nests will be replaced with randomly generated solutions
    - Rank solutions
    - Keep best solutions
    """


    def __init__(self, CVRPInstance, numCuckoos = 15, Pa = 0.2, Pc = 0.6, generations = 5000, pdf_type = 'levy'):
        self.instance = CVRPInstance
        self.Pa = Pa
        self.Pc = Pc
        self.generations = generations
        self.pdf_type = pdf_type
        self.numCuckoos = numCuckoos
        self.nests = []
        random.seed()
        self.solveInstance()
        

    def solveInstance(self):
        for i in range(self.numCuckoos):
            sol = self.instance.create_random_solution() # Initialize Solution
            self.nests.append(sol)

        # sort nests by cost
        self.nests.sort(key = o.attrgetter('cost'))
        best_solution = self.nests[0]
        random.shuffle(self.nests)

        # Search, and Evaluate
        for i in range(math.floor(self.numCuckoos * self.Pc)):
            self.__performLevyFlights(self.nests[i])
            # Randomly select another nest to compare with, 
            # Is Fi > Fj? replace

    def __performLevyFlights(self, nest):
        # Generate random value x from levy 
        # According to randomly generated value, perform 2-opt x time or double-bridge

        # temporary random num gen
        r = random.random()
        
        twoOptIter = 0
        doubleBridgeIter = 0
        if r >= 0 and r <= 0.2:
            twoOptIter = 1
        elif r > 0.2 and r <= 0.4:
            twoOptIter = 2
        elif r > 0.4 and r <= 0.6:
            twoOptIter = 3
        elif r > 0.6 and r <= 0.8:
            twoOptIter = 4
        elif r > 0.8 and r <= 1.0:
            doubleBridgeIter = 1
        
        for i in range(twoOptIter):
            nest = self.__twoOptInter(nest)

        for i in range(doubleBridgeIter):
            nest = self.__doubleBridgeInter(nest)
        
        # validate nest
        # nest.
        # recalculate nest 

    def __twoOptInter(self, sol): 
        # takes solution as input
        # gets 2 routes randomly
        # Select random node from each
        # Swap nodes
        numRoutes = len(sol.routes) # sol.routes - list

        # Randomly select 2 routes to swap
        r1 = random.randrange(0,numRoutes)
        r2 = random.randrange(0,numRoutes)

        # Check if n2 == n1. If true, generate new value for n2.
        while r2 == r1: 
            r2 = random.randrange(0,numRoutes)

        # sol.routes[0].route[0]        # Randomly select nodes to swap from each route
        n1 = random.randrange(1, len(sol.routes[r1].route) - 1) # start with 1 to disregard depot
        n2 = random.randrange(1, len(sol.routes[r2].route) - 1)

        # Perform Swap
        _ = sol.routes[r1].route[n1]
        sol.routes[r1].route[n1] = sol.routes[r2].route[n2]
        sol.routes[r2].route[n2] = _
        
        # validate routes generated 
        

        return sol

    def __doubleBridgeInter(self, sol):
        # takes solution as input
        # gets 4 routes randomly
        # Select random node from each
        # Swap nodes
        numRoutes = len(sol.routes) # sol.routes - list

        # Randomly select 2 routes to swap
        r = list(range(numRoutes))
        random.shuffle(r)
        r1, r2, r3, r4 = r[0], r[1], r[2], r[3]
        
        # Randomly select nodes to swap from each route
        n1 = random.randrange(1, len(sol.routes[r1].route) - 1)
        n2 = random.randrange(1, len(sol.routes[r2].route) - 1)
        n3 = random.randrange(1, len(sol.routes[r3].route) - 1)
        n4 = random.randrange(1, len(sol.routes[r4].route) - 1)

        # Perform Swap - r1 & r3, r2 & r4
        _ = sol.routes[r1].route[n1]
        sol.routes[r1].route[n1] = sol.routes[r3].route[n3]
        sol.routes[r3].route[n3] = _
        _ = sol.routes[r2].route[n2]
        sol.routes[r2].route[n2] = sol.routes[r4].route[n4]
        sol.routes[r4].route[n4] = _

        return sol

    def __repr__(self):
        pass
        # return filename, 
        # string = {
        #     "Name" : self.instance.,
        #     "listDemand" : self.listDemand,
        #     #"dists"  : self.dist
        # }
        # return str(string)
    