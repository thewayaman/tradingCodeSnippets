import time
import winsound
from apscheduler.schedulers.blocking import BlockingScheduler
from nsetools import Nse
import pandas as pd
import math as m
import numpy

frequency1 = 2500  # Set Frequency To 2500 Hertz
duration1 = 1000  # Set Duration To 1000 ms == 1 second

frequency0 = 1500  # Set Frequency To 2500 Hertz
duration0 = 1000  # Set Duration To 1000 ms == 1 second


nse = Nse()
q = nse.get_index_quote('nifty bank')
print(q)
#This is where the time gets set

start_time = time.ctime()
index = start_time.index(':')
print(start_time,' ',)
leftSlice = slice(0,index-2)
rightSlice = slice(index+6,start_time.__len__())
rightPart = start_time[rightSlice]
leftPart = start_time[leftSlice]
start_time = leftPart+'12:00:00'+rightPart
wait_time = leftPart+'12:01:00'+rightPart



#load previous days values into the df

df = pd.read_csv("D:/Stored_data/banknifty.csv")

def ATR(df, n): # ATR(df='The dataframe which has values stored in .csv format',n='The time period of the ATR to be calculated)
    i = 0
    TR_l = [0]
    while i < df.index[-1]:
        # TR = max(df.get_value(i + 1, 'High'), df.get_value(i, 'Close')) - min(df.get_value(i + 1, 'Low'), df.get_value(i, 'Close'))
        TR = max(df.at[i + 1, 'High'], df.at[i, 'Close']) - min(df.at[i + 1, 'Low'], df.at[i, 'Close'])
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = ((df.at[df.index[-2],'ATR'] * (n-1)) + TR_s.tail(1))/n
    return ATR # ATR is being calculated based on a SMA although there are other methods available (RMA,WMA etc.),
                # don't know much about them

mul = 3
ATR  = ATR(df,5)
SP = df.tail(1)
print(df,"SPAPDPAKDP",df['High'].max(),"printe index",df.at[df['High'].idxmax(),'Close'])
calc0 = (SP['High'] + SP['Low']) / 2
calc1 = mul * ATR
Upper = ( calc0 + calc1 ) # …Only if price < upper
Lower = ( calc0 - calc1)  # …Only if price > lower

print(Upper,"upper")
# ATR(df='The dataframe which has values stored in .csv format',n='The time period of the ATR to be calculated)

# def min3():
#     print('3 min supertrend ')
#     winsound.Beep(frequency0, duration0)
#
def hour1():
    print('1 hour 9 sma')
    print(nse.get_index_quote('nifty bank'))
    winsound.Beep(frequency1, duration1)
#
scheduler = BlockingScheduler()
# scheduler.add_job(min3,'interval',minutes=1)
scheduler.add_job(hour1,'interval',minutes=2)
#
while time.ctime() != wait_time:
    if time.ctime() == start_time:
        print("<-- job started -->")
        scheduler.start()
    else :
        print("## job should get started in ")



