using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using System.Diagnostics;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/boot", async context =>
{
    // Simula ejecución COBOL y devuelve su salida
    var output = await RunCobolBootProgram();
    await context.Response.WriteAsync(output);
});

app.Run();

async Task<string> RunCobolBootProgram()
{
    // Aquí podrías ejecutar un binario compilado por GnuCOBOL, por ejemplo.
    var process = new Process
    {
        StartInfo = new ProcessStartInfo
        {
            FileName = "cobcrun",
            Arguments = "seguridad_boot",
            RedirectStandardOutput = true,
            UseShellExecute = false,
            CreateNoWindow = true
        }
    };

    process.Start();
    string result = await process.StandardOutput.ReadToEndAsync();
    process.WaitForExit();
    return result;
}
