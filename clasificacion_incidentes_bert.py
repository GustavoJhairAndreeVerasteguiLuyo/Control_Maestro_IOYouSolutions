from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
text = "Vimos a una persona saltando la cerca de seguridad a las 2AM"

labels = ["intrusión", "normal", "falla técnica", "acceso autorizado"]
result = classifier(text, labels)
print("Clasificación:", result['labels'][0])
