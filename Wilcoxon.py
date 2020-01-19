from scipy.stats import wilcoxon
import pandas as pd

path = 'newFinalResults/'
fileNameSuffix = 'FinalResultsPerRun'

data = pd.read_csv(path + fileNameSuffix + '.csv', header=[0], index_col=0)

columns = data.columns
df1 = data.loc[data["Implementation"] == '2-opt, double-bridge']
print(df1.head())