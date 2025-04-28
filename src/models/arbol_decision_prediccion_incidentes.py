import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# ----------------------------
# 1. Datos de entrenamiento
# ----------------------------
data = pd.DataFrame({
    'zona': [1, 2, 1, 3, 2, 3, 1, 2, 3, 1],
    'hora': [2, 13, 23, 1, 22, 20, 3, 14, 5, 0],
    'clima': [0, 1, 0, 0, 1, 1, 0, 1, 0, 0],  # 0: despejado, 1: lluvia
    'persona': [
        'residente', 'visitante', 'trabajador', 'desconocido',
        'residente', 'visitante', 'trabajador', 'desconocido',
        'residente', 'visitante'
    ],
    'incidente': [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
})

# ----------------------------
# 2. Codificar variable categórica
# ----------------------------
le = LabelEncoder()
data['persona_codificada'] = le.fit_transform(data['persona'])

X = data[['zona', 'hora', 'clima', 'persona_codificada']]
y = data['incidente']

# ----------------------------
# 3. División de datos
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ----------------------------
# 4. Modelo robusto
# ----------------------------
clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# ----------------------------
# 5. Evaluación
# ----------------------------
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# ----------------------------
# 6. Predicción ética en caso real
# ----------------------------
zona = 2
hora = 0
clima = 1
persona = 'visitante'  # Ejemplo con valor ético

persona_cod = le.transform([persona])[0]
pred = clf.predict([[zona, hora, clima, persona_cod]])
print("¿Posible incidente?", "Sí" if pred[0] == 1 else "No")
