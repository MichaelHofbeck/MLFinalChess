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
learning_rate = 1e-3
num_epochs = 1000

PPG_Data = []
data = None
with open("evalData.txt", "r") as g:
    data = g.readlines()
for line in data:
    PPG_Data.append(line.split(","))
print(len(PPG_Data[0]))
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
recordings = np.array(PPG_Data[:len(PPG_Data)-(len(PPG_Data)%batch_size)])
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
    def __init__(self, imgChannels=1, featureDim=5300, bsize=batch_size):
        super(VAE, self).__init__()

        # Initializing the 2 convolutional layers and 2 full-connected layers for the encoder
        self.encConv1 = nn.Conv1d(imgChannels, 8, 5)
        self.encConv2 = nn.Conv1d(8, 5, 5)
        self.encConv3 = nn.Conv1d(5, 1, 5)
        self.encFC1 = nn.Linear(featureDim, bsize)

    def encoder(self, x, featureDim=5300):

        x = torch.unsqueeze(x, 1)
        # print(x.shape)
        x = F.relu(self.encConv1(x))
        # print(x.shape)
        x = F.relu(self.encConv2(x))
        # print(x.shape)
        x = F.relu(self.encConv3(x))
        # print(x.shape)
        x = x.view(-1, featureDim)
        mu = self.encFC1(x)
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
optimizer = torch.optim.SGD(net.parameters(), lr=learning_rate, momentum=0.001, weight_decay=0.001)

"""
Training the network for a given number of epochs
The loss after every epoch is printed
"""
for epoch in range(num_epochs):
    for idx, data in enumerate(train_loader, 0):

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
        optimizer.step()
    print('Epoch {}: Loss {}'.format(epoch, loss.to(cpu)))
raise
with torch.no_grad():
    for data in random.sample(list(test_loader), 1):
        plt.gca().set_prop_cycle(color=['red', 'green'])
        imgs = data.float()
        img = imgs[0]
        plt.plot(img)
        imgs = imgs.to(device)
        out, mu, logVAR = net(imgs)
        outimg = out[0]
        plt.plot(outimg.to(cpu))
        plt.savefig("output11.png")

"""
The following part takes a random image from test loader to feed into the VAE.
Both the original image and generated image from the distribution are shown.
"""

net.eval()