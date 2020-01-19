"""
Read directory of results, results/A-VRP, results/B-VRP, results/P-VRP
Same number of files in all directories
Merge datasets from A-VRP, B-VRP, P-VRP into one. Filename will be equivalent to filenames or results.
Save to newresults.

I don't need this anymore
"""
import os
import pandas as pd
import experiment as e


DataSetResultsPath = 'finalresults/'
DatasetList = os.listdir(DataSetResultsPath)[3:]
savePath = 'finalresults/'
fileName = 'completeFinalResults'
data = []

# store all datasets in data[] list
for i in range(len(DatasetList)):
    data.append(pd.read_csv(DataSetResultsPath + DatasetList[i], header=[0]))

    # build _ variable to fill up fileName column
    _ = []
    instanceCount = data[0].index # .index is the number of rows in the dataFrame
    for j in instanceCount:
        _.append(DatasetList[i])

    # inserting fileName column values
    data[i].insert(loc=1, column='fileName', value=_)

# all data is stored in finaldata
finalData = data[0]
for i in range(1, len(DatasetList)):
    finalData = finalData.append(data[i])
finalData.drop(finalData.columns[0],axis=1, inplace=True)
finalData.reset_index(inplace=True, drop=True)

e.saveResultsToCsv(finalData, savePath, fileName, 'mergeAll')


