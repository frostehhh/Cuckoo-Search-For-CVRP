import pandas as pd
import os
import regex as re
import Parser as p
import numpy as np
import math
from CVRP import CVRPInfo as CVRP
from CuckooSearchCVRP import CuckooSearch

experimentData = []
instanceData = []

#region Load Datasets
DataSetAPath = 'data/A-VRP/'
DataSetBPath = 'data/B-VRP/'
DataSetPPath = 'data/P-VRP/'

DataSetA = os.listdir(DataSetAPath) # list of file names of benchmark instances from Set A
DataSetB = os.listdir(DataSetBPath) # list of file names of benchmark instances from Set B
DataSetP = os.listdir(DataSetPPath) # list of file names of benchmark instances from Set P
#end region

ResultsSetAPath = 'finalresults/A-VRP/'
ResultsSetBPath = 'finalresults/B-VRP/'
ResultsSetPPath = 'finalresults/P-VRP/'

ResultsSetAPath = 'results/A-VRP/'
ResultsSetBPath = 'results/B-VRP/'
ResultsSetPPath = 'results/P-VRP/'



#region definitions
def initializeInstanceData():
       return {'Name':[],
        'Best Solution Cost':[],
        'Optimal Value':[],
        'Run Time':[]
        } 
def initializeExperimentData(name=None, optVal=None, minSolCost=None,
        maxSolCost=None, avgSolCost=None, stdSolCost=None, avgRunTime=None):
        if name is None:
                return {'Name':[],
                'Optimal Value':[],
                'Minimum Solution Cost':[],
                'Max Solution Cost':[],
                'Avg Solution Cost':[],
                'Std of Solution Cost':[],
                'Avg Run Time':[]
                } 
        else:
                return {'Name':[name],
                'Optimal Value':[optVal],
                'Minimum Solution Cost':[minSolCost],
                'Max Solution Cost':[maxSolCost],
                'Avg Solution Cost':[avgSolCost],
                'Std of Solution Cost':[stdSolCost],
                'Avg Run Time':[avgRunTime]
                }  
def appendRowToInstanceDf(df, row):
        df['Name'] += [row['Name']]
        df['Best Solution Cost'] += [row['Best Solution Cost']]
        df['Optimal Value'] += [row['Optimal Value']]
        df['Run Time'] += [row['Run Time']]
def appendRowToExperimentDf(df, row):
        df['Name'] += row['Name']
        df['Optimal Value'] += row['Optimal Value']
        df['Minimum Solution Cost'] += row['Minimum Solution Cost']
        df['Max Solution Cost'] += row['Max Solution Cost']
        df['Avg Solution Cost'] += row['Avg Solution Cost']
        df['Std of Solution Cost'] += row['Std of Solution Cost']
        df['Avg Run Time'] += row['Avg Run Time']
def calculateInstanceResults(instanceData):
        minSolCost = math.inf
        maxSolCost = 0
        avgSolCost = 0
        stdSolCost = 0
        avgRunTime = 0

        listSolCost = []
        listRunTime = []

        for i in range(len(instanceData['Name'])):
                if instanceData['Best Solution Cost'][i] < minSolCost:
                        minSolCost = instanceData['Best Solution Cost'][i]
                if instanceData['Best Solution Cost'][i] > maxSolCost:
                        maxSolCost = instanceData['Best Solution Cost'][i]
                listSolCost.append(instanceData['Best Solution Cost'][i])
                listRunTime.append(instanceData['Run Time'][i])

        avgSolCost = np.average(listSolCost)
        stdSolCost = np.std(listSolCost)
        avgRunTime = np.average(listRunTime)
        print()
        data = initializeExperimentData(instanceData['Name'][0],instanceData['Optimal Value'][0]
                ,minSolCost, maxSolCost, avgSolCost, stdSolCost, avgRunTime)
        print()
        return data
