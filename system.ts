interface BootResult {
  success: boolean;
  message: string;
  status?: number;
  durationMs?: number;
}

export const bootSystem = async (
  endpoint: string = "http://localhost:5000/boot",
  retries: number = 3,
  timeout: number = 5000
): Promise<BootResult> => {
  const controller = new AbortController();
  const signal = controller.signal;

  const timer = setTimeout(() => {
    controller.abort();
  }, timeout);

  let attempt = 0;
  const startTime = performance.now();

  while (attempt < retries) {
    attempt++;
    try {
      const response = await fetch(endpoint, { signal });
      clearTimeout(timer);

      const data = await response.text();
      if (!response.ok) {
        return {
          success: false,
          message: `Error del servidor: ${response.status}`,
          status: response.status,
        };
      }

      const duration = Math.round(performance.now() - startTime);
      return {
        success: true,
        message: data || "Arranque exitoso.",
        durationMs: duration,
        status: response.status,
      };
    } catch (err: any) {
      if (err.name === "AbortError") {
        console.warn(`[Intento ${attempt}] Tiempo de espera agotado (${timeout}ms).`);
        return {
          success: false,
          message: "Tiempo de espera agotado al intentar arrancar el sistema.",
        };
      }

      console.warn(`[Intento ${attempt}] Error al arrancar:`, err.message);

      if (attempt === retries) {
        return {
          success: false,
          message: `Fallo después de ${retries} intentos: ${err.message}`,
        };
      }
    }
  }

  return {
    success: false,
    message: "Error desconocido.",
  };
};
