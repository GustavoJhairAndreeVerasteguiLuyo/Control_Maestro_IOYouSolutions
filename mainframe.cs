using System;
using System.Diagnostics;
using System.IO;

class SecurityBootSystem
{
    static void Main()
    {
        Console.WriteLine("=== SECURE BOOT SYSTEM INITIALIZING ===");
        var stopwatch = Stopwatch.StartNew();

        try
        {
            if (!CheckSystemDependencies())
            {
                LogError("System dependencies check failed.");
                EnterSafeMode();
                return;
            }

            Log("Booting...");
            if (ReadFirmware())
            {
                InitHardware();
                LoadFileSystem();
                LoadDrivers();
                StartSystemClock();

                Log("System successfully loaded.");
                Log("Executing firmware...");
            }
            else
            {
                LogError("Firmware read failure.");
                EnterSafeMode();
            }
        }
        catch (Exception ex)
        {
            LogError($"Exception caught: {ex.Message}");
            EnterSafeMode();
        }
        finally
        {
            stopwatch.Stop();
            Log($"Boot time: {stopwatch.ElapsedMilliseconds}ms");
        }
    }

    static bool CheckSystemDependencies()
    {
        Log("Checking system dependencies...");
        // Simulación: verificar si existe un archivo de config
        return File.Exists("system.config");
    }

    static bool ReadFirmware()
    {
        Log("Reading firmware from sector 2...");
        // Simulación de fallo aleatorio
        bool firmwareOk = new Random().Next(1, 10) > 1; // 90% success
        if (!firmwareOk) return false;

        // Simular validación de checksum o integridad
        Log("Validating firmware integrity...");
        return true;
    }

    static void InitHardware()
    {
        Log("Initializing hardware components...");
        Log(" > USB IRQ configured");
        Log(" > Paging enabled");
        Log(" > COM1 output: Hello");
    }

    static void LoadFileSystem()
    {
        Log("Loading file system from sector 3...");
        // Simular carga de FS
        Log("File system successfully initialized.");
    }

    static void LoadDrivers()
    {
        Log("Loading drivers...");
        Log(" > Disk controller initialized");
        Log(" > Serial COM2 initialized");
    }

    static void StartSystemClock()
    {
        Log("System clock started at: " + DateTime.Now.ToString("HH:mm:ss"));
    }

    static void EnterSafeMode()
    {
        Log("Entering safe boot mode...");
        Log(" > Limited functionality available.");
    }

    static void Log(string message)
    {
        Console.WriteLine($"[INFO] {message}");
    }

    static void LogError(string message)
    {
        Console.ForegroundColor = ConsoleColor.Red;
        Console.WriteLine($"[ERROR] {message}");
        Console.ResetColor();
    }
}

