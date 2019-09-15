from CVRP import CVRPInfo as CVRP
import operator as o
import math
import random
from copy import deepcopy
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
        
        # Initialize Solutions
        for i in range(self.numCuckoos):
            sol = self.instance.create_random_solution() # Initialize Solution
            self.nests.append(sol)
        
        for i in range(self.generations):   
            print('DEBUG: Generation num: ' + str(i))

            # sort nests by cost
            self.nests.sort(key = o.attrgetter('cost'))
            best_solution = self.nests[0]
            random.shuffle(self.nests)

            # Search, and Evaluate with fraction Pc of Cuckoos
            for j in range(math.floor(self.numCuckoos * self.Pc)):
                print('DEBUG: Levy Flights iteration number ' + str(j))
                _levyNest = deepcopy(self.nests[j])
                self.__performLevyFlights(_levyNest)
                print('DEBUG: Levy Flights iteration number ' + str(j) +  ' success')
               
                # Randomly select a nest to compare with
                _ = random.randrange(0, self.numCuckoos)

                # If the generated solution is better than a randomly selected nest
                if _levyNest.cost < self.nests[_].cost:
                    self.nests[_] = _levyNest
                    print('DEBUG: Replace Fi with Fj')
            
            # Abandon a fraction Pa of worse Cuckoos. Generate new random solutions for replacement
            self.nests.sort(key = o.attrgetter('cost'), reverse=True)
            for j in range(math.floor(self.numCuckoos * self.Pa)):
                del self.nests[0] # Abandon nest
                sol = self.instance.create_random_solution()
                self.nests.append(sol)
            print('DEBUG: Success, abandon worst nests Pa and generate new random')



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
            print('DEBUG: Levy Flights twoOpt')
            nest = self.__twoOptInter(nest)

        for i in range(doubleBridgeIter):
            print('DEBUG: Levy Flights doubleBridge')
            nest = self.__doubleBridgeInter(nest)
        
        # validate nest
        # nest.
        # recalculate nest 

    def __twoOptInter(self, sol): 
        # takes solution as input
        # gets 2 routes randomly
        # Select random node from each
        # Swap nodes, until valid route is generated
        numRoutes = len(sol.routes) # sol.routes - list

        r = list(range(numRoutes))
        
        # Perform Swap
        IsSwapInvalid = True
        numFailedAttempts = 0
        while IsSwapInvalid:
            print('DEBUG: Levy Flights twoOpt pre-deepcopy')
           
            # Randomly select 2 routes to swap
            random.shuffle(r)
            r1, r2 = r[0], r[1]

            # Temporary variables for checking if swap is valid
            _solr1 = deepcopy(sol.routes[r1])
            _solr2 = deepcopy(sol.routes[r2])

            # Randomly select nodes to swap from each route
            n1 = random.randrange(1, len(_solr1.route) - 1) # start with 1 to disregard depot
            n2 = random.randrange(1, len(_solr2.route) - 1)
            
            _ = _solr1.route[n1]
            _solr1.route[n1] = _solr2.route[n2]
            _solr2.route[n2] = _

            print('DEBUG: Levy Flights twoOpt after first swap')

            if _solr1.demand <= self.instance.capacity:
                if _solr2.demand <= self.instance.capacity:
                    sol.routes[r1] = _solr1
                    sol.routes[r2] = _solr2
                    IsSwapInvalid = False
                    print('DEBUG: Levy Flights twoOpt after complete swap')
            
            numFailedAttempts += 1
            if numFailedAttempts == 5:
                break

        return sol

    def __doubleBridgeInter(self, sol):
        # takes solution as input
        # gets 4 routes randomly
        # Select random node from each
        # Swap nodes, until valid route is generated
        numRoutes = len(sol.routes) # sol.routes - list

        # Randomly select 4 routes to swap
        r = list(range(numRoutes))
        # Perform Swap - r1 & r3, r2 & r4
        IsSwapInvalid = True
        numFailedAttempts = 0
        while IsSwapInvalid:
            print('DEBUG: Levy Flights doubleBridge pre-deepcopy')

            # re-shuffle routes to swap
            random.shuffle(r)
            r1, r2, r3, r4 = r[0], r[1], r[2], r[3]
            
            # Temporary variables for checking if swap is valid
            _solr1 = deepcopy(sol.routes[r1])
            _solr2 = deepcopy(sol.routes[r2])
            _solr3 = deepcopy(sol.routes[r3])
            _solr4 = deepcopy(sol.routes[r4])

            # Randomly select nodes to swap from each route
            n1 = random.randrange(1, len(_solr1.route) - 1)
            n2 = random.randrange(1, len(_solr2.route) - 1)
            n3 = random.randrange(1, len(_solr3.route) - 1)
            n4 = random.randrange(1, len(_solr4.route) - 1)

            _ = _solr1.route[n1]
            _solr1.route[n1] = _solr3.route[n3]
            _solr3.route[n3] = _
            _ = _solr2.route[n2]
            _solr2.route[n2] = _solr4.route[n4]
            _solr4.route[n4] = _

            print('DEBUG: Levy Flights doubleBridge after first swap')

            if _solr1.demand <= self.instance.capacity:
                if _solr2.demand <= self.instance.capacity:
                    if _solr3.demand <= self.instance.capacity:
                       if _solr4.demand <= self.instance.capacity:
                            sol.routes[r1] = _solr1
                            sol.routes[r2] = _solr2
                            sol.routes[r3] = _solr3
                            sol.routes[r4] = _solr4
                            IsSwapInvalid = False
                            print('DEBUG: Levy Flights doubleBridge after complete swap')
            numFailedAttempts += 1
            if numFailedAttempts == 5:
                break

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
    