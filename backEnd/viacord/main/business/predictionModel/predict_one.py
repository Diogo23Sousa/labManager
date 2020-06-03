import numpy as np 
import pandas as pd
import torch
import joblib

# INPUTS ----- 
mod_path = 'stage2/models/areg10.ckpt'
scaler_path = 'stage2/models/data_scaler.z'

# GET ONE DATA SAMPLE -----
# this is just an example. replace with actual data point.
data = np.array([[2.7000e+01, 2.0140e+03, 9.0000e+00, 3.0000e+00, 1.3000e+01, 2.8050e+02,
         7.7000e+01, 3.2000e+02, 8.1000e+02, 0.0000e+00, 2.1000e+01, 2.9333e+01,
         1.1547e+00, 6.3667e+01, 5.5076e+00, 1.0000e+01, 2.9000e+01, 0.0000e+00,
         6.4000e+01, 0.0000e+00]])

print(f'input data shape: {data.shape}') # (1, 20)

# Load Scaler ----
scaler = joblib.load(scaler_path)

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

model = areg10()

## restore model
checkpoint = torch.load(mod_path, map_location='cpu')
model.load_state_dict(checkpoint['model_state_dict'])
model = model.eval()

## PREDICTION ---- 
def predict_one(x):
    x = scaler.transform(data)
    x = torch.from_numpy(x).float()
    pred = model(x)
    pred = pred.detach().numpy()
    return pred[0][0]

pred_one = predict_one(data)
print(f'Predicted Buffer EDB Volume (mL): {pred_one}')