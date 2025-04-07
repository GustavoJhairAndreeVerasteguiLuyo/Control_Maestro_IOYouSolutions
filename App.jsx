import React, { useState } from 'react';

function App() {
  const [output, setOutput] = useState("");

  const bootSystem = async () => {
    const response = await fetch("http://localhost:5000/boot");
    const text = await response.text();
    setOutput(text);
  };

  return (
    <div className="app">
      <h1>Sistema de Videovigilancia Ciudadana</h1>
      <button onClick={bootSystem}>Iniciar Sistema</button>
      <pre>{output}</pre>
    </div>
  );
}

export default App;
