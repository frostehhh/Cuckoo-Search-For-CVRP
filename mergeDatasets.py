"""
Read directory of results, results/A-VRP, results/B-VRP, results/P-VRP
Same number of files in all directories
Merge datasets from A-VRP, B-VRP, P-VRP into one. Filename will be equivalent to filenames or results.
Save to newresults.

I don't need this anymore
"""
import os
import pandas as pd

#region Load Datasets
DataSetResultsPath = ['results/A-VRP/'
    ,'results/B-VRP/'
    ,'results/P-VRP/'
    ,'results/'
    ]

DatasetList = [os.listdir(datasetPath) for datasetPath in DataSetResultsPath]
DatasetList[3] = DatasetList[3][3:]

data = [[] for i in range(4)] 

# Read a results + i per iteration. Merge into one file.

def saveResultsToCsv(df, path, fileName, type='results'):
    # if not os.path.exists(path + fileName + '.csv'):
        df.to_csv(path + fileName + '.csv')
        print('Saved ' + 'results' + fileName + '.csv')
  
savePath = 'mergedresult/'

for i in range(len(DatasetList[0])):
    for j in range(len(DataSetResultsPath[:-1])):
        data[j] = pd.read_csv(DataSetResultsPath[j] + DatasetList[j][i], header=[0])
    try:
        filename = DatasetList[3][i][:-4]
    except IndexError:
        filename = DatasetList[1][i][:-4] #remove .txt extension
    finalData = data[0].append(data[1]).append(data[2])
    finalData.drop(finalData.columns[0],axis=1, inplace=True)
    finalData.reset_index(inplace=True, drop=True)
    print(finalData)
    if i == 3:
        saveResultsToCsv(finalData, savePath, filename)
    # save file after
#end region

