import random
import pandas as pd

numList = []

for i in range(5):
    numList.append(random.randrange(1,21))

for i in numList:
    while numList[0] == numList[1] or numList[0] == numList[2] or numList[0] == numList[3] or numList[0] == numList[4]:
        numList[0] = numList[0] + 1
    while numList[1] == numList[0] or numList[1] == numList[2] or numList[1] == numList[3] or numList[1] == numList[4]:
        numList[1] = numList[1]+1
    while numList[2] == numList[0] or numList[2] == numList[1] or numList[2] == numList[3] or numList[2] == numList[4]:
        numList[2] = numList[2]+1
    while numList[3] == numList[0] or numList[3] == numList[1] or numList[3] == numList[2] or numList[3] == numList[4]:
        numList[3] = numList[3]+1
    while numList[4] == numList[0] or numList[4] == numList[1] or numList[4] == numList[2] or numList[4] == numList[3]:
        numList[4] = numList[4]+1
#print(numList)

df = pd.DataFrame(numList)

print(df)
