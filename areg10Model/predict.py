import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import torch
from sklearn.preprocessing import MinMaxScaler
from captum.attr import IntegratedGradients
np.random.seed(42)
torch.manual_seed(42)

# NN MODEL CHECKPOINT ----- 
mod_path = 'areg10.ckpt'

# READ DATA -----
data = pd.read_csv('may25_pp_v1.csv')

# PREPROCESSING ----
data = data.drop(columns=['VID'])  
data = data.values # to np

# preprocess x
x = data[:, :-1] 
y = data[:, -1:] 

scaler = MinMaxScaler()
scaler.fit(x)
x = scaler.transform(x)
data = np.hstack((x,y))

#  scaler.inverse_transform(x)    # incase want to return back

np.random.shuffle(data)

# data loader prep
trn_size = int(round(data.shape[0]*0.7))
val_size = int(round(data.shape[0]*0.15))
tst_size = int(round(data.shape[0]*0.15))

trn = data[:trn_size]
val = data[trn_size:trn_size + val_size]
tst = data[-tst_size:]

train_set_torch = torch.from_numpy(trn).float()
val_set_torch = torch.from_numpy(val).float()
tst_set_torch = torch.from_numpy(tst).float()


# NN ARCH ------
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


## restore model
checkpoint = torch.load(mod_path, map_location='cpu')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()
checkpoint['epoch']

## PREDICTION PREP ---- 
def predict(ds):
    x = ds[:, :-1]
    y = ds[:, -1:]
    pred = model(x)
    ### pytorch tensors to numpy arrays + back to original scale. 
    label = y.detach().numpy()
    pred = pred.detach().numpy()
    return (label, pred)

## performance measures
def metrics(label, pred):
    rmse = np.sqrt(np.mean( np.square((label - pred)) ))
    mae = np.mean( np.abs((label - pred)) )
    return (rmse, mae)


# VISUALIZATIONS ----------

## 1. Performance Plot 
def performance_plot(val_ds, test_ds):
    val_label, val_pred = predict(val_ds)
    test_label, test_pred = predict(test_ds)

    ## performance measures
    val_metrics = metrics(val_label, val_pred)
    test_metrics = metrics(test_label, test_pred)

    plt.subplot(121)
    plt.plot([0, val_label.max()+10], [0, val_label.max()+10], ls="-", c="gray", linewidth=0.5)
    plt.scatter(val_label, val_pred, s=12)
    plt.title('{}{} -- RMSE: {:.3f}, MAE: {:.3f}, N={:.0f}'.format('Performance Report\n','VAL', val_metrics[0], val_metrics[1], val_label.shape[0]))
    plt.xlabel('Reference Buffer EDB (ml)')
    plt.ylabel('Predicted Buffer EDB (ml)')
    plt.subplot(122)
    plt.plot([0, test_label.max()+10], [0, test_label.max()+10], ls="-", c="gray", linewidth=0.5)
    plt.scatter(test_label, test_pred, s=12)
    plt.title('{}{} -- RMSE: {:.3f}, MAE: {:.3f}, N={:.0f}'.format('Performance Report\n','TEST', test_metrics[0], test_metrics[1], test_label.shape[0]))
    plt.xlabel('Reference Buffer EDB (ml)')
    plt.ylabel('Predicted Buffer EDB (ml)')

    plt.show()


performance_plot(val_set_torch, tst_set_torch)

