import { useState } from "react";
import { bootSystem as bootSystemAPI } from "../api/system";
import { toast } from "react-hot-toast";

export function useBootSystem() {
  const [loading, setLoading] = useState(false);
  const [output, setOutput] = useState("");

  const bootSystem = async () => {
    setLoading(true);
    try {
      const text = await bootSystemAPI();
      setOutput(text);
      toast.success("Sistema iniciado correctamente");
    } catch (error) {
      toast.error(error.message || "Error al iniciar el sistema");
    } finally {
      setLoading(false);
    }
  };

  return { loading, output, bootSystem };
}
