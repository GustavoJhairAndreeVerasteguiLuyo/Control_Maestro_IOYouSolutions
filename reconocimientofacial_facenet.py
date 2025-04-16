import face_recognition
import os
import datetime

# Configuración
KNOWN_DIR = "empleados/"
UNKNOWN_IMAGE = "entrada_actual.jpg"
TOLERANCE = 0.5

def cargar_rostros_known():
    rostros = []
    nombres = []
    for archivo in os.listdir(KNOWN_DIR):
        if archivo.lower().endswith((".jpg", ".png", ".jpeg")):
            ruta = os.path.join(KNOWN_DIR, archivo)
            imagen = face_recognition.load_image_file(ruta)
            codificaciones = face_recognition.face_encodings(imagen)
            if codificaciones:
                rostros.append(codificaciones[0])
                nombres.append(os.path.splitext(archivo)[0])
            else:
                print(f"[ADVERTENCIA] No se detectó rostro en: {archivo}")
    return rostros, nombres

def verificar_acceso(rostros_known, nombres_known):
    try:
        unknown_img = face_recognition.load_image_file(UNKNOWN_IMAGE)
        unknown_encs = face_recognition.face_encodings(unknown_img)

        if not unknown_encs:
            print("[ERROR] No se detectó ningún rostro en la imagen de entrada.")
            return

        unknown_enc = unknown_encs[0]

        distances = face_recognition.face_distance(rostros_known, unknown_enc)
        best_match_idx = distances.argmin()
        if distances[best_match_idx] <= TOLERANCE:
            nombre = nombres_known[best_match_idx]
            print(f"[ACCESO AUTORIZADO] {nombre} - Rostro verificado")
            registrar_evento(nombre, True)
        else:
            print("[ACCESO DENEGADO] Rostro no coincide con ningún empleado registrado")
            registrar_evento("Desconocido", False)

    except FileNotFoundError:
        print(f"[ERROR] Archivo no encontrado: {UNKNOWN_IMAGE}")
    except Exception as e:
        print(f"[ERROR] Ocurrió una excepción: {e}")

def registrar_evento(nombre, acceso_autorizado):
    estado = "AUTORIZADO" if acceso_autorizado else "DENEGADO"
    tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"{tiempo} - {nombre} - {estado}\n"
    with open("registro_accesos.log", "a") as f:
        f.write(log)

if __name__ == "__main__":
    rostros_known, nombres_known = cargar_rostros_known()
    if rostros_known:
        verificar_acceso(rostros_known, nombres_known)
    else:
        print("[ERROR] No se encontraron rostros conocidos para comparar.")
