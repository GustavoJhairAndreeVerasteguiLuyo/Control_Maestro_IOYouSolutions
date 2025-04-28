from ultralytics import YOLO
import cv2
import os
import numpy as np
import time

# Configuración
CONFIDENCE_THRESHOLD = 0.5
SAVE_RESULTS = True
OUTPUT_DIR = "resultados"
MODEL_PATH = "yolov8n.pt"  # También puedes usar yolov5s.pt si usás v5

def cargar_imagen(ruta):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"[ERROR] Imagen no encontrada: {ruta}")
    imagen = cv2.imread(ruta)
    if imagen is None:
        raise ValueError("[ERROR] La imagen no se pudo cargar correctamente.")
    return imagen

def procesar_detecciones(results):
    personas = 0
    recortes = []

    for result in results:
        for box in result.boxes:
            clase = int(box.cls)
            conf = float(box.conf)
            if clase == 0 and conf >= CONFIDENCE_THRESHOLD:  # Clase "persona"
                personas += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                recortes.append((x1, y1, x2, y2))

    return personas, recortes

def guardar_resultados(imagen, recortes):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    salida_path = os.path.join(OUTPUT_DIR, f"detectado_{timestamp}.jpg")
    cv2.imwrite(salida_path, imagen)

    for i, (x1, y1, x2, y2) in enumerate(recortes):
        recorte = imagen[y1:y2, x1:x2]
        cv2.imwrite(os.path.join(OUTPUT_DIR, f"persona_{i+1}_{timestamp}.jpg"), recorte)

    print(f"[INFO] Resultados guardados en {OUTPUT_DIR}/")

def main():
    print("[INFO] Cargando modelo...")
    model = YOLO(MODEL_PATH)

    print("[INFO] Cargando imagen...")
    frame = cargar_imagen("entrada.jpg")

    print("[INFO] Ejecutando detección...")
    results = model(frame)

    personas, recortes = procesar_detecciones(results)

    print(f"[INFO] Personas detectadas: {personas}")
    if personas == 0:
        print("[INFO] No se detectaron personas.")
    else:
        results[0].plot()  # dibuja los resultados en la imagen

        if SAVE_RESULTS:
            guardar_resultados(results[0].orig_img, recortes)

    results[0].show()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
