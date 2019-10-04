import pandas as pd
import os
import Parser as p
import experiment as exp
from CVRP import CVRPInfo as CVRP
from CuckooSearchCVRP import CuckooSearch
from CuckooSearchCVRP import LevyCombinationTypes
from CuckooSearchCVRP import Neighborhoods

class CSRunner:
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
        finalResultsPath = 'finalresults/'

        #Initialize Cuckoo SearchParameters
        numNests = 15
        Pa = 0.25 # Fraction of worse solutions to be replaced
        Pc = 0.6 # Fraction of cuckoos performing Levy Flights
        maxGenerations = 500# maximum number of iterations
        stopCriterion = maxGenerations # attempt limit of successive iterations

        

        def __init__(self, combinationType, neighborhood, fileName):
                self.combiType = combinationType
                self.listNeighbor = neighborhood
                self.fileName = fileName
                self.performImplementation()

        def performImplementation(self):
                print('Parameters: numNests = ' + str(self.numNests) + ' Pa = ' + str(self.Pa) + ' Pc = ' + str(self.Pc) +
                ' maxGenerations: ' + str(self.maxGenerations) + ' stopCriterion = ' + str(self.stopCriterion))

                #region iterate 30 times
                numIter = 30

                experimentData = exp.initializeExperimentData()
                instanceData = exp.initializeInstanceData()
                for dataset in self.DataSetA:
                        instanceData = exp.initializeInstanceData()
                        for i in range(numIter):
                                CVRPInstance = CVRP(self.DataSetAPath + dataset) #pass data to CVRP       
                                solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = self.numNests, Pa = self.Pa, 
                                        Pc = self.Pc, generations = self.maxGenerations, combinationType = self.combiType, neighborhoods=self.listNeighbor)
                                solver.solveInstance()
                                exp.appendRowToInstanceDf(instanceData, solver.readData())
                        row = exp.calculateInstanceResults(instanceData)
                        exp.appendRowToExperimentDf(experimentData, row)

                for dataset in self.DataSetB:
                        instanceData = exp.initializeInstanceData()
                        for i in range(numIter):
                                CVRPInstance = CVRP(self.DataSetBPath + dataset) #pass data to CVRP       
                                solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = self.numNests, Pa = self.Pa, 
                                        Pc = self.Pc, generations = self.maxGenerations, combinationType = self.combiType, neighborhoods=self.listNeighbor)
                                solver.solveInstance()
                                exp.appendRowToInstanceDf(instanceData, solver.readData())
                        row = exp.calculateInstanceResults(instanceData)
                        exp.appendRowToExperimentDf(experimentData, row)

                for dataset in self.DataSetP:
                        instanceData = exp.initializeInstanceData()
                        for i in range(numIter):
                                CVRPInstance = CVRP(self.DataSetPPath + dataset) #pass data to CVRP       
                                solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = self.numNests, Pa = self.Pa, 
                                        Pc = self.Pc, generations = self.maxGenerations, combinationType = self.combiType, neighborhoods=self.listNeighbor)
                                solver.solveInstance()
                                exp.appendRowToInstanceDf(instanceData, solver.readData())
                        row = exp.calculateInstanceResults(instanceData)
                        exp.appendRowToExperimentDf(experimentData, row)
                exp.saveResultsToCsv(experimentData, self.finalResultsPath, self.fileName, type='finalresults')


                #endregion

                #region iterate once
                # fileNameSuffix = 'crossTwoOpt_reinsertion_swap22_5050_levy4_levy5_30000'
                # data = []
                # data = exp.initializeInstanceData()
                # for dataset in DataSetA:
                #         CVRPInstance = CVRP(DataSetAPath + dataset) #pass data to CVRP       
                #         solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
                #         solver.solveInstance()
                #         exp.appendRowToInstanceDf(data, solver.readData())
                # exp.saveResultsToCsv(data, ResultsSetAPath, fileNameSuffix)

                # for dataset in DataSetB:
                #         CVRPInstance = CVRP(DataSetBPath + dataset) #pass data to CVRP       
                #         solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
                #         solver.solveInstance()
                #         exp.appendRowToInstanceDf(data, solver.readData())
                # # exp.saveResultsToCsv(data, ResultsSetBPath, fileNameSuffix)

                # for dataset in DataSetP:
                #         CVRPInstance = CVRP(DataSetPPath + dataset) #pass data to CVRP       
                #         solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
                #         solver.solveInstance()
                #         exp.appendRowToInstanceDf(data, solver.readData())
                # exp.saveResultsToCsv(data, ResultsPath, fileNameSuffix, type='results')
                #endregion

