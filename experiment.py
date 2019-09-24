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
def saveResultsToCsv(df, path, fileNameSuffix, type='results'):
        df = pd.DataFrame(df)
        # write to results.csv
        fileNum = 0
        while True:
                if fileNum < 10:
                        _ = '0' + str(fileNum)
                else:
                        _ = str(fileNum)
                if type == 'results':
                        if os.path.exists(path + 'results' + path[8] + _ + '.csv'):
                                fileNum += 1
                                continue
                        else:
                                df.to_csv(path + 'results' + path[8] + _ + '_' + fileNameSuffix + '.csv')
                                print('Saved ' + 'results' + path[8] + _ + '_' + fileNameSuffix + '.csv')
                                break
                elif type == 'finalresults':
                        if os.path.exists(path + 'results' + path[13] + _ + '_' + fileNameSuffix + '.csv'):
                                fileNum += 1
                                continue
                        else:
                                df.to_csv(path + 'results' + path[13] + _ + '_' + fileNameSuffix + '.csv')
                                print('Saved ' + 'results' + path[13] + _ + '_' + fileNameSuffix + '.csv')
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