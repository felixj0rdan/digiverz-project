# import numpy as np
# import pandas as pd
# import pyflux as pf
# from datetime import datetime
# import matplotlib.pyplot as plt


# data = pd.read_csv("../assets/train_1.csv")
# data.index = data["Date"].values


# data["Date"] = pd.to_datetime(data["Date"])

# dg = data.groupby(pd.Grouper(key="Date", freq="1D")).sum()  # groupby each 1 month
# dg.index = dg.index.strftime("%b-%y")

# print(data.tail())

# plt.figure(figsize=(15, 5))
# plt.plot(data.index, data["Sales"])
# plt.ylabel("Sales")
# plt.title("SALES")
# model = pf.ARIMA(data=data, ar=4, ma=4, target="Sales", family=pf.Normal())

# x = model.fit("MLE")
# print(x.summary())

# model.plot_z(figsize=(15, 5))
# print(model.predict(10, intervals=False))
# plt.show()


# importing required values
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sktime.forecasting.arima import AutoARIMA
from sktime.forecasting.arima import ARIMA
from sktime.datasets import load_airline
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.utils.plotting import plot_series

from pandas.plotting import autocorrelation_plot
from statsmodels.graphics.tsaplots import plot_pacf

# from sktime.utils import plot_series  # from_2d_array_to_nested
from sktime.datatypes import convert_to, check_raise
import pyflux as pf
from datetime import datetime

from statsmodels.tsa.stattools import adfuller

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from pmdarima.arima.utils import ndiffs

df = pd.read_csv("../assets/train_3.csv")
df["Date"] = pd.to_datetime(df["Date"])
# df.set_index("Date", inplace=True)

# df.index.to_period("M")
# df.set_columns(["Dates", ""])
# df.rename(columns={"Date": "Period", "Sales": ""}, inplace=True)

# df = df.groupby(pd.Grouper(key="Date", freq="M")).sum()

# df.index = df.index.strftime("%Y-%m")
# print(df)

# # check for the null values
# # miss_arr = train_data.isna().sum()


# # l = len(train_data.columns)

# # train_arr = [i for i in range(0, l - 1)]

# # print(train_data.columns[l - 1])

# # print(len(train_data.columns))

# # X_train, X_test, y_train, y_test = train_test_split(
# #     train_data.iloc[:, train_arr],
# #     train_data.iloc[:, [l - 1]],
# #     test_size=0.2,
# #     random_state=1,
# # )

# # LogisticRegressionPipeline = Pipeline(
# #     [
# #         ("myscalar", MinMaxScaler()),
# #         ("mypca", PCA(n_components=3)),
# #         ("logistic_regression", LogisticRegression()),
# #     ]
# # )

# # res = LogisticRegressionPipeline.fit(X_train, y_train)

# # print(res)


# df["Date"] = pd.to_datetime(df["Date"])

# dg = df.groupby(pd.Grouper(key="Date", freq="M")).sum()  # groupby each 1 month
# dg.index = dg.index.strftime("%Y-%m")

# print(dg)

# plt.style.use("_mpl-gallery")

# fig, ax = plt.subplots()

# ax.plot(dg.index, dg["Sales"], linewidth=2.0)

# plt.show()

print("-------------------------------------------------")


# y = from_2d_array_to_nested(dg)

# dg = dg.convert_dtypes()
# y = df.as_matrix()


# convert_to(y, to_type="pd.DataFrame")

# check_raise(dg, mtype="pd.Series")

# y = load_airline()
# y = df
# df = df[["Sales"]].copy()
print(df)
n = ndiffs(df.Sales, test="adf")
print(n)

# X = np.array(df["Sales"]).reshape(-1, 1)

# y = np.array(df["Date"]).reshape(-1, 1)

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)


# regr = LinearRegression()

# regr.fit(X_train, y_train)

# print(regr.score(X_test, y_test))

# y_pred = regr.predict(X_test)

# plt.scatter(X_test, y_test, color="b")

# plt.plot(X_test, y_pred, color="k")

# plt.show()

# result = adfuller(y, autolag="AIC")

# print("ADF Statistic: %f" % result[0])

# print("p-value: %f" % result[1])

# print("Critical Values:")

# for key, value in result[4].items():
#     print("\t%s: %.3f" % (key, value))
# if result[0] < result[4]["5%"]:
#     print("Reject Ho - Time Series is Stationary")
# else:
#     print("Failed to Reject Ho - Time Series is Non-Stationary")

# print(y.size)

# y_train, y_test = temporal_train_test_split(y, test_size=0.25)


# x = autocorrelation_plot(y)  # p = 1, 2
# # print(x.values)
# plt.show()

# # d = 1, 2

# plot_pacf(y, lags=13)  # q =7
# plt.show()

# forecaster = ARIMA(order=(0, 1, 2), suppress_warnings=True)
# forecaster.fit(y_train)
# n = 24
# y_pred = forecaster.predict(fh=list(range(1, int((y.size * 0.25) + 1))))


# print(y_pred)

# y_pred.index = y_pred.index.strftime("%b-%y")

# print(y_pred)
# df.index = df.index.strftime("%b-%y")
# y_pred.index = y_pred.index.strftime("%b-%y")

# plt.plot(df.index, df["Sales"])
# plt.plot(y_pred.index, y_pred["Sales"], "-r")
# plt.show()
# model = pf.ARIMA(data=dg, ar=4, ma=4, target='Sales', family=pf.Normal())


# y_train, y_test = temporal_train_test_split(y, test_size=0.25)

# fh = list(range(1, int((y.size * 0.25) + 1)))

# forecaster = AutoARIMA()

# forecaster.fit(y_train)

# y_pred = forecaster.predict(fh)


# plot_series(y_train, y_test, y_pred, labels=["Train", "Test", "Pred"])

# plt.show()
