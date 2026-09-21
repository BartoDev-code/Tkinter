PRAGMA foreign_keys = ON;

-- ============================================================
-- TABLA: CLIENTES
-- Atributos: id, cuit, nombre, email, telefono,
--            direccion, saldo, activo
-- ============================================================

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    cuit TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE,
    telefono TEXT,
    direccion TEXT,
    saldo REAL NOT NULL DEFAULT 0.0,
    activo INTEGER NOT NULL DEFAULT 1
);


-- ============================================================
-- TABLA: FACTURAS
-- Relación: CLIENTE (1) ---- EMITE ----> (N) FACTURA
-- Atributos: id, monto, descripcion, fecha, id_cliente (FK)
-- ============================================================

CREATE TABLE facturas (
    id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    numero TEXT,
    fecha TEXT NOT NULL DEFAULT (DATE('now')),
    monto REAL NOT NULL CHECK (monto > 0),
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'EMITIDA',

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- ============================================================
-- TABLA: PAGOS
-- Relación: CLIENTE (1) ---- REALIZA ----> (N) PAGO
-- Atributos: id, monto, metodo_pago, fecha, id_cliente (FK)
-- ============================================================

CREATE TABLE pagos (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    fecha TEXT NOT NULL DEFAULT (DATE('now')),
    monto REAL NOT NULL CHECK (monto > 0),
    metodo_pago TEXT NOT NULL,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- ============================================================
-- TABLA: MOVIMIENTOS
-- Relación: CLIENTE (1) ---- TIENE ----> (N) MOVIMIENTO_CC
-- Atributos: id, fecha, monto, descripcion,
--            saldo_anterior, saldo_nuevo, tipo, id_cliente (FK)
-- ============================================================

CREATE TABLE movimientos (
    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    fecha TEXT NOT NULL DEFAULT (DATETIME('now')),
    monto REAL NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('DEBITO', 'CREDITO')),
    descripcion TEXT,
    saldo_anterior REAL NOT NULL DEFAULT 0.0,
    saldo_nuevo REAL NOT NULL DEFAULT 0.0,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- ============================================================
-- ÍNDICES
-- ============================================================

CREATE INDEX idx_facturas_cliente
ON facturas(id_cliente);

CREATE INDEX idx_movimientos_cliente
ON movimientos(id_cliente);

CREATE INDEX idx_pagos_cliente
ON pagos(id_cliente);