import os
import pandas as pd
from natsort import natsorted

dirName = './pozyxAPI_dane_pomiarowe'


def parse_learn_data():
    data = pd.DataFrame()
    for filename in natsorted(os.listdir(dirName)):
        if filename.endswith(".xlsx"):
            df = pd.read_excel(f"{dirName}/{filename}")
            df = df[['0/timestamp', 't', 'no', 'measurement x', 'measurement y', 'reference x', 'reference y']]
            data = data.append(df, ignore_index=True)
    df = pd.read_excel("./pozyxAPI_only_localization_dane_testowe_i_dystrybuanta.xlsx")
    df = df[['0/timestamp', 't', 'no', 'measurement x', 'measurement y', 'reference x', 'reference y']]
    data = data.append(df, ignore_index=True)
    data.to_csv("./dataset.csv")
