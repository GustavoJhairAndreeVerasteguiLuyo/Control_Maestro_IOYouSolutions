from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

# Eventos: [latitud, longitud]
eventos = np.array([
    [10.0, 20.0], [10.2, 20.1], [50.0, 80.0], [49.9, 79.8],
    [9.9, 19.8], [50.2, 80.3]
])

kmeans = KMeans(n_clusters=2)
kmeans.fit(eventos)
etiquetas = kmeans.labels_

plt.scatter(eventos[:, 0], eventos[:, 1], c=etiquetas)
plt.title("Clustering de eventos de seguridad")
plt.show()
