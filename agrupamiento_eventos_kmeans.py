import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans

# ---------- Parámetros de clustering ----------
N_CLUSTERS = 2
BATCH_SIZE = 100  # Ideal para escenarios de múltiples eventos en tiempo real

# ---------- Datos de ejemplo ----------
eventos = np.array([
    [10.0, 20.0], [10.2, 20.1], [50.0, 80.0], [49.9, 79.8],
    [9.9, 19.8], [50.2, 80.3]
])

# ---------- Función para aplicar clustering ----------
def agrupar_eventos(datos, n_clusters=N_CLUSTERS):
    modelo = MiniBatchKMeans(n_clusters=n_clusters, batch_size=BATCH_SIZE)
    modelo.fit(datos)
    return modelo

# ---------- Visualización de resultados ----------
def graficar_clusters(datos, modelo):
    etiquetas = modelo.labels_
    centros = modelo.cluster_centers_

    plt.figure(figsize=(8, 6))
    plt.scatter(datos[:, 0], datos[:, 1], c=etiquetas, cmap='tab10', s=80, alpha=0.7, edgecolors='k')
    plt.scatter(centros[:, 0], centros[:, 1], c='red', s=200, marker='X', label='Centroide')
    plt.title("Clustering de Eventos de Seguridad")
    plt.xlabel("Latitud")
    plt.ylabel("Longitud")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ---------- Ejecución ----------
modelo = agrupar_eventos(eventos)
graficar_clusters(eventos, modelo)
