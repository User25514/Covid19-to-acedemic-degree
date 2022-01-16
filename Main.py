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
    return LST[~m] 

GlobalVariable = {
    "Data":pd.read_csv(f'dataset.csv'),
    "XovidPositive": {"Data":"","TechniqueX":{"Data":"","Mean":""},"TechniqueZERO":{"Data":"","Mean":""}},
    "XovidNegative": {"Data":"","TechniqueX":{"Data":"","Mean":""},"TechniqueZERO":{"Data":"","Mean":""}},
    }
GlobalVariable["Data"].drop(columns="Unnamed: 10", inplace = True)
GlobalVariable["Data"]['date of test'] = pd.to_datetime(GlobalVariable["Data"]['date of test'])
GlobalVariable["Data"].dropna(subset=['date of test'], inplace = True)
for x in GlobalVariable["Data"].index:
    if GlobalVariable["Data"].loc[x, "education level"] == "NA":
            GlobalVariable["Data"].drop(x, inplace = True)
    elif GlobalVariable["Data"].loc[x, "efficacy of technique used"] > 100:
        GlobalVariable["Data"].loc[x, "efficacy of technique used"] = 100
    
GlobalVariable["XovidPositive"]["Data"] = SplitData(GlobalVariable["Data"],"XoviD21 result","true")
GlobalVariable["XovidNegative"]["Data"] = SplitData(GlobalVariable["Data"],"XoviD21 result","false")
GlobalVariable["XovidPositive"]["TechniqueX"]["Data"] = SplitData(GlobalVariable["XovidPositive"]["Data"],"technique used","X")
GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"] = SplitData(GlobalVariable["XovidPositive"]["Data"],"technique used","ZERO")
GlobalVariable["XovidNegative"]["TechniqueX"]["Data"] = SplitData(GlobalVariable["XovidNegative"]["Data"],"technique used","X")
GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"] = SplitData(GlobalVariable["XovidNegative"]["Data"],"technique used","ZERO")

GlobalVariable["XovidPositive"]["TechniqueX"]["Mean"] = Mean(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"],"date of test","efficacy of technique used")
GlobalVariable["XovidPositive"]["TechniqueZERO"]["Mean"] = Mean(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"],"date of test","efficacy of technique used")
GlobalVariable["XovidNegative"]["TechniqueX"]["Mean"] = Mean(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"],"date of test","efficacy of technique used")
GlobalVariable["XovidNegative"]["TechniqueZERO"]["Mean"] = Mean(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"],"date of test","efficacy of technique used")
#ZERO, X = SplitData(Data,'technique used',"X")
print(GlobalVariable["XovidPositive"]["TechniqueX"]["Mean"])
print("------------------------------------------------------")
print(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Mean"])
print("------------------------------------------------------")
print(GlobalVariable["XovidNegative"]["TechniqueX"]["Mean"])
print("------------------------------------------------------")
print(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Mean"])
print("------------------------------------------------------")

plt.scatter(GlobalVariable["XovidPositive"]["TechniqueX"]["Mean"]["date of test"], GlobalVariable["XovidPositive"]["TechniqueX"]["Mean"]["efficacy of technique used"], label = "Xovid Positive with X")
plt.scatter(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Mean"]["date of test"], GlobalVariable["XovidPositive"]["TechniqueZERO"]["Mean"]["efficacy of technique used"], label = "Xovid Positive with ZERO")
plt.scatter(GlobalVariable["XovidNegative"]["TechniqueX"]["Mean"]["date of test"], GlobalVariable["XovidNegative"]["TechniqueX"]["Mean"]["efficacy of technique used"], label = "Xovid Negative with X")
plt.scatter(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Mean"]["date of test"], GlobalVariable["XovidNegative"]["TechniqueZERO"]["Mean"]["efficacy of technique used"], label = "Xovid Negative with ZERO")
plt.legend(loc='upper left')

'''
ZEROAverage = Mean(SplitData(Data,'technique used',"ZERO"),"date of test","efficacy of technique used")

plt.plot(ZEROAverage["date of test"], ZEROAverage["efficacy of technique used"], '.') # plots those points, meaning you can go plot more points over it

XAverage = Mean(SplitData(Data,'technique used',"X"),"date of test","efficacy of technique used")

plt.plot(XAverage["date of test"], XAverage["efficacy of technique used"], '.')


plt.show()
'''
plt.show()