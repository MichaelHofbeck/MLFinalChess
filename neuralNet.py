import sklearn
import sklearn_json as skljson
from sklearn.neural_network import MLPClassifier as MLPC
from sklearn.datasets import load_digits # X This is just to tes

file_name = "neuralModelWeights.json"

D = load_digits()
model = MLPC(hidden_layer_sizes=(100,50,25))
model.fit(D.data, D.target)
accuracy = model.score(D.data, D.target)
print("accuracy: ", accuracy)

skljson.to_json(model, file_name)
savedModel = skljson.from_json(file_name)

smAccuracy = savedModel.score(D.data, D.target)
print("saved model accuracy: ", accuracy)
