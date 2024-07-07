import pandas as pd

df = pd.read_excel("/Users/mac/Downloads/student.xlsx")
print(df)
x = df[["class"]].values
y = df[["mark"]].values

from sklearn.linear_model import LinearRegression as lr

model = lr()

model.fit(x, y)

y_pred = model.predict(x)
print(y)
print(y_pred)


import matplotlib.pyplot as plt

plt.scatter(x, y)
# plt.plot(x,y)
plt.show()

plt.scatter(x, y_pred)
plt.plot(x, y_pred)
plt.show()

from sklearn.metrics import r2_score

print("Accuracy : ", r2_score(y, y_pred))
