import pandas as pd

df=pd.read_csv("Data-sets/drug200.csv")

# print(df.head())


#pre-procesing
# print(df.columns)
x=df[['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']]
y=df['Drug']

#-------------------------

# Convert categorical features to numerical using one-hot encoding
# from sklearn.preprocessing import OneHotEncoder
# enc = OneHotEncoder()
# X_encoded = enc.fit_transform(x).toarray()


#-------------------------

from sklearn.preprocessing import LabelEncoder
label_encoder=LabelEncoder()
x['Sex']=label_encoder.fit_transform(x["Sex"])
x['BP']=label_encoder.fit_transform(x["BP"])
x['Cholesterol']=label_encoder.fit_transform(x["Cholesterol"])

print("Data : \n\n",x,"\n\n")


from sklearn.model_selection import train_test_split 
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=5)


from sklearn.tree import DecisionTreeClassifier 
# clf= DecisionTreeClassifier(criterion="gini",max_depth=4)
# clf= DecisionTreeClassifier(criterion="entropy",max_depth=4)
clf= DecisionTreeClassifier(criterion="log_loss",max_depth=4)
print("\n\nModel : ",clf)
clf.fit(x_train,y_train)


y_pred=clf.predict(x_test)



# print(y_pred)

from sklearn.metrics import accuracy_score

print(accuracy_score(y_test,y_pred))


print(y_test[:5])
print(y_pred[:5])



#visualization

import matplotlib.pyplot as plt
import sklearn.tree as tree
tree.plot_tree(clf)
plt.show()




# classification matrics?

# gini index?


