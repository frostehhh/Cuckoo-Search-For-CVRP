import os
import math
import random
import threading
import operator as o
from PIL import Image, ImageDraw
import Parser as p
class CVRPInfo():
    def __init__(self, data_file):
        self.read_data(data_file)
        self.__compute_dists()
        self.start_node = 0
        self.solutions = [] 
        random.seed()

    def read_data(self, path):
        self.listCoord, self.listDemand, self.instanceData = p.parse_file(path)
        self.fileName = self.instanceData['Name']
        self.minNumVehicles = self.instanceData['MinNumVehicles']
        self.optimalValue = self.instanceData['OptimalValue']
        self.capacity = self.instanceData['Capacity']
        self.dimension = len(self.listCoord)

    def __compute_dist(self, n1, n2):
        n1 = self.listCoord[n1]
        n2 = self.listCoord[n2]
        return math.sqrt((n1[0] - n2[0])**2 + (n1[1] - n2[1])**2)

    def __compute_dists(self):
        self.dist = [list([-1 for _ in range(self.dimension)]) \
                        for _ in range(self.dimension)]
        for xi in range(self.dimension):
            for yi in range(self.dimension):
                self.dist[xi][yi] = self.__compute_dist(xi, yi)

    def create_solution(self, routes):
        cost = 0
        demand = 0
        is_valid = True
        for route in routes:
            if not route.is_valid:
                is_valid = False
            cost += route.cost
            demand += route.demand
        sol = Solution(cost=cost, demand=demand, is_valid=is_valid, routes=routes)
        return sol

    def create_route(self, node_list):
        if node_list[0] != self.start_node:
            return None
        cost = 0
        demand = 0
        is_valid = True
        for i in range(1, len(node_list)):
            n1, n2 = node_list[i - 1], node_list[i]
            cost += self.dist[n1][n2]
            demand += self.listDemand[n2]
        if demand > self.capacity:
            is_valid = False

        route = Route(cost=cost, demand=demand, is_valid=is_valid, route=node_list)
        return route

    def recalculate_route_demand_cost(self, route):
        cost = 0
        demand = 0
        is_valid = True
        for i in range(len(route.route)):
            n1, n2 = route.route[i - 1], route.route[i]
            cost += self.dist[n1][n2]
            demand += self.listDemand[n2]
        route.cost = cost
        route.demand = demand
        return route
    
    def recalculate_solution_cost(self, sol):
        cost = 0
        for route in sol.routes:
            cost += route.cost
        sol.cost = cost
        return sol        

    #region original create random solution
    # def create_random_solution(self):
    #     unserviced = [i for i in range(1, self.dimension)]
    #     random.shuffle(unserviced)
    #     routes = [] # list of all routes
    #     cur_route = [0] # start with depot node
    #     route_demand = 0
    #     route_length = 0

    #     while unserviced:
    #         node = unserviced[0]
    #         if route_demand + self.listDemand[node] <= self.capacity:
    #             cur_route += [node]
    #             route_length += 1
    #             route_demand += self.listDemand[node]
    #             del unserviced[0]
    #             continue
    #         else:
    #             routes += [self.create_route(cur_route + [0])] # end with depot node
    #             # Reset variables for next iteration
    #             cur_route = [0] 
    #             route_demand = 0
    #             route_length = 0
    #     routes += [self.create_route(cur_route + [0])]

    #     return self.create_solution(routes)
    #endregion

    #region create random solution. min-cost algorithm. sorted from closest to farthest
    # def create_random_solution(self):
    #     """
    #     In this implementation, min-cost paths are generated while satisfying
    #     capacity constraints.
    #     """
    #     unserviced = [i for i in range(1, self.dimension)]
    #     routes = [] # list of all routes
    #     cur_route = [0] # start with depot node
    #     route_demand = 0
    #     route_length = 0
    #     curr_node = 0

    #     while unserviced:
    #         # get nearest node to current node
    #         # self.dist[currNode][i]
    #         # get unserviced nodes sorted by nearest to farthest
    #         dist_currNode_to_unserviced = []
    #         for node in unserviced:
    #             dist_currNode_to_unserviced += [self.dist[curr_node][node]]
    #         # unpack sorted unserviced nodes
    #         dist_currNode_to_unserviced, unserviced = [list(x) for x in zip(*sorted(zip(dist_currNode_to_unserviced, unserviced)))]

    #         for i, node in enumerate(unserviced):
    #             if route_demand + self.listDemand[node] <= self.capacity:
    #                 cur_route += [node]
    #                 route_length += 1
    #                 route_demand += self.listDemand[node]
    #                 del unserviced[i], dist_currNode_to_unserviced[i]
    #                 if route_demand == self.capacity:
    #                     routes += [self.create_route(cur_route + [0])] # end with depot node
    #                     # Reset variables for next iteration
    #                     cur_route = [0] 
    #                     route_demand = 0
    #                     route_length = 0
    #                     curr_node = 0
    #                 else:
    #                     curr_node = node
    #                 break
    #         else:
    #             routes += [self.create_route(cur_route + [0])] # end with depot node
    #             # Reset variables for next iteration
    #             cur_route = [0] 
    #             route_demand = 0
    #             route_length = 0
    #             curr_node = 0

    #     routes += [self.create_route(cur_route + [0])]

    #     return self.create_solution(routes)
    # endregion

    # region create random solution, savings method
    def create_random_solution(self):
        def sortSavings(savings):
            return savings.savings
        
        savingsList = self.__calculateCustomerSavings()
        savingsList.sort(key=sortSavings, reverse=True)
        unserviced = [i for i in range(1, self.dimension)]
        routes = []
        # Initialize routes
        for node in unserviced:
            routes.append(self.create_route([0,node,0]))

        
        for i in range(0, len(savingsList)):

            savingsNodesIdx = savingsList[i].nodesIdx
            savingsRoutesIdx = []
            nodesFoundCounter = 0
            isSavingsPairValid = True
            doesIncludeNode = [False,False]
            nodePosInRoute = [0,0]

            # check if merge is possible
            # A node should be at the start of its trip while the other is at the end
            # capacity constraints are respected.
            # Each node should be in their separate trips.

            # Find routes where either of the nodes exist. Will perform the following:
            # Break, if both nodes are in route
            # Break, if either node is not in start or end of route
            for routeIdx, route in enumerate(routes):
                if savingsNodesIdx[0] in route.route:
                    doesIncludeNode[0] = True
                elif savingsNodesIdx[1] in route.route:
                    doesIncludeNode[1] = True
                # If neither is in the route, continue to next iteration
                else:
                    continue
                # Check if both nodes are in the route. If true, break
                if (savingsNodesIdx[0] in route.route and
                    savingsNodesIdx[1] in route.route
                    ):
                    isSavingsPairValid = False
                    break
                # Check if node is in start or end of the route. If false, continue
                # to next iteration
                if doesIncludeNode[0] == True:
                    nodePosInRoute[0] = route.route.index(savingsNodesIdx[0])
                    if (nodePosInRoute[0] == 1 or
                        nodePosInRoute[0] == len(route.route)-2
                        ):
                        doesIncludeNode[0] = False
                        nodesFoundCounter += 1
                        savingsRoutesIdx.append(routeIdx)
                        if nodesFoundCounter == 2:
                            break
                    else:
                        isSavingsPairValid = False
                        break
                # Check if node is in start or end of the route. If false, continue
                # to next iteration
                elif doesIncludeNode[1] == True:
                    nodePosInRoute[1] = route.route.index(savingsNodesIdx[1])
                    if (nodePosInRoute[1] == 1 or
                        nodePosInRoute[1] == len(route.route)-2
                        ):
                        doesIncludeNode[1] = False
                        nodesFoundCounter += 1
                        savingsRoutesIdx.append(routeIdx)
                        if nodesFoundCounter == 2:
                            break
                    else:
                        isSavingsPairValid = False
                        break
                else:
                    isSavingsPairValid = False
                    break
            
            # If not valid, continue to next iteration.
            if isSavingsPairValid == False:
                continue
            
            # Check Capacity constraints, continue to next iteration if not valid
            if not (routes[savingsRoutesIdx[0]].demand + 
                routes[savingsRoutesIdx[1]].demand < self.capacity
                ):
                continue

            # Nodes 1 and 2 should be in start and end of their routes respectively
            # or vice versa
            if(nodePosInRoute[0] == 1 and
                nodePosInRoute[1] == len(routes[savingsRoutesIdx[1]].route)-2
                ):
                rightRoute = routes[savingsRoutesIdx[0]]
                leftRoute = routes[savingsRoutesIdx[1]]
                rightRouteIdx = 0
            elif(nodePosInRoute[1] == 1 and
                nodePosInRoute[0] == len(routes[savingsRoutesIdx[0]].route)-2
                ):
                rightRoute = routes[savingsRoutesIdx[1]]
                leftRoute = routes[savingsRoutesIdx[0]]
                rightRouteIdx = 1
            else:
                # Continue to next iteration since not feasible
                continue

            # remove 0 from end of left route and 0 from start of right route
            # ,then merge routes
            leftRoute.route = leftRoute.route[:-1]
            rightRoute.route = rightRoute.route[1:]
            for node in rightRoute.route:
                leftRoute.route.append(node)
            del rightRoute
            del routes[savingsRoutesIdx[rightRouteIdx]]
            
            self.recalculate_route_demand_cost(leftRoute)
            

        return self.create_solution(routes)

    def __calculateCustomerSavings(self):
        """
        
        """
        class Savings:
            def __init__(self, savings, nodeIdx1, nodeIdx2):
                self.savings = savings
                self.nodesIdx = [nodeIdx1, nodeIdx2]

        savingsList = []
        for i in range(1, self.dimension-1):
            for j in range(i+1, self.dimension):
                if i != j:
                    savingsVal = self.dist[0][i] + self.dist[0][j] - self.dist[i][j]
                    savingsList.append(Savings(savingsVal, i, j))
        return savingsList

    #endregion
    #region random solution, add to route with lowest capacity # this ain't rigth kasi di dapat alam agad yung num of routes
    # def create_random_solution(self):
    #     unserviced = [i for i in range(1, self.dimension)]
    #     random.shuffle(unserviced)
    #     routes = [[0] for i in range(self.minNumVehicles)] #list of all routes
        
    #     route_demand = [0 for i in range(self.minNumVehicles)]
        
    #     debugiterationcount = 0
    #     # iterate through each route
    #     # randomly select an unserviced node to add to that current route
    #     while unserviced:
    #         print('debugiterationcount: ' + str(debugiterationcount))
    #         node = unserviced[0]
    #         sortedRoutes = [route for _,route in sorted(zip(route_demand,routes))]
    #         routes = sortedRoutes
    #         route_demand.sort()

    #         pass
    #         # If the route can still accomodate the node
    #         # cycle through all routes
    #         for i, route in enumerate(routes):
    #             if route_demand[i] + self.listDemand[node] <= self.capacity:
    #                 route += [node]
    #                 route_demand[i] += self.listDemand[node]
    #                 del unserviced[0]
    #                 break
    #         else:
    #             print('no feasible solution found sa create_random_solution')
    #             for route in routes:
    #                 pass
    #                 # shift 1 node from a route to another route to accomodate 
    #                 # the node that cannot be inserted
               
    #         debugiterationcount += 1 
        
    #     final_routes = []
    #     for i in range(len(routes)):
    #         final_routes += [self.create_route(routes[i] + [0])]
    #     return self.create_solution(final_routes)
    #endregion

    #region create random solution, add 1 node per route in each iteration, cycle through routes.
    # def create_random_solution(self):
    #     unserviced = [i for i in range(1, self.dimension)]
    #     random.shuffle(unserviced)
    #     free_routes = [[0] for i in range(self.minNumVehicles)] #list of all routes
    #     final_routes = []
        
    #     free_route_demand = [0 for i in range(self.minNumVehicles)]
    #     final_route_demand = []

    #     free_route_count = self.minNumVehicles
    #     currRoute = 0
        
    #     debugiterationcount = 0
    #     # iterate through each route
    #     # randomly select an unserviced node to add to that current route
    #     while unserviced:
    #         print('debugiterationcount: ' + str(debugiterationcount))
    #         node = unserviced[0]
    #         # If the route can still accomodate the node
    #         if free_route_demand[currRoute] + self.listDemand[node] <= self.capacity:
    #             free_routes[currRoute] += [node]
    #             free_route_demand[currRoute] += self.listDemand[node]
    #             currRoute += 1
    #             if currRoute == free_route_count:
    #                 currRoute = 0
    #             del unserviced[0]
    #         # If the route cannot accomodate the node
    #         else: 
    #             currRoute += 1
    #             if currRoute == free_route_count:
    #                 currRoute = 0
    #             # final_routes += [self.create_route(free_routes[currRoute] + [0])]
    #             # final_route_demand += [free_route_demand[currRoute]]
    #             # del free_routes[currRoute]
    #             # del free_route_demand[currRoute]
    #             # free_route_count -= 1
    #             # if currRoute >= free_route_count:
    #             #     currRoute = 0
    #         debugiterationcount += 1 
    #     if free_route_count > 0:
    #         for i in range(free_route_count):
    #             final_routes += [self.create_route(free_routes[i] + [0])]
    #             final_route_demand += [free_route_demand[i]]

    #     return self.create_solution(final_routes)
    #endregion


    def refresh(self, solution):
        solution.cost, solution.demand = 0, 0
        for route_obj in solution.routes:
            route = route_obj.route
            route_obj.demand, route_obj.cost = 0, 0
            for i in range(0, len(route) - 1):
                route_obj.demand += self.listDemand[route[i]]
                route_obj.cost += self.dist[route[i]][route[i + 1]]
            solution.cost += route_obj.cost
            solution.demand += route_obj.demand
            if route_obj.demand > self.capacity:
                route_obj.is_valid = False
                solution.is_valid = False

    def visualise(self, solution):
        im = Image.new( 'RGB', (500,500), "white") # create a new black image
        draw = ImageDraw.Draw(im)
        color = (0, 0, 0)
        for i, route in enumerate(solution.routes):
            r_c = (i*i)%255
            g_c = (i*r_c)%255
            b_c = (i*g_c)%255
            nodes = route.route
            norm = lambda x, y: (2*x + 250, 2*y + 250)
            draw.line([norm(*self.listCoord[n]) for n in nodes], fill=(r_c, g_c, b_c), width=2)
        return im
    
    def __repr__(self):
        string = {
            "listCoord" : self.listCoord,
            "listDemand" : self.listDemand,
            #"dists"  : self.dist
        }
        return str(string)
    
    def evaluate_solution(self, sol):
        pass
