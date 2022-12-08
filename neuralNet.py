'''
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
'''

###

import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np
import random

"""
Initialize Hyperparameters
"""
batch_size = 100
learning_rate = 1e-2
num_epochs = 3000

PPG_Data = []
data = None
with open("evalDataInit.txt", "r") as g:
    data = g.readlines()
for line in data:
    PPG_Data.append(line.split(",")[:-1])
sample_length = 65

print("DATA LOADED")
"""
Determine if any GPUs are available
"""
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
cpu = torch.device("cpu")

"""
Final Input Processing
"""
random.shuffle(PPG_Data)
recordings = np.array(PPG_Data[:len(PPG_Data)-(len(PPG_Data)%batch_size)], dtype=float)
print("Total Samples: " + str(len(recordings)))
cutoff = int(0.9*(len(recordings)//batch_size))*batch_size

"""
Create dataloaders to feed data into the neural network
"""
train_loader = torch.utils.data.DataLoader(
    recordings[:cutoff],
    batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(
    recordings[cutoff:],
    batch_size=batch_size)


"""
A Convolutional Variational Autoencoder
"""
class VAE(nn.Module):
    def __init__(self, imgChannels=1, featureDim=53, bsize=batch_size):
        super(VAE, self).__init__()

        # Initializing the 2 convolutional layers and 2 full-connected layers for the encoder
        self.encConv1 = nn.Conv1d(1, 1, 5)
        self.encConv2 = nn.Conv1d(1, 1, 5)
        self.encConv3 = nn.Conv1d(1, 1, 5)
        self.encFC1 = nn.Linear(featureDim, 2000)
        self.encFC2 = nn.Linear(2000, 1)

    def encoder(self, x, featureDim=53):

        x = torch.unsqueeze(x, 1)
        # print(x.shape)
        x = F.relu(self.encConv1(x))
        # print(x.shape)
        x = F.relu(self.encConv2(x))
        # print(x.shape)
        x = F.relu(self.encConv3(x))
        # print(x.shape)
        # x = x.view(-1, featureDim)
        mu = self.encFC1(x)
        mu = self.encFC2(mu)
        # print(mu.shape)
        return mu

    def forward(self, x):

        # The entire pipeline of the VAE: encoder -> reparameterization -> decoder
        # output, mu, and logVar are returned for loss computation
        mu = self.encoder(x)
        out = torch.squeeze(mu)
        return out

"""
Initialize the network and the Adam optimizer
"""
net = VAE().to(device)
optimizer = torch.optim.SGD(net.parameters(), lr=learning_rate, momentum=0.9, weight_decay=0.0001)

"""
Training the network for a given number of epochs
The loss after every epoch is printed
"""
losses = []
for epoch in range(num_epochs):
    for idx, data in enumerate(train_loader, 0):
        if epoch == num_epochs/2:   optimizer = torch.optim.SGD(net.parameters(), lr=learning_rate/100, momentum=0.2)
        imgs = data[:,:-1].float()
        targets = data[:,-1].float()
        imgs = imgs.to(device)

        # Feeding a batch of images into the network to obtain the output image, mu, and logVar
        out = net(imgs)
        out = out.to(device)

        # The loss is the BCE loss combined with the KL divergence to ensure the distribution is learnt
        # kl_divergence = -0.5 * torch.sum(1 + logVar - mu.pow(2) - logVar.exp())
        # if idx % 1000: print(kl_divergence)
        loss = F.mse_loss(out, targets).to(device) # + kl_divergence
        if (np.isnan(loss.detach().to(cpu)).any()):
            print(np.isnan(out.detach().to(cpu)).any() == 1)
            temp = net.forward(imgs)[0]
            print(np.isnan(temp[0].detach().to(cpu)).any() == 1)
            print(np.isnan(temp[1].detach().to(cpu)).any() == 1)
            print(np.isnan(net.reparameterize(temp[0], temp[1]).detach().to(cpu)).any() == 1)
            raise
        '''
        if loss < 0:
            if kl_divergence < 0: 
                print("KL")
            else:
                print("MSE")
            raise
        '''
        # Backpropagation based on the loss
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), learning_rate)
        optimizer.step()
    print('Epoch {}: Loss {}'.format(epoch, loss.to(cpu)))
    losses.append(loss.to(cpu).detach().numpy().item())

plt.plot(np.array(losses))
plt.title("CNN Loss")
plt.xlabel('Epoch')
plt.ylabel('Loss (in squared centipawns)')
plt.show()

torch.save(net.state_dict(), "CNN_weights.txt")
""
with torch.no_grad():
    total_error = 0
    for data in list(test_loader):
        imgs = data[:,:-1].float()
        targets = data[:,-1].float()
        imgs = imgs.to(device)

        out = net(imgs)

        total_error += F.mse_loss(out, targets).detach().numpy().item()

print(total_error/(len(test_loader)*batch_size))
print("Avg Out of sample error (in squared centipawns)^^^")
"""
The following part takes a random image from test loader to feed into the VAE.
Both the original image and generated image from the distribution are shown.
"""

net.eval()