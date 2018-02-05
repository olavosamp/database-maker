import os
from collections import Counter
import count
import dirs
import pandas as pd

# testList = ['one', 'one', 'two', 'banana']
# testDict = {'key1': 1, 'key2': 2}
#
# testCount = Counter(testList)
# print(testCount)
#
# for elem in testCount.keys():
#     print(elem)


csvPath = dirs.registro_de_eventos+"GHmls16-263_OK.csv"

data = pd.read_csv(csvPath, dtype=str)

# print(data)
# nameList = Counter(data.loc[:]['VideoName'])
nameList = data['VideoName'].unique().tolist()

for elem in nameList:
    print(elem)
    newDf = data.loc[data.VideoName == elem]
    print(newDf)
