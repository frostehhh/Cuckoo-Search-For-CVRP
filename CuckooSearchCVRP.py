from CVRP import CVRPInfo as CVRP

class CuckooSearch:
    def __init__(self, CVRPInstance, Pa = 0.2, Pc = 0.6, generations = 5000, pdf_type = 'levy'):
        self.instance = CVRPInstance
        self.Pa = Pa
        self.Pc = Pc
        self.generations = generations
        self.pdf_type = pdf_type
        self.solveInstance()

    def solveInstance(self):
        self.instance.create_random_solution # Initialize Solution
        return str('test')
        # Search, and Evaluate

    def __repr__(self):
        pass
        # return filename, 
        # string = {
        #     "Name" : self.instance.,
        #     "listDemand" : self.listDemand,
        #     #"dists"  : self.dist
        # }
        # return str(string)