/*
File: public/index.html
*/
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Sistema de Videovigilancia Ciudadana</title>
  <link href="/dist/output.css" rel="stylesheet" /> <!-- Tailwind CSS output -->
</head>
<body>
  <div id="root"></div>
  <script src="/src/index.js"></script>
</body>
</html>

/*
File: tailwind.config.js
*/
module.exports = {
  content: ['./public/**/*.html', './src/**/*.{js,jsx}'],
  theme: { extend: {} },
  plugins: [],
};

/*
File: postcss.config.js
*/
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};

/*
File: src/index.css
*/
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Archivo principal de estilos adicionales */

/*
File: package.json
*/
{
  "name": "control-maestro-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-hot-toast": "^2.0.0"
  },
  "devDependencies": {
    "tailwindcss": "^3.0.0",
    "postcss": "^8.0.0",
    "autoprefixer": "^10.0.0",
    "vite": "^4.0.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "serve": "vite preview"
  }
}

/*
File: src/index.js
*/
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

/*
File: src/App.jsx
*/
import React from 'react';
import { useBootSystem } from './hooks/useBootSystem';
import Spinner from './components/Spinner';
import { Toaster } from 'react-hot-toast';

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
        {loading ? 'Iniciando...' : 'Iniciar Sistema'}
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

/*
File: src/hooks/useBootSystem.js
*/
import { useState } from 'react';
import toast from 'react-hot-toast';

export function useBootSystem() {
  const [loading, setLoading] = useState(false);
  const [output, setOutput] = useState('');

  const bootSystem = async () => {
    setLoading(true);
    setOutput('');
    toast.loading('Iniciando sistema...');
    try {
      const res = await fetch('/boot/mi_programa');
      if (!res.ok) throw new Error(`Error: ${res.status}`);
      const text = await res.text();
      setOutput(text);
      toast.success('Sistema iniciado con éxito');
    } catch (err) {
      setOutput(err.message);
      toast.error('Fallo al iniciar sistema');
    } finally {
      setLoading(false);
    }
  };

  return { loading, output, bootSystem };
}

/*
File: src/components/Spinner.jsx
*/
import React from 'react';

const Spinner = () => (
  <svg
    className="animate-spin h-5 w-5 text-white"
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
  >
    <circle
      className="opacity-25"
      cx="12"
      cy="12"
      r="10"
      stroke="currentColor"
      strokeWidth="4"
    ></circle>
    <path
      className="opacity-75"
      fill="currentColor"
      d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
    ></path>
  </svg>
);

export default Spinner;
