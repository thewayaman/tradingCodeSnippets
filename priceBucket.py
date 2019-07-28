from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
bucket = {}
datePlot = {}

fig = plt.figure()
ax = plt.axes(projection='3d')
date:str
df = pd.read_csv('D:/NIF1min.csv');
df.dropna(how='any');                   #to drop if any value in the row has a nan
df.dropna(how='all');                  #to drop if all values in the row are nan

for ind,row in df.iterrows():
    if ind <= df.index[-1]:
        string = str(row['Date'])
        df.loc[ind,'Pure Date']=string[0:string.rfind('/')+5]

df.dropna(how='any');                   #to drop if any value in the row has a nan
df.dropna(how='all');                  #to drop if all values in the row are nan

# date = df['Pure Date'][0]
# print(date,"date")
for ind,row in df.iterrows():
    if ind <= df.index[-1]:
        if (ind != 0):
            if(date == df['Pure Date'][ind]):
                for states in datePlot[date]:
                    # print(states.find('-'))
                    lower = float(states[0:states.find('-')])
                    higher = float(states[states.find('-')+1:])
                    openPrice = float(df['Open'][ind])
                    # print(openPrice,lower,higher)
                    if(lower <= openPrice <= higher):
                        tempCount = datePlot[date][states]
                        datePlot[date][states] = tempCount + 1
                        print(date,lower,openPrice,higher,datePlot[date][states])
                        found = True
                        break;
                    else:
                        found = False
                if(found == False):
                    close = int(df['Open'][ind])
                    number = close
                    # print(number%10)
                    temp = close-((number%10)-1)
                    datePlot[date].update({str(str(temp)+"-"+str(temp+9.99)):1})
                found = []

            else:
                date = df['Pure Date'][ind]
                close = int(df['Open'][ind])
                number = close
                # print(number%10)
                temp = close-((number%10)-1)
                datePlot.update({date:{str(str(temp)+"-"+str(temp+9.99)):1}})

        else:
            date = df['Pure Date'][ind]
            close = int(df['Open'][ind])
            number = close
            # print(number%10)
            temp = close-((number%10)-1)
            datePlot = {date:{str(str(temp)+"-"+str(temp+9.99)):1}}
            # print(list)
            # count = 0
            # while(number > 0):
            #     number = number//10
            #     print(number)
            #     count = count + 1
            # print(number,count)

# df.to_csv('D:/PureDateNIF1h.csv');

print(datePlot)
