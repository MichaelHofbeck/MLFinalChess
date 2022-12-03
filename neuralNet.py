from sklearn.neural_network import MLPClassifier as MLPC
from sklearn.datasets import load_digits # X This is just to test
import pickle


D = load_digits()
model = MLPC(hidden_layer_sizes=(100,50,25))
model.fit(D.data, D.target)
accuracy = model.score(D.data, D.target)
print("accuracy: ", accuracy)

# Saves nn weights into nnWeights.sav
fileName = "nnWeights.sav"
pickle.dump(model, open(fileName, "wb"))

# loads nn weights from nnWeights.sav
loadedModel = pickle.load(open(fileName, 'rb'))