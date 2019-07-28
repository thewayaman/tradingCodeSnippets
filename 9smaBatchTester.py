import pandas as pd
import csv
import matplotlib.pyplot as plt



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

for runs in (240,300,360,420,480,540,600,660,720,780):
    result = []
    df = pd.read_csv('D:/NIF1h.csv');      #To read data from a csv file
    # df   = pd.read_csv('D:/Bigdata/JAN_OCT_2012_BANKNIFTY_F1.txt', sep=",", header=None) #To read data from a txt file
    # df.columns = ['Index','Date','Time','Open','High','Low','Close','Volume'] #To read data from a txt file
    df.dropna(how='any')                   #to drop if any value in the row has a nan
    df.dropna(how='all')                   #to drop if all values in the row are nan
    dfSMA = pd.DataFrame({'SMA': df['Close'].rolling(runs).mean()})    #Assign the SMA period through the argumnet to the rolling(period) function
    result = pd.concat([df, dfSMA], axis=1, sort=False)
    result.dropna(how='any')                   #to drop if any value in the row has a nan
    result.dropna(how='all')                   #to drop if all values in the row are nan


    # FOR OVERLAPPING SUBPLOTS
    # ax1 = plt.gca()
    # ax2 = ax1.twinx()
    # ax3 = ax1.twinx()
    # result.plot(kind='line',x='Date',y='Close',ax=ax1)
    # result.plot(kind='line',x='Date',y='DEVL', color='red', ax=ax2)
    # result.plot(kind='line',x='Date',y='DEVS', color='pink', ax=ax3)
    # fig.tight_layout()

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
    dfFinal.to_csv("D:/outputFinal"+str(runs)+".csv")   #Store the trades to a final .csv

print(ledgerBook)
