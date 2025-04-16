from ISR.models import RDN
from PIL import Image, ImageEnhance
import os
import sys

def cargar_imagen(path, reducir_res=True):
    try:
        img = Image.open(path).convert("RGB")
        if reducir_res:
            img = img.resize((img.width // 2, img.height // 2))
        return img
    except Exception as e:
        print(f"[ERROR] No se pudo cargar la imagen: {e}")
        return None

def procesar_imagen(modelo, img, mejorar_nitidez=True):
    try:
        sr_img = modelo.predict(img)
        sr_img = Image.fromarray(sr_img)
        if mejorar_nitidez:
            sr_img = ImageEnhance.Sharpness(sr_img).enhance(1.2)
        return sr_img
    except Exception as e:
        print(f"[ERROR] No se pudo procesar la imagen: {e}")
        return None

def guardar_imagen(img, nombre_salida):
    try:
        img.save(nombre_salida)
        print(f"[INFO] Imagen mejorada guardada en: {nombre_salida}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar la imagen: {e}")

def comparar_original_y_mejorado(original, mejorado):
    from matplotlib import pyplot as plt
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(original)
    plt.title("Original (baja resolución)")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(mejorado)
    plt.title("Superresolución")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def main():
    modelo = RDN(weights='psnr-small')
    ruta = 'frame_borroso.jpg'
    img = cargar_imagen(ruta)

    if img:
        imagen_mejorada = procesar_imagen(modelo, img)
        if imagen_mejorada:
            salida = 'frame_mejorado.jpg'
            guardar_imagen(imagen_mejorada, salida)
            comparar_original_y_mejorado(img, imagen_mejorada)
        else:
            print("[ERROR] La imagen no pudo ser mejorada.")
    else:
        print("[ERROR] No se pudo cargar la imagen de entrada.")

if __name__ == "__main__":
    main()

