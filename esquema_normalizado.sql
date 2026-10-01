-- ============================================================
-- SCRIPT DDL - SISTEMA DE GESTIÓN CONTABLE (CONTABILIDAD FÁCIL)
-- Versión 3 - Ajustado según el Diccionario de Datos y Modelo 3FN
-- Base de datos: SQLite
-- ============================================================

PRAGMA foreign_keys = ON;


-- ============================================================
-- TABLA: CLIENTES
-- Atributos: id_cliente, cuit, nombre, email, telefono,
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
    activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
);


-- ============================================================
-- TABLA: FACTURAS
-- Relación: CLIENTE (1) ---- EMITE ----> (N) FACTURA
-- Atributos: id_factura, id_cliente (FK), numero, fecha,
--            monto, descripcion, estado
-- ============================================================

CREATE TABLE facturas (
    id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    numero TEXT,
    fecha TEXT NOT NULL DEFAULT (DATE('now')),
    monto REAL NOT NULL CHECK (monto > 0),
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'EMITIDA' CHECK (estado IN ('EMITIDA', 'PAGO PARCIAL', 'PAGADA', 'ANULADA')),

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- ============================================================
-- TABLA: PAGOS
-- Relaciones: 
--   CLIENTE (1) ---- REALIZA ----> (N) PAGO
--   FACTURA (1) ---- RECIBE ----> (N) PAGO
-- Atributos: id_pago, id_cliente (FK), id_factura (FK),
--            fecha, monto, metodo_pago
-- ============================================================

CREATE TABLE pagos (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_factura INTEGER NOT NULL,
    fecha TEXT NOT NULL DEFAULT (DATE('now')),
    monto REAL NOT NULL CHECK (monto > 0),
    metodo_pago TEXT NOT NULL CHECK (metodo_pago IN ('EFECTIVO', 'TRANSFERENCIA', 'CHEQUE', 'MERCADO PAGO', 'TARJETA')),

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (id_factura)
        REFERENCES facturas(id_factura)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- ============================================================
-- TABLA: MOVIMIENTOS
-- Relación: CLIENTE (1) ---- TIENE ----> (N) MOVIMIENTO_CC
-- Atributos: id_movimiento, id_cliente (FK), fecha, monto,
--            tipo, descripcion, saldo_anterior, saldo_nuevo
-- ============================================================

CREATE TABLE movimientos (
    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    fecha TEXT NOT NULL DEFAULT (DATETIME('now')),
    monto REAL NOT NULL CHECK (monto <> 0),
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
-- ÍNDICES DE RENDIMIENTO
-- ============================================================

CREATE INDEX idx_facturas_cliente
ON facturas(id_cliente);

CREATE INDEX idx_pagos_cliente
ON pagos(id_cliente);

CREATE INDEX idx_pagos_factura
ON pagos(id_factura);

CREATE INDEX idx_movimientos_cliente
ON movimientos(id_cliente);
