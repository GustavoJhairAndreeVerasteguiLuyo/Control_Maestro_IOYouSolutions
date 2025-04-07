from sklearn.tree import DecisionTreeClassifier
import pandas as pd

data = pd.DataFrame({
    'zona': [1, 2, 1, 3, 2],
    'hora': [2, 13, 23, 1, 22],
    'incidente': [1, 0, 1, 1, 0]
})

X = data[['zona', 'hora']]
y = data['incidente']

clf = DecisionTreeClassifier()
clf.fit(X, y)

pred = clf.predict([[2, 0]])  # zona 2, medianoche
print("¿Posible incidente?", "Sí" if pred[0] == 1 else "No")
