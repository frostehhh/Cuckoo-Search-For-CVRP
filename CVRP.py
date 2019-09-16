import os
import math
import random
import threading
from PIL import Image, ImageDraw
import Parser as p

class CVRPInfo():
    def __init__(self, data_file):
        self.read_data(data_file)
        self.__compute_dists()
        self.start_node = 0
        self.solutions = [] 
        # self.debug = debug
        # self.max_route_len = 10 # I don't need a max route limiter
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
        visited = set()
        for route in routes:
            if not route.is_valid:
                is_valid = False
            for x in route.route:
                visited.add(x)
            cost += route.cost
            demand += route.demand
        # if len(visited) != self.dimension - 1: # I ADDED THIS, remove depot node from visited.
        #     print("NOT ALL VISITED")
        #     print(visited)
        sol = Solution(cost=cost, demand=demand, is_valid=is_valid, routes=routes)
        # print('DEBUG: Created solution of' + self.fileName)
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
    
    def create_random_solution(self):
        unserviced = [i for i in range(1, self.dimension)]
        random.shuffle(unserviced)
        routes = []
        cur_route = [0] # start with depot node
        route_demand = 0
        route_length = 0
        while unserviced:
            i = 0
            node = unserviced[i]
            if route_demand + self.listDemand[node] <= self.capacity:
                cur_route += [node]
                route_length += 1
                route_demand += self.listDemand[node]
                del unserviced[i]
                continue
            cur_route += [0] # end with depot node
            routes += [self.create_route(cur_route)]
            
            # Reset variables for next iteration
            cur_route = [0] 
            route_demand = 0
            route_length = 0
        routes += [self.create_route(cur_route + [0])]
        return self.create_solution(routes)

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
        self.listDemand = demand
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

    

    


