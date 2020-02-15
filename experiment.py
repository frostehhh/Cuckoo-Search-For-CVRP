import pandas as pd
import os
import numpy as np
import math

def initializeInstanceData():
        """
        Initializes instance data

        Returns
        ------
        {'Name':[],
        'Best Solution Cost':[],
        'Optimal Value':[],
        'Run Time':[]
        } 
        """
        return {'Name':[],
        'Best Solution Cost':[],
        'Optimal Value':[],
        'Run Time':[]
        } 
def initializeExperimentData(name=None, optVal=None, minSolCost=None,
        maxSolCost=None, avgSolCost=None, stdSolCost=None, avgRunTime=None):
        """
        Initializes experiment data. Each row of experiment data consists of 
        multiple runs of a single instance and returns the following data:
        - Name
        - Optimal Value
        - Minimum Solution Cost
        - Max Solution Cost
        - Avg Solution Cost
        - Std of Solution Cost
        - Avg Run Time
        
        Returns
        --------
        If name is None:
                {
                        'Name':[],
                        'Optimal Value':[],
                        'Minimum Solution Cost':[],
                        'Max Solution Cost':[],
                        'Avg Solution Cost':[],
                        'Std of Solution Cost':[],
                        'Avg Run Time':[]
                } 
        else:
                {
                        'Name':[name],
                        'Optimal Value':[optVal],
                        'Minimum Solution Cost':[minSolCost],
                        'Max Solution Cost':[maxSolCost],
                        'Avg Solution Cost':[avgSolCost],
                        'Std of Solution Cost':[stdSolCost],
                        'Avg Run Time':[avgRunTime]
                }  
        """
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
        """
        Insert instanceData from row into df

        row = {
            "Name" : self.instance.fileName,
            "Best Solution Cost" : self.nests[0].cost,
            "Optimal Value" : self.instance.optimalValue,
            "Run Time" : float(self.time),
            "Solution" : self.nests
        }
        """
        df['Name'] += [row['Name']]
        df['Best Solution Cost'] += [row['Best Solution Cost']]
        df['Optimal Value'] += [row['Optimal Value']]
        df['Run Time'] += [row['Run Time']]
def appendRowToExperimentDf(df, row):
        """
        Insert row of experimentData from row into df
        """
        df['Name'] += row['Name']
        df['Optimal Value'] += row['Optimal Value']
        df['Minimum Solution Cost'] += row['Minimum Solution Cost']
        df['Max Solution Cost'] += row['Max Solution Cost']
        df['Avg Solution Cost'] += row['Avg Solution Cost']
        df['Std of Solution Cost'] += row['Std of Solution Cost']
        df['Avg Run Time'] += row['Avg Run Time']
def calculateInstanceResults(instanceData):
        """
        Takes instanceData{'Name':[],
        'Best Solution Cost':[],
        'Optimal Value':[],
        'Run Time':[]
        } 
        as input

        Returns a row of experimentData 


        Parameters
        ----------
        instanceData : dict
                {'Name':[],
                'Best Solution Cost':[],
                'Optimal Value':[],
                'Run Time':[]
                } 

        Returns
        -------
        data : dict
                {'Name':[name],
                'Optimal Value':[optVal],
                'Minimum Solution Cost':[minSolCost],
                'Max Solution Cost':[maxSolCost],
                'Avg Solution Cost':[avgSolCost],
                'Std of Solution Cost':[stdSolCost],
                'Avg Run Time':[avgRunTime]
                }  
        """
        
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
def saveResultsToCsv(df, path, fileNameSuffix, type='default'):
        df = pd.DataFrame(df)
        # write to results.csv
        
        if os.path.exists(path + fileNameSuffix + '.csv'):
                data = pd.read_csv(path + fileNameSuffix + '.csv', header=[0], index_col=0)
                data = data.append(df, sort=False)
                data.reset_index(inplace=True, drop=True)
                data.to_csv(path + fileNameSuffix + '.csv')
        else:
                df.to_csv(path + fileNameSuffix + '.csv')
                        
                
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

def initializeWilcoxonDf():
    """
    Initializes Wilcoxon Dict to be converted to DataFrame

    Returns
    ------
    {
        'Instance':[],
        'Optimal Value':[],
        'Implementation 1':[],
        'Minimum Solution Cost 1':[],
        'Average Solution Cost 1':[],
        'Std Solution Cost 1':[],
        'Average Runtime 1':[],
        'Implementation 2':[],
        'Minimum Solution Cost 2':[],
        'Average Solution Cost 2':[],
        'Std Solution Cost 2':[],
        'Average Runtime 2':[],
        'P-value':[]
    } 
    """
    return {
        'Instance':[],
        'Optimal Value':[],
        'Implementation 1':[],
        'Minimum Solution Cost 1':[],
        'Average Solution Cost 1':[],
        'Std Solution Cost 1':[],
        'Average Runtime 1':[],
        'Implementation 2':[],
        'Minimum Solution Cost 2':[],
        'Average Solution Cost 2':[],
        'Std Solution Cost 2':[],
        'Average Runtime 2':[],
        'P-value':[]
    } 

def appendRowToWilcoxonDf(df, row):
        """
        Insert instanceData from row into df

        row = {
                'Instance': "string",
                'Optimal Value': 0,
                'Implementation 1': "string",
                'Minimum Solution Cost 1':0,
                'Average Solution Cost 1':0,
                'Std Solution Cost 1':0,
                'Average Runtime 1':0,
                'Implementation 2':"string",
                'Minimum Solution Cost 2':0,
                'Average Solution Cost 2':0,
                'Std Solution Cost 2':0,
                'Average Runtime 2':0,
                'P-value':0
        } 
        """
        df['Instance'] += [row['Instance']]
        df['Optimal Value'] += [row['Optimal Value']]
        df['Implementation 1'] += [row['Implementation 1']]
        df['Minimum Solution Cost 1'] += [row['Minimum Solution Cost 1']]
        df['Average Solution Cost 1'] += [row['Average Solution Cost 1']]
        df['Std Solution Cost 1'] += [row['Std Solution Cost 1']]
        df['Average Runtime 1'] += [row['Average Runtime 1']]
        df['Implementation 2'] += [row['Implementation 2']]
        df['Minimum Solution Cost 2'] += [row['Minimum Solution Cost 2']]
        df['Average Solution Cost 2'] += [row['Average Solution Cost 2']]
        df['Std Solution Cost 2'] += [row['Std Solution Cost 2']]
        df['Average Runtime 2'] += [row['Average Runtime 2']]
        df['P-value'] += [row['P-value']]