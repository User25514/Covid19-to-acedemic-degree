import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import environ
from pandas_profiling import ProfileReport
import sweetviz as sv
import statistics
from scipy.stats import norm
from scipy.stats import t
import seaborn as sns

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
    #profile = ProfileReport(GlobalVariable["Data"], title='Worker Report')
    #profile
    #profile.to_file("worker_report.html")
    #my_report = sv.analyze(GlobalVariable["Data"])
    #my_report.show_html()
    Scatterplot(GlobalVariable)
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
    
<<<<<<< Updated upstream
def Distribution(GlobalVariable):
    Positive_TechniqueX = {"Length":len(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"])}
    Positive_TechniqueZero = {"Length":len(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"])}
    Negative_TechniqueX = {"Length":len(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"])}
    Negative_TechniqueZero = {"Length":len(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"])}
=======
def BoxPlotResultTech(GlobalVariable):
    
    data = [GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]["efficacy of technique used"],
            GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]["efficacy of technique used"],
            GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]["efficacy of technique used"],
            GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]["efficacy of technique used"]]
    plt.boxplot(data)
    plt.legend()
    plt.ylabel('efficacy of technique used')
    plt.xlabel('Positive/Negative XoviD21 Techniques')
    plt.xticks([1, 2, 3,4], ['Positive X', 'Negative X', 'Positive ZERO', 'Negative ZERO'])
    plt.savefig("BoxPlotResultTech.png")
def StandardDeviation(GlobalVariable):
    plt.clf()
    data = [len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","below GCSE"))+
            len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","GCSE"))+
            len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","A-Level")),
            len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","BSc")),
            len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD")),]
    data2 = [len(SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","below GCSE"))+
            len(SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","GCSE"))+
            len(SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","A-Level")),
            len(SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","BSc")),
            len(SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","PhD")),]

    sns.distplot(norm.pdf(data,np.mean(data),statistics.stdev(data)), hist=False, label = "Positive XoviD21")
    sns.distplot(norm.pdf(data2,np.mean(data2),statistics.stdev(data2)), hist=False, label = "Negative XoviD21")
    print(data)
    print(data2)
    #plt.xlim(0,6)
    #plt.ylim(0,225)
    plt.grid()
    plt.legend()
    plt.savefig("StandardDistribution.png")
def StandardDeviationOfH1(GlobalVariable):
    print("Start Deviation H1")
    plt.clf()
    PositiveGCSE = {"Mean":
        np.mean(pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","A-Level")])["efficacy of technique used"]),
        "SD":float(0.0)}
    NegativeGCSE = {"Mean":
        np.mean(pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","A-Level")])["efficacy of technique used"]),
        "SD":float(0.0)}
    PositiveDegree = {"Mean":
        np.mean(pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD")])["efficacy of technique used"]),
        "SD":float(0.0)}
    NegativeDegree = {"Mean":
        np.mean(pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","PhD")])["efficacy of technique used"]),
        "SD":float(0.0)}
    print(len(pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","A-Level")])))
    print(len(pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","A-Level")])))
    print(len(pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD")])))
    print(len(pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","PhD")])))
    print(sum(pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","A-Level")])["efficacy of technique used"]))
    print(sum(pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","A-Level")])["efficacy of technique used"]))
    print(sum(pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD")])["efficacy of technique used"]))
    print(sum(pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","PhD")])["efficacy of technique used"]))
    for a in pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","below GCSE"),
        SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","GCSE"),
        SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","A-Level")])["efficacy of technique used"]:
        PositiveGCSE["SD"] += np.square((a - PositiveGCSE["Mean"]))
    for a in pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","below GCSE"),
        SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","GCSE"),
        SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","A-Level")])["efficacy of technique used"]:
        NegativeGCSE["SD"] += np.square((a - NegativeGCSE["Mean"]))
    for a in SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","BSc")["efficacy of technique used"]:
        PositiveDegree["SD"] += np.square((a - PositiveDegree["Mean"]))
    for a in SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD")["efficacy of technique used"]:
        PositiveDegree["SD"] += np.square((a - PositiveDegree["Mean"]))
    for a in SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","BSc")["efficacy of technique used"]:
        NegativeDegree["SD"] += np.square((a - NegativeDegree["Mean"]))
    for a in SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","PhD")["efficacy of technique used"]:
        NegativeDegree["SD"] += np.square((a - NegativeDegree["Mean"]))
    PositiveGCSE["SD"] = PositiveGCSE["SD"]/(len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level",
        "below GCSE"))+len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","GCSE"))+
        len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","A-Level"))-1)
    NegativeGCSE["SD"] = NegativeGCSE["SD"]/(len(SplitData(GlobalVariable["XovidNegative"]["Data"],"education level",
        "below GCSE"))+len(SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","GCSE"))+
        len(SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","A-Level"))-1)
    PositiveDegree["SD"] = PositiveDegree["SD"]/(len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level",
        "BSc"))+len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD"))-1)
    NegativeDegree["SD"] = NegativeDegree["SD"]/(len(SplitData(GlobalVariable["XovidNegative"]["Data"],"education level",
        "BSc"))+len(SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","PhD"))-1)
    PositiveGCSE["SQRT"] = np.sqrt(PositiveGCSE["SD"])
    NegativeGCSE["SQRT"] = np.sqrt(NegativeGCSE["SD"])
    PositiveDegree["SQRT"] = np.sqrt(PositiveDegree["SD"])
    NegativeDegree["SQRT"] = np.sqrt(NegativeDegree["SD"])
    sns.distplot(norm.pdf(pd.concat([
        SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","below GCSE"),
        SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","GCSE"),
        SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","A-Level")])["efficacy of technique used"],
        PositiveGCSE["Mean"],PositiveGCSE["SQRT"]), hist=False, label = "Positive Not Degree")
    sns.distplot(norm.pdf(pd.concat([
        SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","below GCSE"),
        SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","GCSE"),
        SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","A-Level")])["efficacy of technique used"],
        NegativeGCSE["Mean"],NegativeGCSE["SQRT"]), hist=False, label = "Negative Not Degree")
    sns.distplot(norm.pdf(pd.concat([
        SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","BSC"),
        SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD")])["efficacy of technique used"],
        PositiveGCSE["Mean"],PositiveGCSE["SQRT"]), hist=False, label = "Positive Degree")
    sns.distplot(norm.pdf(pd.concat([
        SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","BSC"),
        SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","PhD")])["efficacy of technique used"],
        NegativeGCSE["Mean"],NegativeGCSE["SQRT"]), hist=False, label = "Negative Degree")
    plt.grid()
    plt.legend()
    plt.savefig("StandardDistributionH1.png")
    print("End Deviation H1")
    
def StandardDeviationOfH2(GlobalVariable):
    plt.clf()
    PositiveX = {"Mean":
        np.mean(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]["efficacy of technique used"]),
        "SD":float(0.0)}
    
    NegativeX = {"Mean":
        np.mean(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]["efficacy of technique used"]),
        "SD":float(0.0)}
    PositiveZERO = {"Mean":
        np.mean(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]["efficacy of technique used"]),
        "SD":float(0.0)}
    NegativeZERO = {"Mean":
        np.mean(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]["efficacy of technique used"]),
        "SD":float(0.0)}
    for a in GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]["efficacy of technique used"]:
        PositiveX["SD"] += np.square((a - PositiveX["Mean"]))
    for a in GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]["efficacy of technique used"]:
        NegativeX["SD"] += np.square((a - NegativeX["Mean"]))
    for a in GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]["efficacy of technique used"]:
        PositiveZERO["SD"] += np.square((a - PositiveZERO["Mean"]))
    for a in GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]["efficacy of technique used"]:
        NegativeZERO["SD"] += np.square((a - NegativeZERO["Mean"]))

    PositiveX["SD"] = PositiveX["SD"]/(len(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"])-1)
    NegativeX["SD"] =NegativeX["SD"]/(len(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"])-1)
    PositiveZERO["SD"] = PositiveZERO["SD"]/(len(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"])-1)
    NegativeZERO["SD"] = NegativeZERO["SD"]/(len(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"])-1)

    PositiveX["SQRT"] = np.sqrt(PositiveX["SD"])
    NegativeX["SQRT"] = np.sqrt(NegativeX["SD"])
    PositiveZERO["SQRT"] = np.sqrt(PositiveZERO["SD"])
    NegativeZERO["SQRT"] = np.sqrt(NegativeZERO["SD"])

    sns.distplot(norm.pdf(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]["efficacy of technique used"],
                          PositiveX["Mean"],PositiveX["SQRT"]), hist=False, label = "Positive XoviD21 Technique X")
    sns.distplot(norm.pdf(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]["efficacy of technique used"],
                          NegativeX["Mean"],NegativeX["SQRT"]), hist=False, label = "Negative XoviD21 Technique X")
    sns.distplot(norm.pdf(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]["efficacy of technique used"],
                          PositiveZERO["Mean"],PositiveZERO["SQRT"]), hist=False, label = "Positive XoviD21 Technique ZERO")
    sns.distplot(norm.pdf(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]["efficacy of technique used"],
                          PositiveZERO["Mean"],PositiveZERO["SQRT"]), hist=False, label = "Negative XoviD21 Technique ZERO")
    plt.grid()
    plt.legend()
    plt.savefig("StandardDistributionH2.png")
def ConfidenceInterval(GlobalVariable):
    plt.clf()
    PositiveX = {"Mean":
        np.mean(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]["efficacy of technique used"]),
        "SD":float(0.0)}
    
    NegativeX = {"Mean":
        np.mean(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]["efficacy of technique used"]),
        "SD":float(0.0)}
    PositiveZERO = {"Mean":
        np.mean(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]["efficacy of technique used"]),
        "SD":float(0.0)}
    NegativeZERO = {"Mean":
        np.mean(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]["efficacy of technique used"]),
        "SD":float(0.0)}
    print(PositiveX)
    print(NegativeX)
    print(PositiveZERO)
    print(NegativeZERO)
    print("\n lenths:")
    print(len(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]))
    print(len(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]["efficacy of technique used"]))
    print(len(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]["efficacy of technique used"]))
    print(len(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]["efficacy of technique used"]))
    print("\n")
    for a in GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]["efficacy of technique used"]:
        PositiveX["SD"] += np.square((a - PositiveX["Mean"]))
    for a in GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]["efficacy of technique used"]:
        NegativeX["SD"] += np.square((a - NegativeX["Mean"]))
    for a in GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]["efficacy of technique used"]:
        PositiveZERO["SD"] += np.square((a - PositiveZERO["Mean"]))
    for a in GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]["efficacy of technique used"]:
        NegativeZERO["SD"] += np.square((a - NegativeZERO["Mean"]))
    print(PositiveX)
    print(NegativeX)
    print(PositiveZERO)
    print(NegativeZERO)
    print("\n")
    
    PositiveX["SD"] = PositiveX["SD"]/(len(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"])-1)
    NegativeX["SD"] =NegativeX["SD"]/(len(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"])-1)
    PositiveZERO["SD"] = PositiveZERO["SD"]/(len(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"])-1)
    NegativeZERO["SD"] = NegativeZERO["SD"]/(len(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"])-1)
    confidence = 0.95
    print(PositiveX)
    print(NegativeX)
    print(PositiveZERO)
    print(NegativeZERO)
    print("\n")
    
    t_crit1 = np.abs(t.ppf((1-confidence)/2,(len(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"])-1)))
    t_crit2 = np.abs(t.ppf((1-confidence)/2,(len(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"])-1)))
    t_crit3 = np.abs(t.ppf((1-confidence)/2,(len(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"])-1)))
    t_crit4 = np.abs(t.ppf((1-confidence)/2,(len(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"])-1)))
    print(t_crit1)
    print(t_crit2)
    print(t_crit3)
    print(t_crit4)
    print("\n")
    CI1 = ((PositiveX["Mean"]-PositiveX["SD"]*t_crit1/np.sqrt(len(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"])), PositiveX["Mean"]+PositiveX["SD"]*t_crit1/np.sqrt(len(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]))) )
    CI2 = ((NegativeX["Mean"]-NegativeX["SD"]*t_crit2/np.sqrt(len(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"])), NegativeX["Mean"]+NegativeX["SD"]*t_crit2/np.sqrt(len(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]))) )
    CI3 = ((PositiveZERO["Mean"]-PositiveZERO["SD"]*t_crit3/np.sqrt(len(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"])), PositiveZERO["Mean"]+PositiveZERO["SD"]*t_crit3/np.sqrt(len(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]))) )
    CI4 = ((NegativeZERO["Mean"]-NegativeZERO["SD"]*t_crit4/np.sqrt(len(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"])), NegativeZERO["Mean"]+NegativeZERO["SD"]*t_crit2/np.sqrt(len(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]))) )
    print(CI1)
    print(CI2)
    print(CI3)
    print(CI4)
    print("\n")
    plt.clf()
    plt.boxplot([CI1,CI2,CI3,CI4])
    plt.title("Confidence Interval")
    plt.ylabel('efficacy of technique used')
    plt.xlabel('Positive/Negative XoviD21 Techniques')
    plt.xticks([1, 2, 3,4], ['Positive X', 'Negative X', 'Positive ZERO', 'Negative ZERO'])
    plt.legend()
    plt.savefig("BoxPlotconfidence.png")
    som = input()
def ConfidenceIntervalH1(GlobalVariable):
    plt.clf()
    PositiveGCSE = {"Mean":
        np.mean(pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","A-Level")])["efficacy of technique used"]),
        "LEN":len(pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","A-Level")])),
        "SD":float(0.0)}
    NegativeGCSE = {"Mean":
        np.mean(pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","A-Level")])["efficacy of technique used"]),
        "LEN":len(pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","A-Level")])),
        "SD":float(0.0)}
    PositiveDegree = {"Mean":
        np.mean(pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD")])["efficacy of technique used"]),
        "LEN":len(pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD")])),
        "SD":float(0.0)}
    NegativeDegree = {"Mean":
        np.mean(pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","PhD")])["efficacy of technique used"]),
        "LEN":len(pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","PhD")])),
        "SD":float(0.0)}
    print(PositiveGCSE)
    print(NegativeGCSE)
    print(PositiveDegree)
    print(NegativeDegree)
    
    
    
    
    for a in pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","A-Level")])["efficacy of technique used"]:
        PositiveGCSE["SD"] += np.square((a - PositiveGCSE["Mean"]))
    for a in pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","below GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","GCSE"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","A-Level")])["efficacy of technique used"]:
        NegativeGCSE["SD"] += np.square((a - NegativeGCSE["Mean"]))
    for a in pd.concat([SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD")])["efficacy of technique used"]:
        PositiveDegree["SD"] += np.square((a - PositiveDegree["Mean"]))
    for a in pd.concat([SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","BSc"),
                           SplitData(GlobalVariable["XovidNegative"]["Data"],"education level","PhD")])["efficacy of technique used"]:
        NegativeDegree["SD"] += np.square((a - NegativeDegree["Mean"]))
    print(PositiveGCSE)
    print(NegativeGCSE)
    print(PositiveDegree)
    print(NegativeDegree)
    print("\n")
    
    PositiveGCSE["SD"] = PositiveGCSE["SD"]/(PositiveGCSE["LEN"]-1)
    NegativeGCSE["SD"] =NegativeGCSE["SD"]/(NegativeGCSE["LEN"]-1)
    PositiveDegree["SD"] = PositiveDegree["SD"]/(PositiveDegree["LEN"]-1)
    NegativeDegree["SD"] = NegativeDegree["SD"]/(NegativeDegree["LEN"]-1)
    confidence = 0.95
    print(PositiveGCSE)
    print(NegativeGCSE)
    print(PositiveDegree)
    print(NegativeDegree)
    print("\n")
    
    t_crit1 = np.abs(t.ppf((1-confidence)/2,(PositiveGCSE["LEN"]-1)))
    t_crit2 = np.abs(t.ppf((1-confidence)/2,(NegativeGCSE["LEN"]-1)))
    t_crit3 = np.abs(t.ppf((1-confidence)/2,(PositiveDegree["LEN"]-1)))
    t_crit4 = np.abs(t.ppf((1-confidence)/2,(NegativeDegree["LEN"]-1)))
    print(t_crit1)
    print(t_crit2)
    print(t_crit3)
    print(t_crit4)
    print("\n")
    CI1 = ((PositiveGCSE["Mean"]-PositiveGCSE["SD"]*t_crit1/np.sqrt(PositiveGCSE["LEN"]), PositiveGCSE["Mean"]+PositiveGCSE["SD"]*t_crit1/np.sqrt(PositiveGCSE["LEN"])) )
    CI2 = ((NegativeGCSE["Mean"]-NegativeGCSE["SD"]*t_crit2/np.sqrt(NegativeGCSE["LEN"]), NegativeGCSE["Mean"]+NegativeGCSE["SD"]*t_crit2/np.sqrt(NegativeGCSE["LEN"])) )
    CI3 = ((PositiveDegree["Mean"]-PositiveDegree["SD"]*t_crit3/np.sqrt(PositiveDegree["LEN"]), PositiveDegree["Mean"]+PositiveDegree["SD"]*t_crit3/np.sqrt(PositiveDegree["LEN"])) )
    CI4 = ((NegativeDegree["Mean"]-NegativeDegree["SD"]*t_crit4/np.sqrt(NegativeDegree["LEN"]), NegativeDegree["Mean"]+NegativeDegree["SD"]*t_crit2/np.sqrt(NegativeDegree["LEN"])) )
    print(CI1)
    print(CI2)
    print(CI3)
    print(CI4)
    print("\n")
    plt.clf()
    plt.boxplot([CI1,CI2,CI3,CI4])
    plt.title("Confidence Interval")
    plt.ylabel('efficacy of technique used')
    plt.xlabel('Positive/Negative XoviD21 Techniques')
    plt.xticks([1, 2, 3,4], ['Positive N/Degree', 'Negative N/Degree', 'Positive Degree', 'Negative Degree'])
    plt.legend()
    plt.savefig("BoxPlotconfidenceH1.png")
    som = input()
>>>>>>> Stashed changes
def Scatterplot(GlobalVariable):
    plt.scatter(GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]["date of test"], GlobalVariable["XovidPositive"]["TechniqueX"]["Data"]["efficacy of technique used"], label = "Xovid Positive with X")
    plt.scatter(GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]["date of test"], GlobalVariable["XovidPositive"]["TechniqueZERO"]["Data"]["efficacy of technique used"], label = "Xovid Positive with ZERO")
    plt.scatter(GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]["date of test"], GlobalVariable["XovidNegative"]["TechniqueX"]["Data"]["efficacy of technique used"], label = "Xovid Negative with X")
    plt.scatter(GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]["date of test"], GlobalVariable["XovidNegative"]["TechniqueZERO"]["Data"]["efficacy of technique used"], label = "Xovid Negative with ZERO")
    plt.legend()
    plt.ylabel('efficacy of technique used')
    plt.xlabel('Date of Test')
    #plt.show()
    plt.savefig("PositiveAndNegativeWithXorZERO.png")
    BoxPlotResultTech(GlobalVariable)
    StandardDeviation(GlobalVariable)
    StandardDeviationOfH2(GlobalVariable)
    StandardDeviationOfH1(GlobalVariable)
    ConfidenceIntervalH1(GlobalVariable)
    ConfidenceInterval(GlobalVariable)
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
    print(a)
    b = len(SplitData(GlobalVariable["Data"],"education level","BsC"))
    print(b)
    c = len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","PhD"))
    print(c)
    d = len(SplitData(GlobalVariable["XovidPositive"]["Data"],"education level","BsC"))
    print(d)
    e = len(GlobalVariable["Data"])
    print(e)
    f = len(GlobalVariable["XovidPositive"]["Data"])
    print(f)
    a = ((a + b) / e)*100
    print(a)
    b = ((c + d)/e)*100
    print(b)
    c = (e / f)*100
    print(c)
    
    '''
    P(a) is Probability of having phd or bsc = 10%
    P(b|a) is Probability of testing positive, given that they have a phd or bsc happens = 50%
    P(c) is Probability of testing positive = 40%
    '''
    total = (a*b)/c
    print(total)
    print(f"{a} - {b} - {c} - {total}")
    print(f"P(b|a): {round(total*100,2)}%")
    '''
    P(amount of students over 6ft knowing they are over 18)*P(amount of a student over 6ft)/P(Amount of students over 18) = P(amount of students over 18 knowing they are over 6ft)
    A=amount of students over 6ft
    B= students over 18
    P(A|B)*P(A)/P(B)=P(B|A)
    '''
grabAndClean()
"""
cases = 10000
zeroTrust = 1000/cases
print(f"Probability {zeroTrust}%")
trojanInfections = 3000/cases
print(f"Probability {trojanInfections}%")
trojanInfectionsZeroTrust = 20/cases
print(f"Probability {trojanInfectionsZeroTrust}%")
print(f"Probability {(trojanInfectionsZeroTrust*zeroTrust)/trojanInfections}%")
<<<<<<< Updated upstream
"""
=======
"""
>>>>>>> Stashed changes
