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

    #region initialize with random solution
    def __init__(self, CVRPInstance, numCuckoos = 15, Pa = 0.25, Pc = 0.6, generations = 500, pdf_type = 'levy'):
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
        self.time = str("{0:.2f}".format(end - start)) 
        
        lenRoute = 0
        for route in self.nests[0].routes:
            lenRoute += len(route.route) - 2

        print('Dataset: ' + self.instance.fileName + ', Run time: ' + self.time 
            + ', Best Solution Cost: ' + str(self.nests[0].cost) + ', Optimal Value: ' 
            + str(self.instance.optimalValue) + ' routesGen(gen, min) = ' + str(len(self.nests[0].routes)) 
            + ', ' + str(self.instance.minNumVehicles) + ' numNodes(gen, req) = ' 
            + str(lenRoute+1) + ', ' + str(self.instance.dimension))

    def solveInstance(self):
        # Initialize Solutions
        for i in range(self.numCuckoos):
            sol = self.instance.create_random_solution() # Initialize Solution
            self.nests.append(sol)
        
        for i in range(self.generations):   
            # sort nests by cost
            self.nests.sort(key = o.attrgetter('cost'))

            # Search, and Evaluate with fraction Pc of Cuckoos of best cuckoos
            PcNum = math.floor(self.numCuckoos * self.Pc)
            for j in range(PcNum):
                _levyNest = deepcopy(self.nests[j])
                self.__performLevyFlights(_levyNest)
               
                # Randomly select a nest to compare with
                _nestCompare = random.randrange(1, self.numCuckoos)

                # If the generated solution is better than a randomly selected nest
                if _levyNest.cost < self.nests[_nestCompare].cost:
                    self.nests[_nestCompare] = deepcopy(_levyNest)
            
            # Abandon a fraction Pa of worse Cuckoos. Generate new random solutions for replacement
            self.nests.sort(key = o.attrgetter('cost'), reverse=True)
            PaNum = math.floor(self.numCuckoos * self.Pa)
            # Compute probability of each nest to be abandoned except the best nest
            for j in range(1, PaNum):
                del self.nests[0] # Abandon nest
                sol = self.instance.create_random_solution()
                self.nests.append(sol)

            # Sort from best to worst and keep best solution
            self.nests.sort(key = o.attrgetter('cost'))
    #endregion

    #region original levy flight implementation, levy step = number of 2-opt
    def __generateLevyStep(self):
        """
        In this implementation, a random value is generated from levy distribution using mantegna's algorithms.

        """
        # mantegna's algorithm
        beta = 1
        sigma = ((gamma(1 + beta)) * math.sin(math.pi*beta/2)) / ( beta * gamma((1+beta)/2) * math.pow(2,(beta-1)/2) )
        u = np.random.normal(loc=0,scale=sigma)
        v = np.random.normal(loc=0,scale=1)
        steplength = u/ math.pow(abs(v),1/beta)
        
        return steplength

    def __performLevyFlights(self, nest):
        # Generate random value x from levy 
        # According to randomly generated value, perform 2-opt x time or double-bridge
        r = self.__generateLevyStep()
        r = abs(r)
        iterateNum = math.ceil(r)

        upperBound = 5
        if iterateNum > upperBound:
            iterateNum = upperBound

        # One Small Neighborhood
        # for i in range(iterateNum):
        #     self.__shift1(nest)
        
        # Two Small Neighborhood
        # smallStepChoice = random.choice([1,2])
        # if smallStepChoice == 1:
        #     for i in range(iterateNum):
        #         self.__swap2_1(nest)
        # else:
        #     for i in range(iterateNum):
        #         self.__shift1(nest)

        # Two  Small Neighborhood and One Large
        # if iterateNum <= 4:
        #     smallStepChoice = random.choice([1,2])
        #     if smallStepChoice == 1:
        #         for i in range(iterateNum):
        #             self.__crossTwoOpt(nest)
        #     else:
        #         for i in range(iterateNum):
        #             self.__swap11(nest)
        # else:
        #     self.__swap2_2(nest)

        # Three  Small Neighborhood and One Large
        if iterateNum <= 4:
            smallStepChoice = random.choice([1,2,3])
            if smallStepChoice == 1:
                for i in range(iterateNum):
                    self.__crossTwoOpt(nest)
            elif smallStepChoice == 2:
                for i in range(iterateNum):
                    self.__swap11(nest)
            else: 
                for i in range(iterateNum):
                    self.__reinsertionIntra(nest)
        else:
            self.__swap2_2(nest)

        # One Small Neighborhood and One Large
        # if iterateNum <= 4:
        #     for i in range(iterateNum):
        #         self.__swap2_1(nest)
        # else:
        #     self.__crossDoubleBridgeInter(nest)

    #endregion
    

    #region neighborhood structures
    # the true twoOptInter
    def __crossTwoOpt(self,sol):
        # takes solution as input
        # gets 2 routes randomly
        # exchange 2 customer arcs
        numRoutes = len(sol.routes)

        # Perform Swap
        IsSwapValid = True
        numFailedAttempts = 0
        while IsSwapValid: 
            while True:
                rRouteIdx = random.choices(range(numRoutes), k=2)
                if rRouteIdx[0] != rRouteIdx[1]:
                    break  
            
            # Temporary variables for checking if swap is valid
            _solr1 = deepcopy(sol.routes[rRouteIdx[0]])
            _solr2 = deepcopy(sol.routes[rRouteIdx[1]])

            # Randomly select nodes for each arc to swap from each route
            # start with 1 to disregard depot
            rNodeIdx = []
            if (len(sol.routes[rRouteIdx[0]].route) >= 4 and
                len(sol.routes[rRouteIdx[1]].route) >= 4):
                rNodeIdx.append(random.randrange(1, len(_solr1.route) - 2))
                rNodeIdx.append(random.randrange(1, len(_solr2.route) - 2))
            else:
                numFailedAttempts +=1 
                break

            _tempSolr1 = deepcopy(_solr1)
            _solr1.route = _solr1.route[:rNodeIdx[0]+1] + _solr2.route[rNodeIdx[1]+1:]
            _solr2.route = _solr2.route[:rNodeIdx[1]+1] + _tempSolr1.route[rNodeIdx[0]+1:]  
                    
            self.instance.recalculate_route_demand_cost(_solr1)
            self.instance.recalculate_route_demand_cost(_solr2)

            if (_solr1.demand <= self.instance.capacity and
                _solr2.demand <= self.instance.capacity
                ):
                sol.routes[rRouteIdx[0]] = deepcopy(_solr1)
                sol.routes[rRouteIdx[1]] = deepcopy(_solr2)
                self.instance.recalculate_solution_cost(sol)
                break
            
            numFailedAttempts += 1
            if numFailedAttempts == self.numFailedAttemptsLevyLimit:
                break

    def __twoOptIntra(self,sol):
        pass
    # previously twoOptInter
    def __swap11(self, sol): 
        # takes solution as input
        # gets 2 routes randomly
        # Select random node from each
        # Swap nodes, until valid route is generated
        numRoutes = len(sol.routes) # sol.routes - list
        
        # Perform Swap
        IsSwapValid = True
        numFailedAttempts = 0
        while IsSwapValid:
            while True:
                rRouteIdx = random.choices(range(numRoutes), k=2)
                if rRouteIdx[0] != rRouteIdx[1]:
                    break  

            # Temporary variables for checking if swap is valid
            _solr1 = deepcopy(sol.routes[rRouteIdx[0]])
            _solr2 = deepcopy(sol.routes[rRouteIdx[1]])

            # Randomly select nodes to swap from each route
            # start with 1 to disregard depot
            rNodeIdx = []
            rNodeIdx.append(random.randrange(1, len(_solr1.route) - 1))
            rNodeIdx.append(random.randrange(1, len(_solr2.route) - 1))

            _solr1.route[rNodeIdx[0]], _solr2.route[rNodeIdx[1]] = _solr2.route[rNodeIdx[1]], _solr1.route[rNodeIdx[0]]

            self.instance.recalculate_route_demand_cost(_solr1)
            self.instance.recalculate_route_demand_cost(_solr2)

            if (_solr1.demand <= self.instance.capacity and
                _solr2.demand <= self.instance.capacity
                ):
                sol.routes[rRouteIdx[0]] = deepcopy(_solr1)
                sol.routes[rRouteIdx[1]] = deepcopy(_solr2)
                self.instance.recalculate_solution_cost(sol)
                break
            
            numFailedAttempts += 1
            if numFailedAttempts == self.numFailedAttemptsLevyLimit:
                break
    def __swap2_1(self,sol):
        # takes solution as input
        # gets 2 routes randomly
        # Select a random pair of adjacent nodes from 1 route and a random 
        # node from the other
        # Swap nodes, until valid route is generated
        numRoutes = len(sol.routes) # sol.routes - list
        IsSwapValid = True
        numFailedAttempts = 0
        while IsSwapValid:
            while True:
                rRouteIdx = random.choices(range(numRoutes), k=2)
                if rRouteIdx[0] != rRouteIdx[1]:
                    break

            # Temporary variables for checking if swap is valid
            _solr1 = deepcopy(sol.routes[rRouteIdx[0]])
            _solr2 = deepcopy(sol.routes[rRouteIdx[1]])
            
            rNodeIdx = []
            if len(sol.routes[rRouteIdx[0]].route) >= 4:
                rNodeIdx.append(random.randrange(1, len(_solr1.route) - 2)) 
                rNodeIdx.append(random.randrange(1, len(_solr2.route) - 1))
            else:
                numFailedAttempts +=1 
                break
            
            _solr1.route[rNodeIdx[0]+1], _solr2.route[rNodeIdx[1]] = _solr2.route[rNodeIdx[1]], _solr1.route[rNodeIdx[0]+1]
            _solr2.route.insert(rNodeIdx[1],_solr1.route[rNodeIdx[0]])
            del _solr1.route[rNodeIdx[0]]

            self.instance.recalculate_route_demand_cost(_solr1)
            self.instance.recalculate_route_demand_cost(_solr2)

            if (_solr1.demand <= self.instance.capacity and
                _solr2.demand <= self.instance.capacity
                ):
                sol.routes[rRouteIdx[0]] = deepcopy(_solr1)
                sol.routes[rRouteIdx[1]] = deepcopy(_solr2)
                self.instance.recalculate_solution_cost(sol)
                break
            
            numFailedAttempts += 1
            if numFailedAttempts == self.numFailedAttemptsLevyLimit:
                break
    def __swap2_2(self,sol):
        # takes solution as input
        # gets 2 routes randomly
        # Select a random pair of adjacent nodes from 2 route 
        # Swap nodes, until valid route is generated
        numRoutes = len(sol.routes) # sol.routes - list
        IsSwapValid = True
        numFailedAttempts = 0
        while IsSwapValid:
            while True:
                rRouteIdx = random.choices(range(numRoutes), k=2)
                if rRouteIdx[0] != rRouteIdx[1]:
                    break

            # Temporary variables for checking if swap is valid
            _solr1 = deepcopy(sol.routes[rRouteIdx[0]])
            _solr2 = deepcopy(sol.routes[rRouteIdx[1]])

            rNodeIdx = []
            if len(sol.routes[rRouteIdx[0]].route) >= 4 and len(sol.routes[rRouteIdx[1]].route) >= 4:
                rNodeIdx.append(random.randrange(1, len(_solr1.route) - 2)) 
                rNodeIdx.append(random.randrange(1, len(_solr2.route) - 2))
            else:
                numFailedAttempts +=1 
                break
            
            _solr1.route[rNodeIdx[0]], _solr2.route[rNodeIdx[1]] = _solr2.route[rNodeIdx[1]], _solr1.route[rNodeIdx[0]]
            _solr1.route[rNodeIdx[0]+1], _solr2.route[rNodeIdx[1]+1] = _solr2.route[rNodeIdx[1]+1], _solr1.route[rNodeIdx[0]+1] 

            self.instance.recalculate_route_demand_cost(_solr1)
            self.instance.recalculate_route_demand_cost(_solr2)

            if (_solr1.demand <= self.instance.capacity and
                _solr2.demand <= self.instance.capacity
                ):
                sol.routes[rRouteIdx[0]] = deepcopy(_solr1)
                sol.routes[rRouteIdx[1]] = deepcopy(_solr2)
                self.instance.recalculate_solution_cost(sol)
                break
            
            numFailedAttempts += 1
            if numFailedAttempts == self.numFailedAttemptsLevyLimit:
                break
    def __crossDoubleBridgeInter(self, sol):
        # takes solution as input
        # gets 4 routes randomly
        # Select random node from each
        # Swap nodes, until valid route is generated
        numRoutes = len(sol.routes) # sol.routes - list

        # Randomly select 4 routes to swap
        rRouteIdx = list(range(numRoutes))
        # Perform Swap - r1 & r3, r2 & r4
        IsSwapValid = True
        numFailedAttempts = 0
        while IsSwapValid:

            # re-shuffle routes to swap
            if numRoutes < 4:
                IsSwapValid = False
                break
            random.shuffle(rRouteIdx)
            
            # Temporary variables for checking if swap is valid
            _solr1 = deepcopy(sol.routes[rRouteIdx[0]])
            _solr2 = deepcopy(sol.routes[rRouteIdx[1]])
            _solr3 = deepcopy(sol.routes[rRouteIdx[2]])
            _solr4 = deepcopy(sol.routes[rRouteIdx[3]])

            rNodeIdx = []
            # Randomly select nodes to swap from each route
            if (len(sol.routes[rRouteIdx[0]].route) >= 4 and
                len(sol.routes[rRouteIdx[1]].route) >= 4 and
                len(sol.routes[rRouteIdx[2]].route) >= 4 and
                len(sol.routes[rRouteIdx[3]].route) >= 4
                ):
                rNodeIdx.append(random.randrange(1, len(_solr1.route) - 2))
                rNodeIdx.append(random.randrange(1, len(_solr2.route) - 2))
                rNodeIdx.append(random.randrange(1, len(_solr3.route) - 2))
                rNodeIdx.append(random.randrange(1, len(_solr4.route) - 2))
            else:
                numFailedAttempts += 1
                break
            
            _tempSolr = deepcopy(_solr1)
            _solr1.route = _solr1.route[:rNodeIdx[0]+1] + _solr3.route[rNodeIdx[2]+1:]
            _solr3.route = _solr3.route[:rNodeIdx[2]+1] + _tempSolr.route[rNodeIdx[0]+1:]  
            _tempSolr = deepcopy(_solr2)
            _solr2.route = _solr2.route[:rNodeIdx[1]+1] + _solr4.route[rNodeIdx[3]+1:]
            _solr4.route = _solr4.route[:rNodeIdx[3]+1] + _tempSolr.route[rNodeIdx[1]+1:]  

            self.instance.recalculate_route_demand_cost(_solr1)
            self.instance.recalculate_route_demand_cost(_solr2)
            self.instance.recalculate_route_demand_cost(_solr3)
            self.instance.recalculate_route_demand_cost(_solr4)


            if (_solr1.demand <= self.instance.capacity and
                _solr2.demand <= self.instance.capacity and
                _solr3.demand <= self.instance.capacity and
                _solr4.demand <= self.instance.capacity
                ):
                sol.routes[rRouteIdx[0]] = deepcopy(_solr1)
                sol.routes[rRouteIdx[1]] = deepcopy(_solr2)
                sol.routes[rRouteIdx[2]] = deepcopy(_solr3)
                sol.routes[rRouteIdx[3]] = deepcopy(_solr4)
                self.instance.recalculate_solution_cost(sol)
                break

            numFailedAttempts += 1
            if numFailedAttempts == self.numFailedAttemptsLevyLimit:
                break
    def __shift1(self, sol):
        # takes solution as input
        # select route randomly
        # select random node from that route, cycle through all other routes
        # if insert is feasible, take      
        numRoutes = len(sol.routes) # sol.routes - list
        # select random route and random node
        rRouteIdx = random.randrange(0, numRoutes)
        rNodeIdx = random.randrange(1, len(sol.routes[rRouteIdx].route) - 1)

        rNode = sol.routes[rRouteIdx].route[rNodeIdx]
        rNodeDemand = self.instance.listDemand[rNode]
        for i, route in enumerate(sol.routes):
            if i != rRouteIdx and route.demand + rNodeDemand < self.instance.capacity:
                _rPlacement = random.choice(range(1,len(route.route)))
                route.route.insert(_rPlacement,rNode)
                del sol.routes[rRouteIdx].route[rNodeIdx]
                self.instance.recalculate_route_demand_cost(route)

                # if there are no more nodes in route r
                if len(sol.routes[rRouteIdx].route) <= 2:
                    del sol.routes[rRouteIdx]
                else:
                    self.instance.recalculate_route_demand_cost(sol.routes[rRouteIdx])
                self.instance.recalculate_solution_cost(sol)
                break
    def __shift2(self,sol):
        # takes solution as input
        # select route randomly
        # select random node from that route, cycle through all other routes
        # if insert is feasible, take      
        numRoutes = len(sol.routes) # sol.routes - list
        # select random route and random node
        rRouteIdx = random.randrange(0, numRoutes)
        if len(sol.routes[rRouteIdx].route) >= 4:
            rNodeIdx = random.randrange(1, len(sol.routes[rRouteIdx].route) - 2)
            rNode = [sol.routes[rRouteIdx].route[rNodeIdx], sol.routes[rRouteIdx].route[rNodeIdx+1]]
            rNodeDemand = [self.instance.listDemand[rNode[0]], self.instance.listDemand[rNode[1]]]
            for i, route in enumerate(sol.routes):
                if i != rRouteIdx and route.demand + rNodeDemand[0] + rNodeDemand[1] < self.instance.capacity:
                    _rPlacement = random.choice(range(1,len(route.route)))
                    route.route.insert(_rPlacement,rNode[1])
                    route.route.insert(_rPlacement,rNode[0])
                    _tempSol2 = sol.routes[rRouteIdx].route
                    del sol.routes[rRouteIdx].route[rNodeIdx]
                    del sol.routes[rRouteIdx].route[rNodeIdx]
                    self.instance.recalculate_route_demand_cost(route)

                    # if there are no more nodes in route r
                    if len(sol.routes[rRouteIdx].route) <= 2:
                        del sol.routes[rRouteIdx]
                    else:
                        self.instance.recalculate_route_demand_cost(sol.routes[rRouteIdx])
                    self.instance.recalculate_solution_cost(sol)  
                    break  
    def __exchangeIntra(self,sol):
        #takes solution as input
        # select route randomly
        # select 2 random nodes and swap
        numRoutes = len(sol.routes) 
        # select random route and random node
        rRouteIdx = random.randrange(0, numRoutes)
        if len(sol.routes[rRouteIdx].route) >= 4:
            while True:
                rNode = random.choices(range(1,len(sol.routes[rRouteIdx].route)-1), k=2) 
                if rNode[0] != rNode[1]:
                    break               
            sol.routes[rRouteIdx].route[rNode[0]], sol.routes[rRouteIdx].route[rNode[1]]  = sol.routes[rRouteIdx].route[rNode[1]], sol.routes[rRouteIdx].route[rNode[0]]
            self.instance.recalculate_route_demand_cost(sol.routes[rRouteIdx])
            self.instance.recalculate_solution_cost(sol)
    def __reinsertionIntra(self,sol):
        """
        From the given solution, randomly selects a route, node,
        and random index from the route. The node will be moved
        to the selected index.
        """
        numRoutes = len(sol.routes) 
        # select random route and random node
        rRouteIdx = random.randrange(0, numRoutes)
        if len(sol.routes[rRouteIdx].route) >= 4:
            while True:
                rNodeIdx = random.randrange(1, len(sol.routes[rRouteIdx].route) - 1)
                rSwapIdx = random.randrange(1, len(sol.routes[rRouteIdx].route) - 1)
                if rNodeIdx != rSwapIdx:
                    break
            rNode = sol.routes[rRouteIdx].route[rNodeIdx]
            del sol.routes[rRouteIdx].route[rNodeIdx]
            sol.routes[rRouteIdx].route.insert(rSwapIdx,rNode)
            self.instance.recalculate_route_demand_cost(sol.routes[rRouteIdx])
            self.instance.recalculate_solution_cost(sol)
    def __orOpt2(self,sol):
        """
        From the given solution, randomly selects a route, node,
        and random index from the route. Nodes n and n+1 will be moved
        to the selected index.
        """
        numRoutes = len(sol.routes)
        # select random route and random node
        rRouteIdx = random.randrange(0, numRoutes)
        
        if len(sol.routes[rRouteIdx].route) >= 5:
            while True:
                rNodeIdx = random.randrange(1, len(sol.routes[rRouteIdx].route) - 2)
                rSwapIdx = random.randrange(1, len(sol.routes[rRouteIdx].route) - 2)
                if rNodeIdx != rSwapIdx:
                    break
            rNode = []
            rNode.append(sol.routes[rRouteIdx].route[rNodeIdx])
            rNode.append(sol.routes[rRouteIdx].route[rNodeIdx+1])
            del sol.routes[rRouteIdx].route[rNodeIdx]
            del sol.routes[rRouteIdx].route[rNodeIdx]
            sol.routes[rRouteIdx].route.insert(rSwapIdx,rNode[1])
            sol.routes[rRouteIdx].route.insert(rSwapIdx,rNode[0])
            self.instance.recalculate_route_demand_cost(sol.routes[rRouteIdx])
            self.instance.recalculate_solution_cost(sol)
        
    def __orOpt3(self,sol):
        """
        From the given solution, randomly selects a route, node,
        and random index from the route. Nodes n, n+1 and n+2 will be moved
        to the selected index.
        """
        numRoutes = len(sol.routes)
        # select random route and random node
        rRouteIdx = random.randrange(0, numRoutes)
        
        if len(sol.routes[rRouteIdx].route) >= 6:
            while True:
                rNodeIdx = random.randrange(1, len(sol.routes[rRouteIdx].route) - 3)
                rSwapIdx = random.randrange(1, len(sol.routes[rRouteIdx].route) - 3)
                if rNodeIdx != rSwapIdx:
                    break
            rNode = []
            rNode.append(sol.routes[rRouteIdx].route[rNodeIdx])
            rNode.append(sol.routes[rRouteIdx].route[rNodeIdx+1])
            rNode.append(sol.routes[rRouteIdx].route[rNodeIdx+2])
            del sol.routes[rRouteIdx].route[rNodeIdx]
            del sol.routes[rRouteIdx].route[rNodeIdx]
            del sol.routes[rRouteIdx].route[rNodeIdx]
            sol.routes[rRouteIdx].route.insert(rSwapIdx,rNode[2])
            sol.routes[rRouteIdx].route.insert(rSwapIdx,rNode[1])
            sol.routes[rRouteIdx].route.insert(rSwapIdx,rNode[0])
            self.instance.recalculate_route_demand_cost(sol.routes[rRouteIdx])
            self.instance.recalculate_solution_cost(sol)
    #endregion
    

    def readData(self):
        data = {
            "Name" : self.instance.fileName,
            "Best Solution Cost" : self.nests[0].cost,
            "Optimal Value" : self.instance.optimalValue,
            "Run Time" : float(self.time),
            "Solution" : self.nests
        }
        return data

    def __repr__(self):
        
        # return filename, 
        string = {
            "Name" : self.instance.fileName,
            "Best Solution Cost" : self.nests[0].cost,
            "Optimal Value" : self.instance.optimalValue,
            "Run Time" : self.time,
            "Solution" : self.nests
        }
        return str(string)
    
    #region initialize with non-random heuristic, clarke-wright savings method
    # def __init__(self, CVRPInstance, numCuckoos = 20, Pa = 0.2, Pc = 0.6, generations = 5000, pdf_type = 'levy'):
    #     self.instance = CVRPInstance
    #     self.Pa = Pa
    #     self.Pc = Pc
    #     self.generations = generations
    #     self.pdf_type = pdf_type
    #     self.numCuckoos = numCuckoos
    #     self.nests = []
    #     self.numFailedAttemptsLevyLimit = 1
    #     random.seed()
    #     self.initialSolution = self.instance.create_random_solution()

    #     start = timer()
    #     self.solveInstance()
    #     end = timer()
    #     self.time = str("{0:.2f}".format(end - start)) 
        
    #     lenRoute = 0
    #     for route in self.nests[0].routes:
    #         lenRoute += len(route.route) - 2

    #     print('Dataset: ' + self.instance.fileName 
    #         + ', Optimal Value: ' + str(self.instance.optimalValue)
    #         + ', Best Solution Cost: ' + str(self.nests[0].cost)
    #         + ', clarkeSol: ' + str(self.initialSolution.cost)
    #         + ', Run time: ' + self.time 
    #         + ', routesGen(gen, min) = ' + str(len(self.nests[0].routes)) 
    #         + ', ' + str(self.instance.minNumVehicles))
    #         # ' numNodes(gen, req) = ' + str(lenRoute+1) + ', ' + str(self.instance.dimension))

    # def solveInstance(self):
    #     # Initialize Solutions
    #     for i in range(self.numCuckoos):
    #         sol = self.initialSolution # Initialize Solution
    #         self.nests.append(sol)
        
    #     for i in range(self.generations):   
    #         # sort nests by cost
    #         self.nests.sort(key = o.attrgetter('cost'))

    #         # Search, and Evaluate with fraction Pc of Cuckoos of best cuckoos
    #         PcNum = math.floor(self.numCuckoos * self.Pc)
    #         for j in range(PcNum):
    #             _levyNest = deepcopy(self.nests[j])
    #             self.__performLevyFlights(_levyNest)
               
    #             # Randomly select a nest to compare with
    #             _nestCompare = random.randrange(1, self.numCuckoos)

    #             # If the generated solution is better than a randomly selected nest
    #             if _levyNest.cost < self.nests[_nestCompare].cost:
    #                 self.nests[_nestCompare] = deepcopy(_levyNest)
            
    #         # Abandon a fraction Pa of worse Cuckoos. Generate new random solutions for replacement
    #         self.nests.sort(key = o.attrgetter('cost'), reverse=True)
    #         PaNum = math.floor(self.numCuckoos * self.Pa)
    #         # Compute probability of each nest to be abandoned except the best nest
    #         for j in range(1, PaNum):
    #             del self.nests[0] # Abandon nest
    #             sol = self.initialSolution
    #             self.nests.append(sol)

    #         # Sort from best to worst and keep best solution
    #         self.nests.sort(key = o.attrgetter('cost'))
    #endregion

    #region gaussian implementation
    # def __generateLevyStep(self):
    #     """
    #     In this implementation, a random value is generated from gaussian distribution
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
        
    #     twoOptIter = (math.ceil(r))
    #     doubleBridgeIter = 0
        
    #     for i in range(twoOptIter):
    #         nest = self.__twoOptInter(nest)

    #     for i in range(doubleBridgeIter):
    #         nest = self.__doubleBridgeInter(nest)
    #endregion
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