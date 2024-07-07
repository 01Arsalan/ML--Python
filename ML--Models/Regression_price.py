import pandas as pd

#creating Dataframe
df=pd.read_csv("Data-sets/Housing.csv")

#Spiliting data fraame into input(indenpendent-variable) and output(Dependent-variable)

#print(df.columns)
#['price', 'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad','guestroom', 'basement', 'hotwaterheating', 'airconditioning','parking', 'prefarea', 'furnishingstatus']

x=df[['area', 'bedrooms', 'bathrooms', 'stories','parking', 'mainroad','guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnishingstatus']]
y=df['price']


#Encoding non-numerical columns

from sklearn.preprocessing import LabelEncoder

label_encoder=LabelEncoder()

x['mainroad']=label_encoder.fit_transform(x['mainroad'])
x['guestroom']=label_encoder.fit_transform(x['guestroom'])
x['basement']=label_encoder.fit_transform(x['basement'])
x['hotwaterheating']=label_encoder.fit_transform(x['hotwaterheating'])
x['airconditioning']=label_encoder.fit_transform(x['airconditioning'])
x['prefarea']=label_encoder.fit_transform(x['prefarea'])
x['furnishingstatus']=label_encoder.fit_transform(x['furnishingstatus'])


#Spiliting data into train-test-split
from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=4)


#Decision tree achitecure

from sklearn.linear_model import LinearRegression

clf=LinearRegression()

clf.fit(x_train,y_train)

y_pred=clf.predict(x_test)


#Evaluation
#manual
y_test=y_test.values
print(y_test[:5])
print(y_pred[:5])



#mean_absolute_error
from sklearn.metrics import mean_absolute_error
mae = str(mean_absolute_error(y_test,y_pred))
mae="MAE: "+mae
#auto
import matplotlib.pyplot as plt

plt.plot(range(len(y_test)),y_test,color='blue',label='Test-Data')
plt.plot(range(len(y_pred)),y_pred,color='red',label='Pred-Data')

plt.legend()
plt.show()
