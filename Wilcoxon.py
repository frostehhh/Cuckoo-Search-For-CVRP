from scipy.stats import wilcoxon
import pandas as pd
from experiment import appendRowToWilcoxonDf
from experiment import initializeWilcoxonDf
from experiment import saveResultsToCsv
import numpy as np

#region Variable Initialization
sourcePath = 'newFinalResults/'
sourceFileName = 'FinalResultsPerRun - Compiled Csv'
resultsPath = 'newFinalResults/'
resultsPerInstanceFileName = 'WilcoxonPerInstanceFinal'
resultsPerDatasetFilename = 'WilcoxonPerDatasetFinal'
resultsPerImplementationFileName = 'WilcoxonPerImplementationFinal'

data = pd.read_csv(sourcePath + sourceFileName + '.csv', header=[0], index_col=0)
implementationList = data.Implementation.unique()
instanceList = data.Name.unique()
implementationRange = range(len(implementationList))
instanceLength = len(instanceList)
instanceRange = range(instanceLength)
datasetACount = 27
datasetBCount = 23
datasetPCount = 24

# DataFrame Variables
df1 = None
df2 = None
WilcoxonPerInstanceDf = initializeWilcoxonDf()
WilcoxonPerDatasetDf = initializeWilcoxonDf()
WilcoxonPerImplementationDf = initializeWilcoxonDf()

minSolCost = None
avgSolCost = None
stdSolCost = None
avgRuntime = None
p_value = None

instanceName = ""
implementation1Name = ""
implementation2Name = ""
optimalValue = 0
# for adding new rows to the WilcoxonDf
row = {}
#endregion

#region TESTING 
# df1 = data.loc[data["Implementation"] == '2-opt, shift-1, double-bridge']
# df1_data = df1["Best Solution Cost"].tolist()

# print(df1.head())
# print(implementationRange)
#endregion



