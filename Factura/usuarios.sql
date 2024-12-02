-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS usuarios;

-- Usar la base de datos
USE usuarios;

-- Crear la tabla users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255) NOT NULL UNIQUE,
    PhoneNumber VARCHAR(20),
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    ConfirmPassword VARCHAR(255) NOT NULL
);

-- Opcional: Insertar un usuario de prueba
INSERT INTO users (Email, PhoneNumber, Username, Password, ConfirmPassword) 
VALUES ('test@example.com', '1234567890', 'testuser', 'testpassword', 'testpassword');

-- Crear o actualizar la tabla productos
CREATE TABLE IF NOT EXISTS productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),        -- Nueva columna para la descripción del producto
    precio DECIMAL(10, 2) NOT NULL,  -- Precio del producto
    existencia INT DEFAULT 0,        -- Cantidad en stock
    unidad VARCHAR(50),              -- Unidad de medida del producto
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Fecha de alta
);

-- Opcional: Insertar un producto de prueba
INSERT INTO productos (nombre, descripcion, precio, existencia, unidad) 
VALUES ('Producto de prueba', 'Descripción del producto de prueba', 99.99, 10, 'pieza');

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100),
    fecha_nacimiento DATE,
    direccion TEXT,
    telefono VARCHAR(15),
    email VARCHAR(100),
    rfc VARCHAR(13)
);

-- Opcional: Insertar un cliente de prueba
INSERT INTO clientes (nombre, apellido_paterno, apellido_materno, fecha_nacimiento, direccion, telefono, email, rfc) 
VALUES ('Juan', 'Pérez', 'González', '1985-05-10', 'Calle 123', '5551234567', 'juan@example.com', 'JUAN850510XYZ');

-- Crear la tabla de encabezado de factura
CREATE TABLE IF NOT EXISTS fact_encab (
    folio INT AUTO_INCREMENT PRIMARY KEY,
    idCliente INT NOT NULL,
    fecha DATE NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (idCliente) REFERENCES clientes(id)
);

-- Agregar campo empresa en fact_encab
ALTER TABLE fact_encab ADD COLUMN empresa VARCHAR(255);

-- Crear la tabla de detalle de factura
CREATE TABLE IF NOT EXISTS fact_detalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    folio INT NOT NULL,
    idProd INT NOT NULL,
    cant INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (folio) REFERENCES fact_encab(folio),
    FOREIGN KEY (idProd) REFERENCES productos(id)
);

-- Opcional: Insertar un encabezado de factura de prueba
INSERT INTO fact_encab (idCliente, fecha, monto, empresa) 
VALUES (1, CURDATE(), 199.98, 'Empresa de prueba');

-- Opcional: Insertar un detalle de factura de prueba
INSERT INTO fact_detalle (folio, idProd, cant, precio_unitario) 
VALUES (1, 1, 2, 99.99);