class Solution:
    def __init__(self, routes=[], cost=0, is_valid=False, demand=0):
        self.is_valid = is_valid
        self.routes = routes
        self.cost = cost
        self.demand = demand
        self.penalty = 0

    def shuffle(self):
        random.shuffle(self.routes)

    def remove_node(self, x):
        for route in self.routes:
            if x in route.route:
                route.remove_node(x)
        self.is_valid = False

    def insert_route(self, route_id, route_index, route):
        self.routes[route_id].insert_route(route_index, route)
        self.is_valid = False

    def random_subroute(self):
        r_i = random.randrange(0, len(self.routes))
        while len(self.routes[r_i].route) == 2:
            r_i = random.randrange(0, len(self.routes))
        c_s = random.randrange(1, len(self.routes[r_i].route))
        c_e = c_s
        while c_e == c_s:
            c_e = random.randrange(1, len(self.routes[r_i].route))
        if c_s > c_e:
            c_s, c_e = c_e, c_s
        return self.routes[r_i].route[c_s:c_e]

    def hash(self):
        return hash("-".join([",".join(str(x) for x in x.route) for x in self.routes]))

    def __repr__(self):
        return "\n".join([str(route) for route in self.routes])

class Route:
    def __init__(self, route=[], cost=0, is_valid=False, demand=0):
        self.is_valid = is_valid
        self.route = route
        self.cost = cost
        self.demand = demand

    def insert_route(self, index, route):
        self.is_valid = False
        self.route = self.route[:index + 1] + route + self.route[index + 1:]

    def append_node(self, node):
        self.is_valid = False
        self.route = self.route[:-1] + [node] + [1]

    def remove_node(self, x):
        self.is_valid = False
        del self.route[self.route.index(x)]

    def validate_route(self, CVRPInstance):
        if self.route[0] != CVRPInstance.start_node:
            return None
        cost = 0
        demand = 0
        is_valid = True

        for i in range(1, len(self.route)):
            n1, n2 = self.route[i - 1], self.route[i]
            cost += CVRPInstance.dist[n1][n2]
            demand += CVRPInstance.listDemand[n2]
        if demand > CVRPInstance.capacity:
            is_valid = False

        return is_valid

    def __repr__(self):
        debug_str = ", cost = " + str(self.cost) + ", demand = " + str(self.demand)
        ret_str = "->".join(str(n) for n in self.route)
        return ret_str + (debug_str if False else "")

    

    


