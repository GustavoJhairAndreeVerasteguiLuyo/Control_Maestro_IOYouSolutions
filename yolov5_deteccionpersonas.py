from ultralytics import YOLO
import cv2

model = YOLO('yolov5s.pt')  # o yolov8n.pt si usas v8
frame = cv2.imread("entrada.jpg")

results = model(frame)
results.print()
results.show()  # muestra imagen con las detecciones

for result in results:
    for box in result.boxes:
        if box.cls == 0:  # clase 'person'
            print("Persona detectada en coordenadas:", box.xyxy)
