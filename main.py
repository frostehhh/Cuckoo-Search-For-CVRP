import pandas as pd
import os
import regex as re
import Parser as p
import numpy as np
from CVRP import CVRPInfo as CVRP
from CuckooSearchCVRP import CuckooSearch

#region Initialize Parameters
#Initialize Cuckoo SearchParameters
numNests = 15
Pa = 0.25 # Fraction of worse solutions to be replaced
Pc = 0.6 # Fraction of cuckoos performing Levy Flights
maxGenerations = 1 # maximum number of iterations
stopCriterion = maxGenerations # attempt limit of successive iterations

#region Load Datasets
DataSetAPath = 'data/A-VRP/'
DataSetBPath = 'data/B-VRP/'
DataSetPPath = 'data/P-VRP/'

DataSetA = os.listdir(DataSetAPath) # list of file names of benchmark instances from Set A
DataSetB = os.listdir(DataSetBPath) # list of file names of benchmark instances from Set B
DataSetP = os.listdir(DataSetPPath) # list of file names of benchmark instances from Set P
#end region

ResultsSetAPath = 'results/A-VRP/'

data = {'Name':[],
        'Best Solution Cost':[],
        'Optimal Value':[],
        'Run Time':[]
        }

print('Parameters: numNests = ' + str(numNests) + ' Pa = ' + str(Pa) + ' Pc = ' + str(Pc) +
' maxGenerations: ' + str(maxGenerations) + ' stopCriterion = ' + str(stopCriterion))

# def __init__(self, CVRPInstance, numCuckoos = 20, Pa = 0.2, Pc = 0.6, generations = 5000, pdf_type = 'levy'):
for dataset in DataSetA:
        CVRPInstance = CVRP(DataSetAPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()
        _ = solver.readData()
        data['Name'] += [_['Name']]
        data['Best Solution Cost'] += [_['Best Solution Cost']]
        data['Optimal Value'] += [_['Optimal Value']]
        data['Run Time'] += [_['Run Time']]
df = pd.DataFrame(data)

# write to results.csv
fileNum = 0
while True:
        if fileNum < 0:
                _ = '0' + str(fileNum)
        else:
                _ = str(fileNum)
        if os.path.exists(ResultsSetAPath + 'results' + _ + '.csv'):
                fileNum += 1
                continue
        else:
                df.to_csv(ResultsSetAPath + 'results' + _ + '.csv')
                break

for dataset in DataSetB:
        CVRPInstance = CVRP(DataSetBPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()

# This dataset contains instances where vehicles will need multiple trips
for dataset in DataSetP:
        CVRPInstance = CVRP(DataSetPPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()