# Iterate through every possible pair of implementations
for i in implementationRange[:-1]:
    for j in implementationRange[i+1:]:
        # compare i and j
        # iterate through every instance of implementations i and j
        for k in instanceRange:
            instanceName = instanceList[k]
            implementation1Name = implementationList[i]
            implementation2Name = implementationList[j]
            
            # In each implementation, get rows for the current instance
            df1 = data.loc[lambda data: (data["Name"] == instanceName) & (data["Implementation"] == implementation1Name)]
            df2 = data.loc[lambda data: (data["Name"] == instanceName) & (data["Implementation"] == implementation2Name)]
            

            optimalValue = df1.iloc[0, 2]
            df1_solutionCostList = df1["Best Solution Cost"].tolist()
            df2_solutionCostList = df2["Best Solution Cost"].tolist()
            df1_runtimeList = df1["Run Time"].tolist()
            df2_runtimeList = df2["Run Time"].tolist()
        
            try:
                _, p_value = wilcoxon(x = df1_solutionCostList, y = df2_solutionCostList)
            except: 
                print("Error with acquiring wilcoxon p-value")
            
            minSolCost = [min(df1_solutionCostList), min(df2_solutionCostList)]
            avgSolCost = [np.average(df1_solutionCostList), np.average(df2_solutionCostList)]
            stdSolCost = [np.std(df1_solutionCostList), np.std(df2_solutionCostList)]
            avgRuntime = [np.average(df1_runtimeList), np.average(df2_runtimeList)]

            # build the resulting WilcoxonPerInstanceDf
            row = {
                'Instance': instanceList[k],
                'Optimal Value': optimalValue,
                'Implementation 1': implementation1Name,
                'Minimum Solution Cost 1': minSolCost[0],
                'Average Solution Cost 1': avgSolCost[0],
                'Std Solution Cost 1': stdSolCost[0],
                'Average Runtime 1': avgRuntime[0],
                'Implementation 2': implementation2Name,
                'Minimum Solution Cost 2': minSolCost[1],
                'Average Solution Cost 2': avgSolCost[1],
                'Std Solution Cost 2': stdSolCost[1],
                'Average Runtime 2': avgRuntime[1],
                'P-value': p_value
            }
            appendRowToWilcoxonDf(WilcoxonPerInstanceDf, row)
        
        # build the resulting WilcoxonPerDatasetDf
        setAMinBound = -instanceLength
        setAMaxBound = -instanceLength + datasetACount
        setBMinBound = setAMaxBound
        setBMaxBound = setAMaxBound + datasetBCount
        setPMinBound = setBMaxBound
        setAOptimalAvg = 1045
        setBOptimalAvg = 971
        setPOptimalAvg = 576
        datasetOptimalAvg = 870
        # setPMaxBound = setBMaxBound + datasetPCount
        
        # Set A
        test = instanceList[setAMinBound:setAMaxBound]
        test = instanceList[setBMinBound:setBMaxBound]
        test = instanceList[setPMinBound:]
        try:
            _, p_value = wilcoxon(x = WilcoxonPerInstanceDf['Average Solution Cost 1'][setAMinBound:setAMaxBound],
                                     y = WilcoxonPerInstanceDf['Average Solution Cost 2'][setAMinBound:setAMaxBound])
        except: 
            print("Error with acquiring wilcoxon p-value")

        row = {
            'Instance': "Set A",
            'Optimal Value': setAOptimalAvg,
            'Implementation 1': implementation1Name,
            'Minimum Solution Cost 1': np.average(WilcoxonPerInstanceDf['Minimum Solution Cost 1'][setAMinBound:setAMaxBound]),
            'Average Solution Cost 1': np.average(WilcoxonPerInstanceDf['Average Solution Cost 1'][setAMinBound:setAMaxBound]),
            'Std Solution Cost 1': np.average(WilcoxonPerInstanceDf['Std Solution Cost 1'][setAMinBound:setAMaxBound]),
            'Average Runtime 1': np.average(WilcoxonPerInstanceDf['Average Runtime 1'][setAMinBound:setAMaxBound]),
            'Implementation 2': implementation2Name,
            'Minimum Solution Cost 2': np.average(WilcoxonPerInstanceDf['Minimum Solution Cost 2'][setAMinBound:setAMaxBound]),
            'Average Solution Cost 2': np.average(WilcoxonPerInstanceDf['Average Solution Cost 2'][setAMinBound:setAMaxBound]),
            'Std Solution Cost 2': np.average(WilcoxonPerInstanceDf['Std Solution Cost 2'][setAMinBound:setAMaxBound]),
            'Average Runtime 2': np.average(WilcoxonPerInstanceDf['Average Runtime 2'][setAMinBound:setAMaxBound]),
            'P-value': p_value
        }
        appendRowToWilcoxonDf(WilcoxonPerDatasetDf, row)

        # Set B
        try:
            _, p_value = wilcoxon(x = WilcoxonPerInstanceDf['Average Solution Cost 1'][setBMinBound:setBMaxBound],
                                     y = WilcoxonPerInstanceDf['Average Solution Cost 2'][setBMinBound:setBMaxBound])
        except: 
            print("Error with acquiring wilcoxon p-value")

        row = {
            'Instance': "Set B",
            'Optimal Value': setBOptimalAvg,
            'Implementation 1': implementation1Name,
            'Minimum Solution Cost 1': np.average(WilcoxonPerInstanceDf['Minimum Solution Cost 1'][setBMinBound:setBMaxBound]),
            'Average Solution Cost 1': np.average(WilcoxonPerInstanceDf['Average Solution Cost 1'][setBMinBound:setBMaxBound]),
            'Std Solution Cost 1': np.average(WilcoxonPerInstanceDf['Std Solution Cost 1'][setBMinBound:setBMaxBound]),
            'Average Runtime 1': np.average(WilcoxonPerInstanceDf['Average Runtime 1'][setBMinBound:setBMaxBound]),
            'Implementation 2': implementation2Name,
            'Minimum Solution Cost 2': np.average(WilcoxonPerInstanceDf['Minimum Solution Cost 2'][setBMinBound:setBMaxBound]),
            'Average Solution Cost 2': np.average(WilcoxonPerInstanceDf['Average Solution Cost 2'][setBMinBound:setBMaxBound]),
            'Std Solution Cost 2': np.average(WilcoxonPerInstanceDf['Std Solution Cost 2'][setBMinBound:setBMaxBound]),
            'Average Runtime 2': np.average(WilcoxonPerInstanceDf['Average Runtime 2'][setBMinBound:setBMaxBound]),
            'P-value': p_value
        }
        appendRowToWilcoxonDf(WilcoxonPerDatasetDf, row)

        # Set P
        try:
            _, p_value = wilcoxon(x = WilcoxonPerInstanceDf['Average Solution Cost 1'][setPMinBound:],
                                     y = WilcoxonPerInstanceDf['Average Solution Cost 2'][setPMinBound:])
        except: 
            print("Error with acquiring wilcoxon p-value")

        row = {
            'Instance': "Set P",
            'Optimal Value': setPOptimalAvg,
            'Implementation 1': implementation1Name,
            'Minimum Solution Cost 1': np.average(WilcoxonPerInstanceDf['Minimum Solution Cost 1'][setPMinBound:]),
            'Average Solution Cost 1': np.average(WilcoxonPerInstanceDf['Average Solution Cost 1'][setPMinBound:]),
            'Std Solution Cost 1': np.average(WilcoxonPerInstanceDf['Std Solution Cost 1'][setPMinBound:]),
            'Average Runtime 1': np.average(WilcoxonPerInstanceDf['Average Runtime 1'][setPMinBound:]),
            'Implementation 2': implementation2Name,
            'Minimum Solution Cost 2': np.average(WilcoxonPerInstanceDf['Minimum Solution Cost 2'][setPMinBound:]),
            'Average Solution Cost 2': np.average(WilcoxonPerInstanceDf['Average Solution Cost 2'][setPMinBound:]),
            'Std Solution Cost 2': np.average(WilcoxonPerInstanceDf['Std Solution Cost 2'][setPMinBound:]),
            'Average Runtime 2': np.average(WilcoxonPerInstanceDf['Average Runtime 2'][setPMinBound:]),
            'P-value': p_value
        }
        appendRowToWilcoxonDf(WilcoxonPerDatasetDf, row)

        #build the resulting WilcoxonPerImplementationDf
        try:
            _, p_value = wilcoxon(x = WilcoxonPerInstanceDf['Average Solution Cost 1'][-instanceLength:],
                                     y = WilcoxonPerInstanceDf['Average Solution Cost 2'][-instanceLength:])
        except: 
            print("Error with acquiring wilcoxon p-value")

        row = {
            'Instance': "",
            'Optimal Value': datasetOptimalAvg,
            'Implementation 1': implementation1Name,
            'Minimum Solution Cost 1': np.average(WilcoxonPerInstanceDf['Minimum Solution Cost 1'][-instanceLength:]),
            'Average Solution Cost 1': np.average(WilcoxonPerInstanceDf['Average Solution Cost 1'][-instanceLength:]),
            'Std Solution Cost 1': np.average(WilcoxonPerInstanceDf['Std Solution Cost 1'][-instanceLength:]),
            'Average Runtime 1': np.average(WilcoxonPerInstanceDf['Average Runtime 1'][-instanceLength:]),
            'Implementation 2': implementation2Name,
            'Minimum Solution Cost 2': np.average(WilcoxonPerInstanceDf['Minimum Solution Cost 2'][-instanceLength:]),
            'Average Solution Cost 2': np.average(WilcoxonPerInstanceDf['Average Solution Cost 2'][-instanceLength:]),
            'Std Solution Cost 2': np.average(WilcoxonPerInstanceDf['Std Solution Cost 2'][-instanceLength:]),
            'Average Runtime 2': np.average(WilcoxonPerInstanceDf['Average Runtime 2'][-instanceLength:]),
            'P-value': p_value
        }
        appendRowToWilcoxonDf(WilcoxonPerImplementationDf, row)
# saveResultsToCsv(WilcoxonPerInstanceDf, resultsPath, resultsPerInstanceFileName)
saveResultsToCsv(WilcoxonPerDatasetDf, resultsPath, resultsPerDatasetFilename)
# saveResultsToCsv(WilcoxonPerImplementationDf, resultsPath, resultsPerImplementationFileName)


        