#include <iostream>
#include <string>

// Simulación de sensores
bool detectaMovimiento() {
    return true; // Simula movimiento
}

std::string capturarImagen() {
    return "imagen_base64_simulada";
}

void enviarServidor(const std::string& imagen) {
    std::cout << "[IOT] Enviando imagen al servidor... " << std::endl;
    // Aquí se usaría una librería HTTP como libcurl para enviar la imagen
}

int main() {
    std::cout << "Dispositivo IoT Iniciado" << std::endl;

    if (detectaMovimiento()) {
        std::string imagen = capturarImagen();
        enviarServidor(imagen);
    }

    std::cout << "Proceso finalizado" << std::endl;
    return 0;
}
