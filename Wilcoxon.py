from scipy.stats import wilcoxon
import pandas as pd

path = 'newFinalResults/'
fileNameSuffix = 'FinalResultsPerRun - Work'

data = pd.read_csv(path + fileNameSuffix + '.csv', header=[0], index_col=0)
implementationList = data.Implementation.unique()
instanceList = data.Name.unique()
implementationRange = range(len(implementationList))



df1 = data.loc[data["Implementation"] == '2-opt, shift-1, double-bridge']
df1_data = df1["Best Solution Cost"].tolist()

print(df1.head())
print(implementationRange)



for i in implementationRange:
    for j in implementationRange[1:]:
        # compare i and j
        # iterate through every instance of implementations i and j