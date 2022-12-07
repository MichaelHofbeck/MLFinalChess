from sklearn.neighbors import KNeighborsClassifier, DistanceMetric
from sklearn.model_selection import cross_val_score, KFold
import numpy as np
from matplotlib import pyplot as plt
import preProcessing

x, y = preProcessing.main()
kf = KFold(n_splits=3)

# Euclidean distance metric
scores = []
k = [_ for _ in range(1, 20)]
for i in k:
    model = KNeighborsClassifier(n_neighbors=i)
    scores.append(np.mean((1 - cross_val_score(model, x, y, cv=kf))))

plt.plot(k, scores)
plt.title("Euclidean")
plt.xlabel('k')
plt.ylabel('error rate')
plt.show()

# Mahalanobis Metric
# scores = []
# DistanceMetric.get_metric('mahalanobis', V=np.cov(x, rowvar=False))
# for i in range(20):
#     model = KNeighborsClassifier(n_neighbors=1, metric='mahalanobis', metric_params={'V': np.cov(x, rowvar=False)})
#     scores.append(np.mean((1 - cross_val_score(model, x, y))))

# plt.plot(scores)
# plt.title("Mahalanobis")
# plt.xlabel('k')
# plt.ylabel('error rate')
# plt.show()

