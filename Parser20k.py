import regex as re
import experiment as exp
import pandas as pd

# Dataset: A-n32-k5, Run time: 149.15, Best Solution Cost: 842.785755207392, Optimal Value: 784 routesGen(gen, min) = 5, 5 numNodes(gen, req) = 32, 32
rx_dict = {
    'instanceResults': re.compile(r'Dataset: \s*(?P<instanceName>[A-Za-z0-9\.-]*), Run time: (?P<time>[0-9\.]*), Best Solution Cost: (?P<cost>[0-9\.]*), Optimal Value: (?P<optimal>[0-9]*).*')
    # 'instanceResults': re.compile(r'Dataset:\s*(?P<instanceName>[A-Za-z0-9\.-]*), Run time: (?P<time>[0-9]*.*[0-9]*), Best Solution Cost: (?P<cost>[0-9]*.*[0-9]*), Optimal Value: (?P<optimal>[0-9]*).*')

}

def __assignToRow(instanceName, solutionCost, optimal, time):
    """
    Parameters
    ----------
    instanceName : str
    solutionCost : float
    optimal : str
    time : float

    Returns
    ----------
    {
        "Name" : instanceName,
        "Best Solution Cost" : float(solutionCost),
        "Optimal Value" : optimal,
        "Run Time" : float(time)
    }
    """
    
    return {
        "Name" : instanceName,
        "Best Solution Cost" : float(solutionCost),
        "Optimal Value" : optimal,
        "Run Time" : float(time)
    }
    
def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """

    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

def parse_file(filepath):
    """
    Parse txt file ng 20k iter results

    Parameters
    ----------
    filepath : str
        Filepath for file_object to be parsed

    Returns
    -------
    experimentData : df
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

    # dataframes
    instanceData = exp.initializeInstanceData()
    experimentData = exp.initializeExperimentData()

    # read 5 lines of data. 
    # store in instanceData. 
    # compute results. 
    # save to experiment data.
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        i = 0
        while line:
            # at each line check for a match with a regex
            key, match = _parse_line(line)
            if key == 'instanceResults':
                #name = match.group('instanceResults')
                if i < 5:
                    instanceName = match.group('instanceName')
                    solutionCost = match.group('cost')
                    optimal = match.group('optimal')
                    time = match.group('time')
                    row = __assignToRow(instanceName, solutionCost, optimal, time)
                    exp.appendRowToInstanceDf(instanceData, row)
                    i += 1
                else:
                    i=0
                    row = exp.calculateInstanceResults(instanceData)
                    exp.appendRowToExperimentDf(experimentData, row)
                    instanceData = exp.initializeInstanceData()
                    instanceName = match.group('instanceName')
                    solutionCost = match.group('cost')
                    optimal = match.group('optimal')
                    time = match.group('time')
                    i += 1

            # next line
            line = file_object.readline()
        row = exp.calculateInstanceResults(instanceData)
        exp.appendRowToExperimentDf(experimentData, row)

    return experimentData

if __name__ == '__main__':
    datasetPath = 'results20k/'
    inputFileName = 'results20k.txt'
    outputFileName = 'results20k'

    experimentData = parse_file(datasetPath + inputFileName)
    experimentData = pd.DataFrame(experimentData)
    experimentData.to_csv(datasetPath + outputFileName + '.csv')
    pass
