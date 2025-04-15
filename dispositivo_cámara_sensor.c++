#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <stdexcept>
#include <mutex>

// Simulación de sensores de movimiento
bool detectaMovimiento() {
    // Simulación de detección de movimiento
    std::this_thread::sleep_for(std::chrono::milliseconds(500));  // Simula el tiempo de espera
    return true;  // Simula que siempre detecta movimiento
}

// Simulación de captura de imagen
std::string capturarImagen() {
    std::this_thread::sleep_for(std::chrono::milliseconds(300));  // Simula el tiempo de captura
    return "imagen_base64_simulada";
}

// Función para enviar la imagen al servidor de forma eficiente y segura (con un timeout)
void enviarServidor(const std::string& imagen) {
    try {
        std::cout << "[IOT] Enviando imagen al servidor..." << std::endl;

        // Aquí deberías usar libcurl para enviar la imagen
        // Simulación de envío
        std::this_thread::sleep_for(std::chrono::milliseconds(800)); // Simula el tiempo de transmisión

        // En un entorno real, podrías tener algo como:
        // curl_easy_setopt(curl, CURLOPT_URL, "http://mi-servidor.com/upload");
        // curl_easy_setopt(curl, CURLOPT_POSTFIELDS, imagen.c_str());
        // curl_easy_perform(curl);
    } catch (const std::exception& e) {
        std::cerr << "Error al enviar la imagen al servidor: " << e.what() << std::endl;
    }
}

// Función que ejecuta la detección de movimiento y captura en un hilo paralelo
void detectarYCapturar() {
    try {
        if (detectaMovimiento()) {
            std::string imagen = capturarImagen();
            if (imagen.empty()) {
                throw std::runtime_error("Imagen no válida, no se puede enviar.");
            }
            enviarServidor(imagen);
        } else {
            std::cout << "[IOT] No se detectó movimiento." << std::endl;
        }
    } catch (const std::exception& e) {
        std::cerr << "[ERROR] " << e.what() << std::endl;
    }
}

int main() {
    std::cout << "Dispositivo IoT Iniciado" << std::endl;

    // Lanzamos un hilo para la detección y captura en segundo plano
    std::thread sensorThread(detectarYCapturar);

    // Hacemos otras operaciones si es necesario, mientras se ejecuta el hilo de sensores
    std::cout << "[IOT] Realizando otras tareas en paralelo..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(2));  // Simulamos otras tareas

    // Esperamos que el hilo de sensor termine
    sensorThread.join();

    std::cout << "Proceso finalizado" << std::endl;
    return 0;
}
