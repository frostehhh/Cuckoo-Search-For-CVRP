import pandas as pd
import os
import Parser as p
import experiment as exp
from CVRP import CVRPInfo as CVRP
from CuckooSearchCVRP import CuckooSearch

dataPerInstance = []
instanceData = []

#region Load Datasets
DataSetPath = 'data/FinalDataset/'
DataSet = os.listdir(DataSetPath) # list of file names of of instances from 
#end region

finalResultsPath = 'FinalResults/'

#Initialize Cuckoo SearchParameters
numNests = 15
Pa = 0.25 # Fraction of worse solutions to be replaced
Pc = 0.6 # Fraction of cuckoos performing Levy Flights
maxGenerations = 1000# maximum number of iterations
stopCriterion = maxGenerations/5 # attempt limit of successive iterations

print('Parameters: numNests = ' + str(numNests) + ' Pa = ' + str(Pa) + ' Pc = ' + str(Pc) +
' maxGenerations: ' + str(maxGenerations) + ' stopCriterion = ' + str(stopCriterion))

numIter = 30
fileName = 'FinalResultstesting'
implementationName = '2-opt, reinsertion, swap-2-2'

dataPerInstance = exp.initializeExperimentData()
instanceData = exp.initializeInstanceData()
dataPerRun = exp.initializeInstanceData()
for dataset in DataSet:
        instanceData = exp.initializeInstanceData()
        for i in range(numIter):
                CVRPInstance = CVRP(DataSetPath + dataset) #pass data to CVRP       
                solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations, stopCriterion = stopCriterion)
                solver.solveInstance()
                exp.appendRowToInstanceDf(instanceData, solver.readData())
                exp.appendRowToInstanceDf(dataPerRun, solver.readData())
                dataPerRun["Implementation"] = implementationName
        row = exp.calculateInstanceResults(instanceData)
        exp.appendRowToExperimentDf(dataPerInstance, row)
        dataPerInstance["Implementation"] = implementationName
exp.saveResultsToCsv(dataPerRun, finalResultsPath, fileName + 'PerRun', type='merge')
exp.saveResultsToCsv(dataPerInstance, finalResultsPath, fileName + 'PerInstance', type='merge')

