-- Crear base de datos
CREATE DATABASE videovigilancia;

-- Conectarse a la base de datos
\c videovigilancia;

-- Tabla de Clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    direccion TEXT,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(15),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Cámaras
CREATE TABLE camaras (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    ubicacion VARCHAR(100),
    modelo VARCHAR(100),
    resolucion VARCHAR(50),
    ip_address VARCHAR(15),
    estado BOOLEAN DEFAULT TRUE,  -- Si la cámara está activa
    fecha_instalacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Sensores
CREATE TABLE sensores (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    tipo_sensor VARCHAR(100),  -- Ejemplo: "Movimiento", "Temperatura"
    ubicacion VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE,  -- Si el sensor está activo
    fecha_instalacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Dispositivos IoT
CREATE TABLE dispositivos_iot (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    tipo_dispositivo VARCHAR(100),  -- Ejemplo: "Cámara IP", "Controlador"
    modelo VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE,  -- Si el dispositivo está activo
    fecha_instalacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Eventos
CREATE TABLE eventos (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    tipo_evento VARCHAR(100),  -- Ejemplo: "Intrusión", "Fallo de cámara"
    descripcion TEXT,
    fecha_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dispositivo_id INT,  -- Referencia al dispositivo o sensor que detectó el evento
    FOREIGN KEY (dispositivo_id) REFERENCES dispositivos_iot(id) ON DELETE SET NULL
);

-- Insertar ejemplos de datos
INSERT INTO clientes (nombre, direccion, email, telefono) VALUES
('Juan Pérez', 'Calle Falsa 123', 'juan.perez@example.com', '123456789');

INSERT INTO camaras (cliente_id, ubicacion, modelo, resolucion, ip_address) VALUES
(1, 'Entrada principal', 'CameraPro X100', '1080p', '192.168.0.101');

INSERT INTO sensores (cliente_id, tipo_sensor, ubicacion) VALUES
(1, 'Movimiento', 'Pasillo 1');

INSERT INTO dispositivos_iot (cliente_id, tipo_dispositivo, modelo) VALUES
(1, 'Cámara IP', 'CameraPro X100');

INSERT INTO eventos (cliente_id, tipo_evento, descripcion, dispositivo_id) VALUES
(1, 'Intrusión', 'Movimiento detectado cerca de la entrada', 1);
