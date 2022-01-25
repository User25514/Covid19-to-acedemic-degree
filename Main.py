import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()
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
def grabAndClean():
    GlobalVariable = {
        "Data":pd.read_csv(f'dataset.csv'),
        "XovidPositive": {"Data":"","TechniqueX":{"Data":"","Mean":""},"TechniqueZERO":{"Data":"","Mean":""}},
        "XovidNegative": {"Data":"","TechniqueX":{"Data":"","Mean":""},"TechniqueZERO":{"Data":"","Mean":""}}}
    GlobalVariable["Data"].drop(columns=["nhs number","drug used during test","Unnamed: 10"], inplace = True)
    GlobalVariable["Data"]['date of test'] = pd.to_datetime(GlobalVariable["Data"]['date of test'])
    GlobalVariable["Data"].dropna(subset=['date of test'], inplace = True)
    for x in GlobalVariable["Data"].index:
        if GlobalVariable["Data"].loc[x, "education level"] == "NA":
                GlobalVariable["Data"].drop(x, inplace = True)
        elif GlobalVariable["Data"].loc[x, "efficacy of technique used"] > 100:
            GlobalVariable["Data"].loc[x, "efficacy of technique used"] = 100
    
    populateVariable(GlobalVariable,"XovidPositive","true")
    populateVariable(GlobalVariable,"XovidNegative","false")
    plot(GlobalVariable)
def populateVariable(GlobalVariable,Direction,bool):
    GlobalVariable[Direction]["Data"] = SplitData(GlobalVariable["Data"],"XoviD21 result",bool)
    q1 = int(GlobalVariable[Direction]["Data"].quantile(0.10))
    q2 = int(GlobalVariable[Direction]["Data"].quantile(0.75))
    for x in GlobalVariable[Direction]["Data"].index:
        if GlobalVariable[Direction]["Data"].loc[x, "efficacy of technique used"] > q2 or GlobalVariable[Direction]["Data"].loc[x, "efficacy of technique used"] < q1:
           GlobalVariable[Direction]["Data"].drop(x, inplace = True)
    for a in ["X","ZERO"]:
        GlobalVariable[Direction][f"Technique{a}"]["Data"] = SplitData(GlobalVariable[Direction]["Data"],"technique used",a)
        GlobalVariable[Direction][f"Technique{a}"]["Mean"] = Mean(GlobalVariable[Direction][f"Technique{a}"]["Data"],"date of test","efficacy of technique used")
    

def plot(GlobalVariable):
    plt.scatter(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]["date of test"], GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]["efficacy of technique used"], label = "Xovid Positive with X")
    plt.scatter(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]["date of test"], GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]["efficacy of technique used"], label = "Xovid Positive with ZERO")
    plt.scatter(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]["date of test"], GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]["efficacy of technique used"], label = "Xovid Negative with X")
    plt.scatter(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]["date of test"], GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]["efficacy of technique used"], label = "Xovid Negative with ZERO")
    plt.legend()
    plt.ylabel('efficacy of technique used')
    plt.xlabel('Date of Test')
    
    plt.show()
    printStats(GlobalVariable)
def printStats(GlobalVariable):
    print(f'All: {len(GlobalVariable["Data"])}')
    print(f'Tested Positive: {len(GlobalVariable["XovidPositive"]["Data"])}')
    print(f'Tested Negative: {len(GlobalVariable["XovidNegative"]["Data"])}')
    print(f'Difference between p/n: {len(GlobalVariable["XovidPositive"]["Data"]) - len(GlobalVariable["XovidNegative"]["Data"])}')
    print(f'Tested Positive X: {len(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"])}')
    print(f'Tested Positive ZERO: {len(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"])}')
    print(f'Difference between pX/PZERO: {len(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]) - len(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"])}')
    print(f'Tested Negative X: {len(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"])}')
    print(f'Tested Negative ZERO: {len(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"])}')
    print(f'Difference between nX/nZERO: {len(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]) - len(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"])}')
    print(f'Difference between pX/nX: {len(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]) - len(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"])}')
    print(f'Difference between pZERO/nZERO: {len(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]) - len(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"])}')
    print(f'Percentage of Degrees with positive: {round(len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD"))/len(GlobalVariable["XovidPositive"]["Data"])*100,2)}%')
    a = len(SplitData(GlobalVariable["Data"],"education level","PhD"))
    b = len(SplitData(GlobalVariable["Data"],"education level","BsC"))
    c = len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD"))
    d = len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","BsC"))
    e = len(GlobalVariable["Data"])
    
    f = len(GlobalVariable["XovidPositive"]["Data"])
    a = ((a + b) / e)*100
    b = ((c + d)/e)*100
    c = (e / f)*100
    '''
    P(a) is Probability of having phd or bsc = 10%
    P(b|a) is Probability of testing positive, given that they have a phd or bsc happens = 50%
    P(c) is Probability of testing positive = 40%
    '''
    total = (a*b)/c
    print(f"{round(total*100,2)}%")

grabAndClean()
