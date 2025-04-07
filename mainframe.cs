using System;

class SecurityBootSystem
{
    static void Main()
    {
        Console.WriteLine("Booting");

        if (ReadFirmware())
        {
            InitHardware();
            LoadFileSystem();
            LoadDrivers();
            Console.WriteLine("Loaded");
            Console.WriteLine("Executing firmware...");
        }
        else
        {
            Console.WriteLine("Error");
        }
    }

    static bool ReadFirmware()
    {
        Console.WriteLine("Reading firmware from sector 2...");
        // Aquí iría el acceso real a disco o almacenamiento
        return true;
    }

    static void InitHardware()
    {
        Console.WriteLine("USB IRQ Configured");
        Console.WriteLine("Paging Enabled");
        Console.WriteLine("COM1 output: Hello");
    }

    static void LoadFileSystem()
    {
        Console.WriteLine("Filesystem initialized from sector 3...");
    }

    static void LoadDrivers()
    {
        Console.WriteLine("Disk controller and Serial COM2 initialized");
    }
}
