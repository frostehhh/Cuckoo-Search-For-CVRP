"""
Read directory of results, results/A-VRP, results/B-VRP, results/P-VRP
Same number of files in all directories
Merge datasets from A-VRP, B-VRP, P-VRP into one. Filename will be equivalent to filenames or results.
Save to newresults.
"""
import os
import pandas as pd

#region Load Datasets
DataSetResultsPath = 'mergedresult/'
DatasetList = os.listdir(DataSetResultsPath) 

# Read a results + i per iteration. Merge into one file.

def saveResultsToCsv(df, path, fileName, type='results'):
    # if not os.path.exists(path + fileName + '.csv'):
        df.to_csv(path + fileName + '.csv')
        print('Saved ' + fileName + '.csv')
  
savePath = 'completeResults/'

data = []

for i in range(len(DatasetList)):
    data.append(pd.read_csv(DataSetResultsPath + DatasetList[i], header=[0]))
    _ = []
    instanceRange = data[0].index
    for j in instanceRange:
        _.append(DatasetList[i])
    data[i].insert(loc=1, column='fileName', value=_)
    # append 
    # data[i].

finalData = data[0]
for i in range(1, len(DatasetList)):
    finalData = finalData.append(data[i])
finalData.drop(finalData.columns[0],axis=1, inplace=True)
finalData.reset_index(inplace=True, drop=True)

saveResultsToCsv(finalData, savePath, 'completeResults')
    # save file after
#end region

