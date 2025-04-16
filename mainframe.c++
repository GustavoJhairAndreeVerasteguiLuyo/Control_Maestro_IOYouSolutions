#include <iostream>
#include <chrono>
#include <thread>
#include <cstdlib>

// Simular demoras realistas de carga
void esperar(int milisegundos) {
    std::this_thread::sleep_for(std::chrono::milliseconds(milisegundos));
}

// Logger simple
void log(const std::string& mensaje) {
    std::cout << "[INFO] " << mensaje << std::endl;
}

void logError(const std::string& mensaje) {
    std::cerr << "[ERROR] " << mensaje << std::endl;
}

// Módulo de video
void initializeVideoMode() {
    log("Inicializando modo de video...");
    esperar(200);
    log("Modo de video activado");
}

// Lectura de firmware simulada
bool readFirmware() {
    log("Leyendo firmware desde disco...");
    esperar(300);

    // Simular posible fallo de firmware
    if (rand() % 10 == 0) {
        logError("Fallo en la lectura del firmware.");
        return false;
    }

    log("Firmware leído correctamente");
    return true;
}

// Inicialización de hardware
bool initHardware() {
    log("Inicializando hardware...");
    esperar(300);

    log("USB inicializado");
    log("Serial COM1 listo");
    log("Paginación habilitada");

    return true;
}

// Verificar dependencias básicas
bool verifyDependencies() {
    log("Verificando dependencias del sistema...");
    esperar(150);
    // Simular un sistema de detección
    bool all_ok = true;
    if (!all_ok) {
        logError("Dependencias faltantes detectadas");
        return false;
    }

    log("Dependencias verificadas correctamente");
    return true;
}

// Simular carga de sistema de archivos
bool loadFileSystem() {
    log("Montando sistema de archivos...");
    esperar(250);
    log("Sistema de archivos montado con éxito");
    return true;
}

// Simular carga de controladores
bool loadDrivers() {
    log("Cargando controladores...");
    esperar(250);
    log("Controladores cargados correctamente");
    return true;
}

// Simular reloj de sistema
void startSystemClock() {
    log("Reloj del sistema iniciado");
}

int main() {
    srand(time(nullptr));  // Semilla para simulaciones aleatorias

    log("==== INICIO DEL SISTEMA ====");
    initializeVideoMode();

    if (!verifyDependencies()) {
        logError("El sistema no puede continuar sin dependencias.");
        return 1;
    }

    if (!readFirmware()) {
        logError("Fallo crítico: no se pudo leer el firmware.");
        return 1;
    }

    if (!initHardware()) {
        logError("Fallo en la inicialización del hardware.");
        return 1;
    }

    if (!loadFileSystem()) {
        logError("No se pudo montar el sistema de archivos.");
        return 1;
    }

    if (!loadDrivers()) {
        logError("Error al cargar los controladores.");
        return 1;
    }

    startSystemClock();

    log("Sistema cargado exitosamente.");
    log("Saltando al firmware...");

    log("==== SISTEMA LISTO ====");

    return 0;
}
