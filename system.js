export const bootSystem = async () => {
  const response = await fetch("http://localhost:5000/boot");
  if (!response.ok) {
    throw new Error(`Error del servidor: ${response.status}`);
  }
  return await response.text();
};
