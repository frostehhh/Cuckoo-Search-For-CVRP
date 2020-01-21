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
resultsPerImplementationFileName = 'WilcoxonPerImplementationFinal'

data = pd.read_csv(sourcePath + sourceFileName + '.csv', header=[0], index_col=0)
implementationList = data.Implementation.unique()
instanceList = data.Name.unique()
implementationRange = range(len(implementationList))
instanceLength = len(instanceList)
instanceRange = range(instanceLength)

# DataFrame Variables
df1 = None
df2 = None
WilcoxonPerInstanceDf = initializeWilcoxonDf()
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
        
        #build the resulting WilcoxonPerImplementationDf
        try:
            _, p_value = wilcoxon(x = WilcoxonPerInstanceDf['Average Solution Cost 1'][-instanceLength:],
                                     y = WilcoxonPerInstanceDf['Average Solution Cost 2'][-instanceLength:])
        except: 
            print("Error with acquiring wilcoxon p-value")

        row = {
            'Instance': "",
            'Optimal Value': optimalValue,
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
saveResultsToCsv(WilcoxonPerInstanceDf, resultsPath, resultsPerInstanceFileName)
saveResultsToCsv(WilcoxonPerImplementationDf, resultsPath, resultsPerImplementationFileName)


        