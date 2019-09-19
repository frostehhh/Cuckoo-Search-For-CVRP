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
Pc = 1 # Fraction of cuckoos performing Levy Flights
maxGenerations = 500# maximum number of iterations
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
ResultsSetBPath = 'results/B-VRP/'
ResultsSetPPath = 'results/P-VRP/'

data = []

def initializeData():
       return {'Name':[],
        'Best Solution Cost':[],
        'Optimal Value':[],
        'Run Time':[]
        } 


def appendRowToDf(df, row):
        df['Name'] += [row['Name']]
        df['Best Solution Cost'] += [row['Best Solution Cost']]
        df['Optimal Value'] += [row['Optimal Value']]
        df['Run Time'] += [row['Run Time']]


def saveResultsToCsv(df, path):
        df = pd.DataFrame(data)
        # write to results.csv
        fileNum = 0
        while True:
                if fileNum < 10:
                        _ = '0' + str(fileNum)
                else:
                        _ = str(fileNum)
                if os.path.exists(path + 'results' + path[8] + _ + '.csv'):
                        fileNum += 1
                        continue
                else:
                        df.to_csv(path + 'results' + path[8] + _ + '.csv')
                        print('Saved ' + 'results' + path[8] + _ + '.csv')
                        break


print('Parameters: numNests = ' + str(numNests) + ' Pa = ' + str(Pa) + ' Pc = ' + str(Pc) +
' maxGenerations: ' + str(maxGenerations) + ' stopCriterion = ' + str(stopCriterion))

data = initializeData()
for dataset in DataSetA:
        CVRPInstance = CVRP(DataSetAPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()
        appendRowToDf(data, solver.readData())
saveResultsToCsv(data, ResultsSetAPath)

data = initializeData()
for dataset in DataSetB:
        CVRPInstance = CVRP(DataSetBPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()
        appendRowToDf(data, solver.readData())
saveResultsToCsv(data, ResultsSetBPath)

data = initializeData()
for dataset in DataSetP:
        CVRPInstance = CVRP(DataSetPPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()
        appendRowToDf(data, solver.readData())
saveResultsToCsv(data, ResultsSetPPath)




