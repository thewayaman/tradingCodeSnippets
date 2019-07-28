import pandas as pd
import csv
import matplotlib.pyplot as plt

df = pd.read_csv('D:/NIF1h.csv');    #Path to the data to be back tested
df.dropna(how='any')                   #to drop if any value in the row has a nan
df.dropna(how='all')                   #to drop if all values in the row are nan

df1 = pd.DataFrame({'Mass': abs(df['High'] - df['Low'])})    #Assign the SMA period through the argumnet to the rolling(period) function
result = pd.concat([df, df1], axis=1, sort=False)

result.dropna(how='any')                   #to drop if any value in the row has a nan
result.dropna(how='all')                   #to drop if all values in the row are nan
df1 = []
df1 = pd.DataFrame({'Points Shed': result['Mass'] - abs(result['Close'] - result['Open'])})
result = pd.concat([result, df1], axis=1, sort=False)

df1 = []
df1 = pd.DataFrame({'Points Ratio': result['Points Shed'].rolling(6).mean() /result['Mass'].rolling(6).sum()})
result = pd.concat([result, df1], axis=1, sort=False)

df1 = []
df1 = pd.DataFrame({'Points Ratio Smoothed': result['Points Ratio'].rolling(6).mean()})
result = pd.concat([result, df1], axis=1, sort=False)
# for ind,row in result.iterrows():
#     while ind+1 < result.index.max()+1:

fig,axes = plt.subplots(4,1)
result.plot(kind='line',x='Date',y='Mass', color='red', ax=axes[0])
result.plot(kind='line',x='Date',y='Points Shed', color='red', ax=axes[1])
result.plot(kind='line',x='Date',y='Points Ratio Smoothed', color='red', ax=axes[2])
result.plot(kind='line',x='Date',y='Close',ax=axes[3])
plt.show()

