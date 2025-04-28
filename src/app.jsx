import React from "react";
import { useBootSystem } from "./hooks/useBootSystem";
import Spinner from "./components/Spinner";
import { Toaster } from "react-hot-toast";

function App() {
  const { loading, output, bootSystem } = useBootSystem();

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6">
      <Toaster position="top-right" />
      <h1 className="text-2xl font-bold mb-4 text-center">
        Sistema de Videovigilancia Ciudadana
      </h1>

      <button
        onClick={bootSystem}
        disabled={loading}
        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded shadow-md flex items-center gap-2 disabled:opacity-50"
      >
        {loading && <Spinner />}
        {loading ? "Iniciando..." : "Iniciar Sistema"}
      </button>

      {output && (
        <pre className="mt-4 bg-white p-4 rounded shadow max-w-full overflow-auto whitespace-pre-wrap">
          {output}
        </pre>
      )}
    </div>
  );
}

export default App;
