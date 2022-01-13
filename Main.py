import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Mean(LST,Duplicate,MathData):
    LSTNoDate = LST.drop_duplicates(subset=[Duplicate])
    LSTAverage = []
    for a in LSTNoDate[Duplicate]:
        total = (LST.loc[LST[Duplicate] == a])[MathData].mean()
        LSTAverage.append([a,total])
    LSTAverage = pd.DataFrame(LSTAverage, columns = [Duplicate, MathData])
    return LSTAverage
def SplitData(LST,Column,Splitter):
    m = LST[Column] != Splitter
    print(m)
    return Data[~m] 
    
Data = pd.read_csv(f'dataset.csv') # reads csv file, used the first line for headings!
Data.drop(columns="Unnamed: 10", inplace = True)
Data['date of test'] = pd.to_datetime(Data['date of test'])
Data.dropna(subset=['date of test'], inplace = True)
print(Data)
#ZERO, X = SplitData(Data,'technique used',"X")
ZEROAverage = Mean(SplitData(Data,'technique used',"ZERO"),"date of test","efficacy of technique used")

plt.plot(ZEROAverage["date of test"], ZEROAverage["efficacy of technique used"], '.') # plots those points, meaning you can go plot more points over it

XAverage = Mean(SplitData(Data,'technique used',"X"),"date of test","efficacy of technique used")

plt.plot(XAverage["date of test"], XAverage["efficacy of technique used"], '.')


plt.show()