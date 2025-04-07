#include <iostream>

void initializeVideoMode() {
    std::cout << "Booting" << std::endl;
}

bool readFirmware() {
    std::cout << "Reading sector from disk..." << std::endl;
    // Simular lectura desde disco o firmware
    return true;
}

void initHardware() {
    std::cout << "USB initialized" << std::endl;
    std::cout << "Serial COM1: Hello" << std::endl;
    std::cout << "Paging enabled" << std::endl;
}

void loadFileSystem() {
    std::cout << "Filesystem mounted" << std::endl;
}

void loadDrivers() {
    std::cout << "Drivers loaded" << std::endl;
}

int main() {
    initializeVideoMode();

    if (readFirmware()) {
        initHardware();
        loadFileSystem();
        loadDrivers();
        std::cout << "Loaded" << std::endl;
        std::cout << "Jumping to firmware..." << std::endl;
    } else {
        std::cout << "Error" << std::endl;
    }

    return 0;
}
