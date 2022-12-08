import preProcessing
import numpy as np

x, y = preProcessing.main()

randomBaseline = []
for example in x:
    randomBaseline.append(np.random.randint(0,63) * 100 + np.random.randint(0,63))

correctExamples = 0
totalExamples = len(randomBaseline)
for i in range(totalExamples):
    if randomBaseline[i] == y[i]:
        correctExamples += 1
# print(randomBaseline)
print(list(y))
print(correctExamples/totalExamples)