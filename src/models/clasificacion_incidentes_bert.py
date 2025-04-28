from transformers import pipeline

# Modelo más moderno y eficiente
classifier = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/deberta-v3-large-zeroshot-v1",
    device=0  # Si tienes GPU
)

# Texto recibido del sistema de videovigilancia
texto_evento = "Vimos a una persona saltando la cerca de seguridad a las 2AM"

# Etiquetas jerárquicas y especializadas
etiquetas = [
    "intrusión humana",
    "movimiento animal",
    "condición normal",
    "acceso autorizado",
    "error del sistema",
    "caída de cámara",
    "sabotaje",
    "lluvia intensa"
]

# Clasificación con evaluación de certeza
resultado = classifier(texto_evento, etiquetas, multi_label=True)
mejor_clase = resultado["labels"][0]
confianza = resultado["scores"][0]

print(f"📌 Clasificación del evento: {mejor_clase} ({confianza:.2f})")

# Umbral para acción automatizada
if confianza > 0.75 and "intrusión" in mejor_clase:
    print("🚨 Alerta: posible intrusión detectada")
elif confianza < 0.5:
    print("⚠️ Evento ambiguo, requiere revisión humana")
else:
    print("✅ Evento categorizado sin riesgo")
