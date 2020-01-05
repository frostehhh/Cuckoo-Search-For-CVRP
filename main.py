import pandas as pd
import os
import Parser as p
import experiment as exp
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

ResultsPath = 'results/'
FinalResultsPath = 'finalresults/'

#Initialize Cuckoo SearchParameters
numNests = 15
Pa = 0.25 # Fraction of worse solutions to be replaced
Pc = 0.6 # Fraction of cuckoos performing Levy Flights
maxGenerations = 1000# maximum number of iterations
stopCriterion = maxGenerations/5 # attempt limit of successive iterations

print('Parameters: numNests = ' + str(numNests) + ' Pa = ' + str(Pa) + ' Pc = ' + str(Pc) +
' maxGenerations: ' + str(maxGenerations) + ' stopCriterion = ' + str(stopCriterion))


numIter = 30
fileNameSuffix = 'results00_crossTwoOpt_reinsertion_shift1_swap22_333_levy4_levy5'

experimentData = exp.initializeExperimentData()
instanceData = exp.initializeInstanceData()
for dataset in DataSetA:
        instanceData = exp.initializeInstanceData()
        for i in range(numIter):
                CVRPInstance = CVRP(DataSetAPath + dataset) #pass data to CVRP       
                solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations, stopCriterion = stopCriterion)
                solver.solveInstance()
                exp.appendRowToInstanceDf(instanceData, solver.readData())
        row = exp.calculateInstanceResults(instanceData)
        exp.appendRowToExperimentDf(experimentData, row)
# exp.saveResultsToCsv(experimentData, FinalResultsSetAPath, fileNameSuffix, type='finalresults')

for dataset in DataSetB:
        instanceData = exp.initializeInstanceData()
        for i in range(numIter):
                CVRPInstance = CVRP(DataSetBPath + dataset) #pass data to CVRP       
                solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations, stopCriterion = stopCriterion)
                solver.solveInstance()
                exp.appendRowToInstanceDf(instanceData, solver.readData())
        row = exp.calculateInstanceResults(instanceData)
        exp.appendRowToExperimentDf(experimentData, row)
# exp.saveResultsToCsv(experimentData, FinalResultsSetBPath, fileNameSuffix, type='finalresults')


for dataset in DataSetP:
        instanceData = exp.initializeInstanceData()
        for i in range(numIter):
                CVRPInstance = CVRP(DataSetPPath + dataset) #pass data to CVRP       
                solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations, stopCriterion = stopCriterion)
                solver.solveInstance()
                exp.appendRowToInstanceDf(instanceData, solver.readData())
        row = exp.calculateInstanceResults(instanceData)
        exp.appendRowToExperimentDf(experimentData, row)
# exp.saveResultsToCsv(experimentData, FinalResultsSetPPath, fileNameSuffix, type='finalresults')
exp.saveResultsToCsv(experimentData, FinalResultsPath, fileNameSuffix, type='finalresults')

