import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pmdarima.arima.utils import ndiffs

from statsmodels.graphics.tsaplots import plot_pacf, plot_acf

from statsmodels.tsa.arima.model import ARIMA

from statsmodels.graphics.tsaplots import plot_predict

# import statsmodels.api as sm

df = pd.read_csv("../assets/train_1.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.groupby(pd.Grouper(key="Date", freq="M")).sum()
print(df)

d = ndiffs(df.Sales, test="adf")
print(d)

diff = df.Sales.dropna()
n = d
while n > 0:
    diff = df.Sales.diff().dropna()
    n = n - 1

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))

ax1.plot(diff)
ax1.set_title("Difference " + str(d) + " times")
# ax1.set_title("")
ax2.set_ylim(0, 1)

plot_pacf(diff, ax=ax2)
# plt.show()

p = 0

diff = df.Sales.diff().dropna()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))

ax1.plot(diff)
ax1.set_title("Difference " + str(d) + " times")
ax2.set_ylim(0, 1)

plot_acf(diff, ax=ax2)

# plt.show()

q = 2  # 26


# ARIMA Model
model = ARIMA(df.Sales, order=(1, 0, 9))
result = model.fit()

# model = sm.tsa.arima.ARIMA(df.Sales, order=(0, 0, 2))
# result = model.fit(disp=0)

print(result.summary())

# result.plot_predict(static=1, end=60, dynamic=False)
plot_predict(result)
plt.show()
