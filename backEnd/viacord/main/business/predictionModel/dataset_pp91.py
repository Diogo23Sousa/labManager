import pandas as pd
import datetime

# read data
data = pd.read_csv('stage2/data/hackatonDataViaCordLogicalWithoutTemperature.csv')

data.shape

## preprocess
pp = pd.DataFrame()
pp['VID'] = data['VID']

pp['Initial weight (g)'] = data['Initial weight (g)']

# sample year, sample month, sample day, sample hour
data['Labeling Timestamp'] = data['Labeling Date'] + " " + data['Labeling Time']
data['Labeling Timestamp'] = [datetime.datetime.strptime(data['Labeling Timestamp'][i], '%m/%d/%Y %I:%M:%S %p') for i in range(data.shape[0])]
pp['Labeling Year'] =  [ int(data['Labeling Timestamp'][i].strftime("%Y")) for i in range(data.shape[0])  ]
pp['Labeling Month'] =  [ int(data['Labeling Timestamp'][i].strftime("%m")) for i in range(data.shape[0])  ]
pp['Labeling Day'] =  [ int(data['Labeling Timestamp'][i].strftime("%d")) for i in range(data.shape[0])  ]
pp['Labeling Hour'] =  [ int(data['Labeling Timestamp'][i].strftime("%H")) for i in range(data.shape[0])  ]

pp['Birth-Order Received Mins'] = data['Birth-Order Received Mins']
pp['Hospital Mins'] = data['Hospital Mins']
pp['OriginCourier Mins'] = data['OriginCourier Mins']
pp['Plane Mins'] = data['Plane Mins']
pp['DestinationCourier Mins'] = data['DestinationCourier Mins']

pp['Hospital Temp'] = data['Hospital Temp']
pp['OriginTemp Avg'] = data['OriginTemp Avg']
pp['OriginTemp Std'] = data['OriginTemp Std']
pp['OriginHumid Avg'] = data['OriginHumid Avg']
pp['OriginHumid Std'] = data['OriginHumid Std']
pp['Plane Temp'] = data['Plane Temp']
pp['DestinationTemp Avg'] = data['DestinationTemp Avg']
pp['DestinationTemp Std'] = data['DestinationTemp Std']
pp['DestinationHumid Avg'] = data['DestinationHumid Avg']
pp['DestinationHumid Std'] = data['DestinationHumid Std']

# y
pp['Buffer EDB Volume (mL)'] = data['Buffer EDB Volume (mL)']

# null values
pp = pp.dropna()
pp.isnull().sum().sum()

# remove misleading samples, default value 1.
pp = pp[pp['Buffer EDB Volume (mL)']!=1]
pp = pp[abs(pp['Buffer EDB Volume (mL)'] - pp['Initial weight (g)']) <= 20]

# save pp dataset
pp.to_csv('stage2/data/may25_pp_v1.csv', index=False)