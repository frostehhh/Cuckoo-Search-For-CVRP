from CVRP import CVRPInfo as CVRP
import operator as o
import math
import random
import numpy as np
from timeit import default_timer as timer
from copy import deepcopy
from scipy.stats import levy
from scipy.special import gamma
from numpy.random import RandomState



class CuckooSearch:
    """
    Cuckoo Search CS-Ouaarab with modified LF

    For this implementation of Cuckoo Search for the CVRP, the given pseudocode will be followed:
    - Initialize randomly generated solutions
    - With fraction Pc (fraction of cuckoos to perform levy flights), randomly select a cuckoo to
      perform levy flights. If the new solution found is better than a randomly selected nest, 
      replace the randomly selected nest.
    - The worse Pa (fraction of nest to be abandoned) nests will be replaced with randomly generated solutions
    - Rank solutions
    - Keep best solution. (In this implementation, nest[0], the current best cannot be abandoned)

    For Levy flights, Mantegna's algorithm was used. 
    
    """


    def __init__(self, CVRPInstance, numCuckoos = 20, Pa = 0.2, Pc = 0.6, generations = 5000, pdf_type = 'levy'):
        self.instance = CVRPInstance
        self.Pa = Pa
        self.Pc = Pc
        self.generations = generations
        self.pdf_type = pdf_type
        self.numCuckoos = numCuckoos
        self.nests = []
        self.numFailedAttemptsLevyLimit = 1
        random.seed()

        start = timer()
        self.solveInstance()
        end = timer()
        time = str("{0:.2f}".format(end - start)) 
    
        print('Dataset: ' + self.instance.fileName + ', Run time: ' + time 
            + ', Best Solution Cost: ' + str(self.nests[0].cost) + ', Optimal Value: ' 
            + str(self.instance.optimalValue))

    def solveInstance(self):
        # Initialize Solutions
        for i in range(self.numCuckoos):
            sol = self.instance.create_random_solution() # Initialize Solution
            self.nests.append(sol)
        
        for i in range(self.generations):   
            # print('DEBUG: Generation num: ' + str(i))

            # sort nests by cost
            self.nests.sort(key = o.attrgetter('cost'))
            random.shuffle(self.nests)

            # Search, and Evaluate with fraction Pc of Cuckoos of best cuckoos
            for j in range(math.floor(self.numCuckoos * self.Pc)):
                _levyNest = deepcopy(self.nests[j])
                self.__performLevyFlights(_levyNest)
               
                # Randomly select a nest to compare with
                _ = random.randrange(1, self.numCuckoos)

                # If the generated solution is better than a randomly selected nest
                if _levyNest.cost < self.nests[_].cost:
                    self.nests[_] = _levyNest
                    # print('DEBUG: Replace Fi with Fj')
            
            # Abandon a fraction Pa of worse Cuckoos. Generate new random solutions for replacement
            self.nests.sort(key = o.attrgetter('cost'), reverse=True)
            # Compute probability of each nest to be abandoned except the best nest
            for j in range(1, math.floor(self.numCuckoos * self.Pa)):
                del self.nests[0] # Abandon nest
                sol = self.instance.create_random_solution()
                self.nests.append(sol)
            # print('DEBUG: Success, abandon worst nests Pa and generate new random')

            # Sort from best to worst and keep best solution
            self.nests.sort(key = o.attrgetter('cost'))
    
    #region first implementation, range 0-5 of levy distrib considered. xiao
    # def __generateLevyStep(self):
    #     """
    #     In this implementation, a random value is generated from levy distribution using mantegna's algorithms.
    #     A levy flight will be generated as follows:

    #     levy step
    #     0 - 1, 0.2
    #     1 - 2, 0.4
    #     2 - 3, 0.6
    #     3 - 4, 0.8
    #     4 - 5, 1
    #     """
    #     # mantegna's algorithm
    #     beta = 1
    #     stepsize = 1
    #     sigma = ((gamma(1 + beta)) * math.sin(math.pi*beta/2)) / ( beta * gamma((1+beta)/2) * math.pow(2,(beta-1)/2) )
    #     u = np.random.normal(loc=0,scale=sigma)
    #     v = np.random.normal(loc=0,scale=1)
    #     steplength = u/ math.pow(abs(v),1/beta)
    #     step = stepsize*steplength
    #     step = abs(step)

    #     # not mantegna's algorithm. I'm sure this ain't right tho
    #     if step >= 0 and step <= 1:
    #         return 0.2
    #     elif step > 1 and step <= 2:
    #         return 0.4
    #     elif step > 2 and step <= 3:
    #         return 0.6
    #     elif step > 3 and step <= 4:
    #         return 0.8
    #     elif step > 4 and step <= 5:
    #         return 1
    #     else:
    #         return 1

    # def __performLevyFlights(self, nest):
    #     # Generate random value x from levy 
    #     # According to randomly generated value, perform 2-opt x time or double-bridge

    #     # # temporary random num gen
    #     # r = random.random()

    #     r = self.__generateLevyStep()
        
    #     twoOptIter = 0
    #     doubleBridgeIter = 0
    #     if r >= 0 and r <= 0.2:
    #         twoOptIter = 1
    #     elif r > 0.2 and r <= 0.4:
    #         twoOptIter = 2
    #     elif r > 0.4 and r <= 0.6:
    #         twoOptIter = 3
    #     elif r > 0.6 and r <= 0.8:
    #         twoOptIter = 4
    #     elif r > 0.8 and r <= 1.0:
    #         doubleBridgeIter = 1
        
    #     for i in range(twoOptIter):
    #         nest = self.__twoOptInter(nest)

    #     for i in range(doubleBridgeIter):
    #         nest = self.__doubleBridgeInter(nest)
    #endregion

    #region original levy flight implementation, levy step = number of 2-opt
    def __generateLevyStep(self):
        """
        In this implementation, a random value is generated from levy distribution using mantegna's algorithms.

        """
        # mantegna's algorithm
        beta = 1
        stepsize = 1
        sigma = ((gamma(1 + beta)) * math.sin(math.pi*beta/2)) / ( beta * gamma((1+beta)/2) * math.pow(2,(beta-1)/2) )
        u = np.random.normal(loc=0,scale=sigma)
        v = np.random.normal(loc=0,scale=1)
        steplength = u/ math.pow(abs(v),1/beta)
        step = stepsize*steplength
        step = abs(step)
        
        return step

    def __performLevyFlights(self, nest):
        # Generate random value x from levy 
        # According to randomly generated value, perform 2-opt x time or double-bridge

        # # temporary random num gen
        # r = random.random()

        r = self.__generateLevyStep()
        
        twoOptIter = math.floor(r)
        doubleBridgeIter = 1
        
        for i in range(twoOptIter):
            nest = self.__twoOptInter(nest)

        for i in range(doubleBridgeIter):
            nest = self.__doubleBridgeInter(nest)
    #endregion

    #region gaussian, not done
    # def __generateLevyStep(self):
    #     """
    #     In this implementation, a random value is generated from levy distribution using mantegna's algorithms.
    #     A levy flight will be generated as follows:

    #     levy step
    #     0 - 1, 0.2
    #     1 - 2, 0.4
    #     2 - 3, 0.6
    #     3 - 4, 0.8
    #     4 - 5, 1
    #     """
    #     # mantegna's algorithm
    #     stepsize = 5
    #     steplength = np.random.normal(loc=0,scale=1)
    #     step = stepsize*steplength
    #     step = abs(step)
        
    #     return step

    # def __performLevyFlights(self, nest):
    #     # Generate random value x from levy 
    #     # According to randomly generated value, perform 2-opt x time or double-bridge

    #     # # temporary random num gen
    #     # r = random.random()

    #     r = self.__generateLevyStep()
        
    #     twoOptIter = 0
    #     doubleBridgeIter = 0
    #     if r >= 0 and r <= 0.2:
    #         twoOptIter = 1
        
        
    #     for i in range(twoOptIter):
    #         nest = self.__twoOptInter(nest)

    #     for i in range(doubleBridgeIter):
    #         nest = self.__doubleBridgeInter(nest)
    #endregion

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

            if _solr1.demand <= self.instance.capacity:
                if _solr2.demand <= self.instance.capacity:
                    sol.routes[r1] = _solr1
                    sol.routes[r2] = _solr2
                    IsSwapInvalid = False
            
            numFailedAttempts += 1
            if numFailedAttempts == self.numFailedAttemptsLevyLimit:
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

            if _solr1.demand <= self.instance.capacity:
                if _solr2.demand <= self.instance.capacity:
                    if _solr3.demand <= self.instance.capacity:
                       if _solr4.demand <= self.instance.capacity:
                            sol.routes[r1] = _solr1
                            sol.routes[r2] = _solr2
                            sol.routes[r3] = _solr3
                            sol.routes[r4] = _solr4
                            IsSwapInvalid = False
            numFailedAttempts += 1
            if numFailedAttempts == self.numFailedAttemptsLevyLimit:
                break

        return sol


    def __repr__(self):
        
        # return filename, 
        string = {
            "Name" : self.instance.fileName,
            "Best Solution Cost" : self.nests[0].cost,
            "Optimal Value" : self.instance.optimalValue,
            "Run Time" : 'test',
            "Solution" : self.nests
        }
        return str(string)
    