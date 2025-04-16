
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using System.Text.Json;
using System.IO;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var logger = app.Logger;

// Ruta de programas COBOL (por seguridad, ruta fija)
string cobolProgramPath = "/usr/local/bin/";

app.MapGet("/boot/{program}", async (HttpContext context, string program) =>
{
    using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(10));

    try
    {
        if (string.IsNullOrWhiteSpace(program) || program.Contains(".."))
        {
            context.Response.StatusCode = 400;
            await context.Response.WriteAsync("Programa inválido");
            return;
        }

        var output = await RunCobolProgramAsync(program, cts.Token);

        context.Response.ContentType = "application/json";
        await context.Response.WriteAsync(JsonSerializer.Serialize(new
        {
            success = true,
            program,
            timestamp = DateTime.UtcNow,
            output
        }));
    }
    catch (OperationCanceledException)
    {
        logger.LogWarning("Timeout ejecutando COBOL: {Program}", program);
        context.Response.StatusCode = 504;
        await context.Response.WriteAsync("Timeout ejecutando COBOL");
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

// Nuevo endpoint para ver logs del sistema
app.MapGet("/logs", async context =>
{
    var logFile = "log.txt";
    if (File.Exists(logFile))
    {
        var logs = await File.ReadAllTextAsync(logFile);
        context.Response.ContentType = "text/plain";
        await context.Response.WriteAsync(logs);
    }
    else
    {
        context.Response.StatusCode = 404;
        await context.Response.WriteAsync("Log no encontrado");
    }
});

app.Run();

async Task<string> RunCobolProgramAsync(string program, CancellationToken token)
{
    var startInfo = new ProcessStartInfo
    {
        FileName = $"{cobolProgramPath}{program}",
        RedirectStandardOutput = true,
        RedirectStandardError = true,
        UseShellExecute = false,
        CreateNoWindow = true
    };

    using var process = new Process { StartInfo = startInfo };
    process.Start();

    string output = await process.StandardOutput.ReadToEndAsync();
    string error = await process.StandardError.ReadToEndAsync();

    await process.WaitForExitAsync(token);

    if (!string.IsNullOrEmpty(error))
    {
        throw new Exception($"Error: {error}");
    }

    return output.Trim();
}