def saveResultsToCsv(df, path):
        df = pd.DataFrame(df)
        # write to results.csv
        fileNum = 0
        while True:
                if fileNum < 10:
                        _ = '0' + str(fileNum)
                else:
                        _ = str(fileNum)
                if os.path.exists(path + 'results' + path[13] + _ + '.csv'):
                        fileNum += 1
                        continue
                else:
                        df.to_csv(path + 'results' + path[13] + _ + '.csv')
                        print('Saved ' + 'results' + path[13] + _ + '.csv')
                        break
# def saveResultsInfoTxt(string, path):
#         fileNum = 0
#         while True:
#                 if fileNum < 10:
#                         _ = '0' + str(fileNum)
#                 else:
#                         _ = str(fileNum)
#                 if os.path.exists(path + 'results' + path[8] + _ + '.csv'):
#                         fileNum += 1
#                         continue
#                 else:
#                         df.to_csv(path + 'results' + path[8] + _ + '.csv')
#                         print('Saved ' + 'results' + path[8] + _ + '.csv')
#                         break
#         f = open("results.txt","w+")
#endregion

#region Initialize Parameters
#Initialize Cuckoo SearchParameters
numNests = 15
Pa = 0.25 # Fraction of worse solutions to be replaced
Pc = 0.6 # Fraction of cuckoos performing Levy Flights
maxGenerations = 1000# maximum number of iterations
stopCriterion = maxGenerations # attempt limit of successive iterations

print('Parameters: numNests = ' + str(numNests) + ' Pa = ' + str(Pa) + ' Pc = ' + str(Pc) +
' maxGenerations: ' + str(maxGenerations) + ' stopCriterion = ' + str(stopCriterion))

#region iterate once
data = []
data = initializeInstanceData()
for dataset in DataSetA:
        CVRPInstance = CVRP(DataSetAPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()
        appendRowToInstanceDf(data, solver.readData())
saveResultsToCsv(data, ResultsSetAPath)

data = initializeInstanceData()
for dataset in DataSetB:
        CVRPInstance = CVRP(DataSetBPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()
        appendRowToInstanceDf(data, solver.readData())
saveResultsToCsv(data, ResultsSetBPath)

data = initializeInstanceData()
for dataset in DataSetP:
        CVRPInstance = CVRP(DataSetPPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()
        appendRowToInstanceDf(data, solver.readData())
saveResultsToCsv(data, ResultsSetPPath)
#endregion
#region iterate 30 times
# numIter = 30

# experimentData = initializeExperimentData()
# instanceData = initializeInstanceData()
# for dataset in DataSetA:
#         instanceData = initializeInstanceData()
#         for i in range(numIter):
#                 CVRPInstance = CVRP(DataSetAPath + dataset) #pass data to CVRP       
#                 solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
#                 solver.solveInstance()
#                 appendRowToInstanceDf(instanceData, solver.readData())
#         row = calculateInstanceResults(instanceData)
#         appendRowToExperimentDf(experimentData, row)
# saveResultsToCsv(experimentData, ResultsSetAPath)

# experimentData = initializeExperimentData()
# instanceData = initializeInstanceData()
# for dataset in DataSetB:
#         instanceData = initializeInstanceData()
#         for i in range(numIter):
#                 CVRPInstance = CVRP(DataSetBPath + dataset) #pass data to CVRP       
#                 solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
#                 solver.solveInstance()
#                 appendRowToInstanceDf(instanceData, solver.readData())
#         row = calculateInstanceResults(instanceData)
#         appendRowToExperimentDf(experimentData, row)
# saveResultsToCsv(experimentData, ResultsSetBPath)


# experimentData = initializeExperimentData()
# instanceData = initializeInstanceData()
# for dataset in DataSetP:
#         instanceData = initializeInstanceData()
#         for i in range(numIter):
#                 CVRPInstance = CVRP(DataSetPPath + dataset) #pass data to CVRP       
#                 solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
#                 solver.solveInstance()
#                 appendRowToInstanceDf(instanceData, solver.readData())
#         row = calculateInstanceResults(instanceData)
#         appendRowToExperimentDf(experimentData, row)
# saveResultsToCsv(experimentData, ResultsSetAPath)


#endregion



