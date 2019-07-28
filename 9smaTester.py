import pandas as pd
import csv



df = pd.read_csv('D:/NIF1h.csv');    #Path to the data to be back tested
df.dropna(how='any')                   #to drop if any value in the row has a nan
df.dropna(how='all')                   #to drop if all values in the row are nan

df2 = pd.DataFrame({'SMA': df['Close'].rolling(20).mean()})    #Assign the SMA period through the argumnet to the rolling(period) function
result = pd.concat([df, df2], axis=1, sort=False)
trade = []

with open("D:/output.csv", "w",newline='') as fp:    #Creates .csv to store overall trades at the path specified
    csvwriter = csv.writer(fp,dialect="excel")
    csvwriter.writerow(['Position','Open Date','Open Price','Close Date','Close Price'])    #Append column headings to the created .csv

def maestro(tradelist,position,date,price):
    if len(tradelist) != 0:
         for i in tradelist:
             if i != position:
                with open("D:/output.csv", "a",newline='') as fp: #Stores the final trade in the form of a single list created in the specified .csv
                    csvwriter = csv.writer(fp,dialect="excel")
                    csvwriter.writerow(tradelist)
             i=0
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

for index,row in result.iterrows():
        if(row['Close'] > row['SMA']):      #check if price is lower than SMA
            tradetemp = maestro(trade,'LONG',row['Date'],row['Close'])
            trade = tradetemp

        elif(row['Close'] < row['SMA']):    #check if price is higher than SMA
            tradetemp = maestro(trade,'SHORT',row['Date'],row['Close'])
            trade = tradetemp


dfFinal = pd.read_csv("D:/output.csv")
pd.options.mode.chained_assignment = None  # default='warn'
for index,row in dfFinal.iterrows():       #Replaces all the closing dates and prices for those trades that did'nt last
                                           #more than a day
    if index+1 < dfFinal.index.max()+1:
        # if row['Close Date'] == "0" :
        #     print('kaboom')
            dfFinal.loc[index,'Close Date'] = dfFinal.loc[index+1,'Open Date']
            dfFinal.loc[index,'Close Price'] = dfFinal.loc[index+1,'Open Price']
    if row['Position'] == 'SHORT':          #calculates and appends the gain/loss
        dfFinal.loc[index,'GAIN/LOSS'] = dfFinal.loc[index,'Open Price'] - dfFinal.loc[index,'Close Price']
    else :
        dfFinal.loc[index,'GAIN/LOSS'] = dfFinal.loc[index,'Close Price'] - dfFinal.loc[index,'Open Price']

print(dfFinal['GAIN/LOSS'].sum())                         #View all the trades
dfFinal.to_csv("D:/outputFinal.csv")   #Store the trades to a final .csv
