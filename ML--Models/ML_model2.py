import pandas as pd
from sklearn.linear_model import LinearRegression as lr
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import numpy as np


df = pd.read_csv('Data-sets/Car_sales.csv')

price = df[["Price_in_thousands"]].multiply(1000).dropna()

milage = df['Fuel_efficiency'].dropna()


price.insert(1, 'Milage', milage, True)
n_df = price

n_df.dropna(inplace=True)
print(n_df.isnull().sum())

print(n_df.shape)

x = n_df[["Price_in_thousands"]].values
y = n_df["Milage"].values

# x=np.delete(x,[1,3])  #to delete values 
# y=y[~np.isnan(y)]  #removes nan value--needs exp?     #~ operator is the bitwise complement operator. It is used to invert the bits of an integer or a Boolean value.

# checking array dimentions
print(x.ndim)
print(y.ndim)


# calling the regressor
model = lr()

# Training the model
model.fit(x, y)

# getting predicted output
y_pred = model.predict(x)

plt.scatter(x, y, color="grey", label="Actual data")  # actual data
# predicted output/ best fit line
plt.plot(x, y_pred, color='red', label="Best fit line")
plt.legend()
plt.title("Car Prize and Milage")
plt.show()


r2 = r2_score(y, y_pred)
print(r2)
