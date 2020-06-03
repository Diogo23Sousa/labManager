import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import torch
from sklearn.preprocessing import MinMaxScaler
np.random.seed(42)
torch.manual_seed(42)

mod_path = 'areg10.ckpt'
epochs = 100000
batch_size = 32


# read data
data = pd.read_csv('may25_pp_v1.csv')

# pp
data = data.drop(columns=['VID'])  
data = data.values # to np

# preprocess x
x = data[:, :-1] 
y = data[:, -1:] 

scaler = MinMaxScaler()
scaler.fit(x)
x = scaler.transform(x)
data = np.hstack((x,y))

np.random.shuffle(data)

# data loader 
trn_size = int(round(data.shape[0]*0.7))
val_size = int(round(data.shape[0]*0.15))
tst_size = int(round(data.shape[0]*0.15))

trn = data[:trn_size]
val = data[trn_size:trn_size + val_size]
tst = data[-tst_size:]

train_set_torch = torch.from_numpy(trn).float()
val_set_torch = torch.from_numpy(val).float()

train_loader = torch.utils.data.DataLoader(dataset=train_set_torch,
                                          batch_size=batch_size,
                                          shuffle=True)                          
val_loader = torch.utils.data.DataLoader(dataset=val_set_torch,
                                          batch_size=batch_size,
                                          shuffle=True)


idx, data = next(enumerate(train_loader))
print( data.shape )


class areg10(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.act = torch.nn.ReLU()
        self.fc1 = torch.nn.Linear(20,64)
        self.bnorm1 = torch.nn.LayerNorm(64)
        self.fc2 = torch.nn.Linear(64,64)
        self.bnorm2 = torch.nn.LayerNorm(64)
        self.drop2 = torch.nn.Dropout(0.2)
        self.fc3 = torch.nn.Linear(64,32)
        self.bnorm3 = torch.nn.LayerNorm(32)
        self.drop3 = torch.nn.Dropout(0.1)
        self.logits = torch.nn.Linear(32, 1)
    def forward(self, x):        
        x = self.bnorm1(self.act(self.fc1(x)))
        x = self.drop2(self.bnorm2(self.act(self.fc2(x))))
        x = self.drop3(self.bnorm3(self.act(self.fc3(x))))
        x = self.logits(x)
        return x


# model & loss init
model = areg10()

optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
adjustLR = torch.optim.lr_scheduler.CyclicLR(optimizer, base_lr=1e-5, max_lr=1e-4, mode='exp_range', cycle_momentum=False)
mae_loss = torch.nn.L1Loss()

# main train for-loop
train_losses = []
cur_epoch = 0
val_losses = []
best_loss = float('inf')

## restore model
# checkpoint = torch.load(mod_path)
# model.load_state_dict(checkpoint['model_state_dict'])
# cur_epoch = checkpoint['epoch']
# best_loss = checkpoint['best_loss']

for e in range(epochs):
    e += cur_epoch
    running_loss = 0
    batches = len(train_loader)
    for i, data in enumerate(train_loader):
        model = model.cpu()
        model = model.train() 
        x = data[:, :-1] 
        y = data[:, -1:]

        optimizer.zero_grad()
        outputs = model(x)
        loss = mae_loss(outputs, y)
        loss.backward()
        optimizer.step()
        adjustLR.step()
        running_loss += loss.item()
        if (i % 1000 == 0):
            print ('Batch: {}/{} Train loss: {}'.format(i, batches, loss.item() ))
    else:
        with torch.no_grad():
            val_loss = 0
            model = model.eval()
            for i, data in enumerate(val_loader):
                x = data[:, :-1] 
                y = data[:, -1:]
                outputs = model(x)
                
                loss = mae_loss(outputs, y)
                val_loss += loss.item()
        
        val_losses.append(val_loss / len(val_loader))
        train_losses.append(running_loss / len(train_loader))
        
        if val_losses[-1] < best_loss:
            best_loss = val_losses[-1]
            torch.save({
                    'epoch': e+1,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'best_loss': best_loss}, mod_path)

        print ('Epochs: {}/{}'.format(e+1, epochs),
                'Train Loss: {:.7f}'.format(train_losses[-1]),
                'Val Loss: {:.7f}'.format(val_losses[-1]),
                'Best Val Loss: {:.7f}'.format(best_loss))
