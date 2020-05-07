import os
import pandas as pd
from natsort import natsorted


dirName = './pozyxAPI_dane_pomiarowe'


def parselearndata():
    learndata = pd.DataFrame()
    for filename in natsorted(os.listdir(dirName)):
        if filename.endswith(".xlsx"):
            df = pd.read_excel(f"{dirName}/{filename}")
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            learndata = learndata.append(df, ignore_index=True)
    print(learndata.head())
    learndata.to_csv("./learn_data.csv")


def parsetestdata():
    dataframe = pd.DataFrame()
    df = pd.read_excel("./pozyxAPI_only_localization_dane_testowe_i_dystrybuanta.xlsx")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    dataframe = dataframe.append(df, ignore_index=True)
    dataframe.to_csv("./test_data.csv")

