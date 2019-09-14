import pandas as pd
import os
import regex as re
import Parser as p

#region Initialize Parameters
#Initialize Cuckoo SearchParameters
numNests = 25
Pa = 0.25 # Fraction of worse solutions to be replaced
Pc = 0.6 # Fraction of cuckoos performing Levy Flights
maxGenerations = 5000 # maximum number of iterations
stopCriteration = maxGenerations / 5 # attempt limit of successive iterations

#Initialize CVRP Parameters

Tol = 1.0e-5 # Tolerance

#endregion

#region Load Datasets
DataSetAPath = 'data/A-VRP/'
DataSetBPath = 'data/B-VRP/'
DataSetPPath = 'data/P-VRP/'

DataSetA = os.listdir(DataSetAPath) # list of file names of benchmark instances from Set A
DataSetB = os.listdir(DataSetBPath) # list of file names of benchmark instances from Set B
DataSetP = os.listdir(DataSetPPath) # list of file names of benchmark instances from Set P
#end region

#region Main
#load all datasets from Set A
for dataset in DataSetA:
        listCoord, listDemand, InstanceData = p.parse_file(DataSetAPath + dataset)
        print(listCoord)
        print(listDemand)
        print(InstanceData)

# Capacity = 
# Node_Coordinates = []
# Node_Demand = []

#endregion
