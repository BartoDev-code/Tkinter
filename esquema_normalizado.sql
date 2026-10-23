-- ============================================================
-- SCRIPT DDL - CONTABILIDAD FACIL
-- Motor: MySQL
-- ============================================================

CREATE DATABASE IF NOT EXISTS contabilidad_facil;
USE contabilidad_facil;

-- ============================================================
-- TABLA: USUARIOS
-- ============================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT IGNORE INTO usuarios (id_usuario, usuario, password)
VALUES (1, 'admin', '1234');


-- ============================================================
-- TABLA: CLIENTES
-- ============================================================

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    cuit VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(50),
    direccion TEXT,
    saldo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    activo TINYINT NOT NULL DEFAULT 1
        CHECK (activo IN (0, 1))
);


-- ============================================================
-- TABLA: FACTURAS
-- CLIENTES (1) ---- (N) FACTURAS
-- ============================================================

CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    numero VARCHAR(50),
    fecha DATE NOT NULL DEFAULT (CURRENT_DATE),
    monto DECIMAL(10,2) NOT NULL CHECK (monto > 0),
    descripcion TEXT,
    estado VARCHAR(20) NOT NULL DEFAULT 'EMITIDA'
        CHECK (
            estado IN (
                'EMITIDA',
                'PAGADA_PARCIAL',
                'PAGADA',
                'ANULADA'
            )
        ),

    CONSTRAINT fk_facturas_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- ============================================================
-- TABLA: PAGOS
-- CLIENTES (1) ---- (N) PAGOS
-- FACTURAS (1) ---- (N) PAGOS
-- ============================================================

CREATE TABLE IF NOT EXISTS pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_factura INT NOT NULL,
    fecha DATE NOT NULL DEFAULT (CURRENT_DATE),
    monto DECIMAL(10,2) NOT NULL CHECK (monto > 0),
    metodo_pago VARCHAR(50) NOT NULL
        CHECK (
            metodo_pago IN (
                'EFECTIVO',
                'TRANSFERENCIA',
                'CHEQUE',
                'MERCADO PAGO',
                'TARJETA'
            )
        ),

    CONSTRAINT fk_pagos_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_pagos_factura
        FOREIGN KEY (id_factura)
        REFERENCES facturas(id_factura)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- ============================================================
-- TABLA: MOVIMIENTOS
-- CLIENTES (1) ---- (N) MOVIMIENTOS
-- ============================================================

CREATE TABLE IF NOT EXISTS movimientos (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    monto DECIMAL(10,2) NOT NULL CHECK (monto <> 0),
    tipo VARCHAR(20) NOT NULL
        CHECK (tipo IN ('DEBITO', 'CREDITO')),
    descripcion TEXT,
    saldo_anterior DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    saldo_nuevo DECIMAL(10,2) NOT NULL DEFAULT 0.00,

    CONSTRAINT fk_movimientos_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);



