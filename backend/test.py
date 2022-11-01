import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as set_columns

from sktime.forecasting.model_selection import temporal_train_test_split
from sklearn.model_selection import TimeSeriesSplit

import xgboost as xgb
from sklearn.metrics import mean_squared_error

from datetime import date, timedelta, datetime


def create_feature(df):

    df = df.copy()
    df["dayofweek"] = df.index.dayofweek
    df["month"] = df.index.month
    df["year"] = df.index.year
    df["dayofyear"] = df.index.dayofyear
    df["quarter"] = df.index.quarter
    df["dayofmonth"] = df.index.dayofmonth
    df["weekofyear"] = df.index.isocalendar().week

    return df


df = pd.read_csv("../assets/train_1.csv")
df = df.set_index("Date")
df.index = pd.to_datetime(df.index)
print(df.head())

df.plot(style="-", figsize=(15, 5), color="red", title="sales")
# plt.show()

tss = TimeSeriesSplit(n_splits=5, test_size=24 * 7 * 1, gap=24)
df = df.sort_index()

fig, axs = plt.subplots(5, 1, figsize=(15, 5), sharex=True)
fold = 0

for train_idx, val_idx in tss.split(df):
    train = df.iloc[train_idx]
    test = df.iloc[val_idx]

    train["Sales"].plot(ax=axs[fold], label="Training Set", title="Train/Test Data")
    test["Sales"].plot(ax=axs[fold], label="Tesing Set")
    axs[fold].axvline(test.index.min(), color="black", ls="--")

    fold += 1

print(train_idx)
print(val_idx)

df = create_feature(df)

target_map = df["Sales"].to_dict()
df["lag1"] = (df.index - pd.timedelta("364 days")).map(target_map)

plt.show()
