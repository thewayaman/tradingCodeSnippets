import pandas as pd
import csv
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf


def maestro(tradelist,position,date,price):
    if len(tradelist) != 0:
         for i in tradelist:
             if i != position:
                with open("D:/output"+str(runs)+".csv", "a",newline='') as fp: #Stores the final trade in the form of a single list created in the specified .csv
                    csvwriter = csv.writer(fp,dialect="excel")
                    csvwriter.writerow(tradelist)
             i=0                       #Resets the counter to the trade position
             break
    if len(tradelist)==0 :             #initalizes the trade list
        tradelist = [position,date,price,0,0]
        return tradelist
    else :                             #appends the second the leg of the trade
        if tradelist[0] == position:
            tradelist[3] = date
            tradelist[4] = price
            return tradelist
        else :
            del tradelist[0:4]
            tradelist = [position,date,price,0,0]
            return tradelist

result = []
ledgerBook = {}

for runs in range(2,14):
    result = []
    df = pd.read_csv('D:/NIF30.csv');    #Path to the data to be back tested
    df.dropna(how='any')                   #to drop if any value in the row has a nan
    df.dropna(how='all')                   #to drop if all values in the row are nan

    dfSMA = pd.DataFrame({'SMA': df['Close'].rolling(runs).mean()})    #Assign the SMA period through the argumnet to the rolling(period) function
    result = pd.concat([df, dfSMA], axis=1, sort=False)
    # dfStdS = pd.DataFrame({'DEVS': df['Close'].rolling(10).std()})    #Assign the SMA period through the argumnet to the rolling(period) function
    # result = pd.concat([result, dfStdS], axis=1, sort=False)
    # dfStdL = pd.DataFrame({'DEVL': df['Close'].rolling(42).std()})    #Assign the SMA period through the argumnet to the rolling(period) function
    # result = pd.concat([result, dfStdL], axis=1, sort=False)
    result.dropna(how='any')                   #to drop if any value in the row has a nan
    result.dropna(how='all')                   #to drop if all values in the row are nan
    for indi,row in result.iterrows():
        if indi+1 < result.index.max()+1:
            result.loc[indi,'ABSDIFF'] = abs(result.loc[indi,'Close'] - result.loc[indi,'Open'])
            if indi > (runs)*2:
                if indi+1 < result.index.max()+1:
                    result.loc[indi,'ACC'] = (result.loc[indi,'ABSDIFF'] - result.loc[indi-(runs*2),'ABSDIFF'])/(runs * 2)
                    result.loc[indi,'Force'] = result.loc[indi,'ACC'] * result.loc[indi,'Close']
    result.to_csv("D:/result.csv")
    # FOR OVERLAPPING SUBPLOTS
    # ax1 = plt.gca()
    # ax2 = ax1.twinx()
    # ax3 = ax1.twinx()
    # result.plot(kind='line',x='Date',y='Close',ax=ax1)
    # result.plot(kind='line',x='Date',y='DEVL', color='red', ax=ax2)
    # result.plot(kind='line',x='Date',y='DEVS', color='pink', ax=ax3)
    # fig.tight_layout()

    fig,axes = plt.subplots(3,1)
    result.plot(kind='scatter',x='Close',y='Force', color='red', ax=axes[0])
    result.plot(kind='line',x='Date',y='ACC', color='red', ax=axes[1])
    result.plot(kind='line',x='Date',y='Close',ax=axes[2])
    plt.show()
    trade = []
    print("D:/output"+str(runs)+".csv")
    with open("D:/output"+str(runs)+".csv", "w",newline='') as fp:    #Creates .csv to store overall trades at the path specified
        csvwriter = csv.writer(fp,dialect="excel")
        csvwriter.writerow(['Position','Open Date','Open Price','Close Date','Close Price'])    #Append column headings to the created .csv


    for index,row in result.iterrows():
            if(row['Close'] > row['SMA']):      #check if price is lower than SMA
                tradetemp = maestro(trade,'LONG',row['Date'],row['Close'])
                trade = tradetemp

            elif(row['Close'] < row['SMA']):    #check if price is higher than SMA
                tradetemp = maestro(trade,'SHORT',row['Date'],row['Close'])
                trade = tradetemp


    dfFinal = pd.read_csv("D:/output"+str(runs)+".csv")
    pd.options.mode.chained_assignment = None  # default='warn'
    for index,row in dfFinal.iterrows():       #Replaces all the closing dates and prices for those trades that did'nt last
                                               #more than a day
        if index+1 < dfFinal.index.max()+1:
            # if row['Close Date'] == "0" :
            #     print('kaboom')
                dfFinal.loc[index,'Close Date'] = dfFinal.loc[index+1,'Open Date']
                dfFinal.loc[index,'Close Price'] = dfFinal.loc[index+1,'Open Price']
        elif index+1 == dfFinal.index.max()+1:
            if row['Close Date'] == "0" :
                dfFinal.loc[index,'Close Date'] = dfFinal.loc[index,'Open Date']
                dfFinal.loc[index,'Close Price'] = dfFinal.loc[index,'Open Price']
        if row['Position'] == 'SHORT':          #calculates and appends the gain/loss
            dfFinal.loc[index,'GAIN/LOSS'] = dfFinal.loc[index,'Open Price'] - dfFinal.loc[index,'Close Price']
        else :
            dfFinal.loc[index,'GAIN/LOSS'] = dfFinal.loc[index,'Close Price'] - dfFinal.loc[index,'Open Price']

    # print(dfFinal)                         #View all the trades
    ledgerBook[runs]= dfFinal['GAIN/LOSS'].sum()
    print(ledgerBook)
    dfFinal.to_csv("D:/outputFinal"+str(runs)+".csv")   #Store the trades to a final .csv

print(ledgerBook,"Final")
