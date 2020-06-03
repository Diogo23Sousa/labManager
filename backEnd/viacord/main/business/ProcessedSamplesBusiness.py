# BLUEPRINT (processed_samples_repository)
import json
import numpy as np
import pandas as pd
from datetime import datetime
import torch
import joblib

from flask import Blueprint

from viacord.main.repositories.SampleInfoRepository import SampleInfoRepository

processed_samples_business = Blueprint('processed_samples_business', __name__, template_folder='templates')


class ProcessedSamplesBusiness:
    def __init__(self):
        self = self

    @staticmethod
    def calculateBufferVolume(sampleInfo):
        sInfo = json.loads(sampleInfo)
        sInfoInitialWeight = sInfo["initialWeight"]
        bufferVolume = 27
        if sInfoInitialWeight != 0:
            bufferVolume = ProcessedSamplesBusiness.predictBufferVolume(sampleInfo)
            print("The buffer volume calculated is:", bufferVolume)
            # bufferVolume = 5.15 + 0.84*sInfoInitialWeight
        return SampleInfoRepository.updateSampleInfo(sampleInfo, bufferVolume)


    @staticmethod
    def predictBufferVolume(sampleInfo):
        sInfo = json.loads(sampleInfo)
        # INPUTS -----
        mod_path = 'business/predictionModel/areg10.ckpt'
        scaler_path = 'business/predictionModel/data_scaler.z'

        dateAndTime = datetime.now()
        labelingYear = dateAndTime.year
        labelingMonth = dateAndTime.month
        labelingDay = dateAndTime.day
        labelingHour = dateAndTime.hour

        data = np.array([[sInfo["initialWeight"], labelingYear, labelingMonth, labelingDay, labelingHour,
                          sInfo["birthOrderReceivedMins"], sInfo["hospitalMins"], sInfo["originCourierMins"],
                          sInfo["planeMins"], sInfo["destinationCourierMins"], sInfo["hospitalTemp"],
                          sInfo["avgOriginCourierTemp"], sInfo["stdOriginCourierTemp"], sInfo["avgOriginCourierHumid"],
                          sInfo["stdOriginCourierHumid"], sInfo["planeTemp"], sInfo["avgDestinationCourierTemp"],
                          sInfo["stdDestinationCourierTemp"], sInfo["avgDestinationCourierHumid"],
                          sInfo["stdDestinationCourierHumid"]]])

        print(f'input data shape: {data.shape}')  # (1, 20)

        # Load Scaler ----
        scaler = joblib.load(scaler_path)

        # NN ARCH ------
        class areg10(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.act = torch.nn.ReLU()
                self.fc1 = torch.nn.Linear(20, 64)
                self.bnorm1 = torch.nn.LayerNorm(64)
                self.fc2 = torch.nn.Linear(64, 64)
                self.bnorm2 = torch.nn.LayerNorm(64)
                self.drop2 = torch.nn.Dropout(0.2)
                self.fc3 = torch.nn.Linear(64, 32)
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
        return pred_one.item()
