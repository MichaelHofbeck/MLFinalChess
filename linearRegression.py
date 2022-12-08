from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, KFold
import numpy as np
import preProcessing

x, y = preProcessing.main()
kf = KFold(n_splits=3)

model = LinearRegression()
model.fit(x, y)
print("LinearRegression")
print("Error Rate", 1 - np.mean((cross_val_score(model, x, y, cv=kf))))
