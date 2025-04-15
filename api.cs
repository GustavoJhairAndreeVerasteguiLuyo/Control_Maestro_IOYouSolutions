using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using System.Diagnostics;
using System.Threading.Tasks;
using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var logger = app.Logger;

// Endpoint generalizado: puedes pasar el nombre del programa COBOL
app.MapGet("/boot/{program}", async (HttpContext context, string program) =>
{
    try
    {
        var output = await RunCobolProgramAsync(program);
        context.Response.ContentType = "application/json";
        await context.Response.WriteAsync(JsonSerializer.Serialize(new
        {
            success = true,
            program,
            output
        }));
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Error ejecutando programa COBOL");

        context.Response.StatusCode = 500;
        await context.Response.WriteAsync(JsonSerializer.Serialize(new
        {
            success = false,
            error = ex.Message
        }));
    }
});

app.Run();

/// <summary>
/// Ejecuta un programa COBOL compilado con GnuCOBOL.
/// </summary>
async Task<string> RunCobolProgramAsync(string programName)
{
    if (string.IsNullOrWhiteSpace(programName))
        throw new ArgumentException("Nombre de programa no válido");

    var process = new Process
    {
        StartInfo = new ProcessStartInfo
        {
            FileName = "cobcrun",
            Arguments = programName,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        }
    };

    process.Start();

    // Lee ambas salidas en paralelo
    var outputTask = process.StandardOutput.ReadToEndAsync();
    var errorTask = process.StandardError.ReadToEndAsync();

    await Task.WhenAll(outputTask, errorTask);
    process.WaitForExit();

    if (process.ExitCode != 0)
        throw new Exception($"Programa '{programName}' terminó con código {process.ExitCode}: {errorTask.Result}");

    return outputTask.Result;
}

