from conexion import obtener_conexion
from datetime import datetime

class GestorDatos:
    def __init__(self):
        self.cliente_edicion = None
        self.factura_edicion = None
        self.pago_edicion = None

    # ==================== CLIENTES ====================
    def verificar_usuario(self, usuario, password):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = %s AND password = %s", 
            (usuario, password)
        )
        fila = cursor.fetchone()
        conexion.close()
        return fila is not None 
    
    def obtener_clientes(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes")
        columnas = [col[0] for col in cursor.description]
        filas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        conexion.close()
        return filas

    def agregar_cliente(self, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, cuit, email, telefono, direccion, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (datos["nombre"], datos["CUIT"], datos["email"], datos["teléfono"], datos["dirección"], 1 if datos["Activo"] else 0))
        conexion.commit()
        nuevo_id = cursor.lastrowid
        conexion.close()
        return nuevo_id

    def actualizar_cliente(self, cliente_id, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE clientes 
            SET nombre=%s, cuit=%s, email=%s, telefono=%s, direccion=%s, activo=%s
            WHERE id_cliente=%s
        """, (datos["nombre"], datos["CUIT"], datos["email"], datos["teléfono"], datos["dirección"], 1 if datos["activo"] else 0, cliente_id))
        conexion.commit()
        conexion.close()

    def eliminar_cliente(self, cliente_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (cliente_id,))
        conexion.commit()
        conexion.close()

    def obtener_cliente(self, cliente_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_cliente AS id_cliente,
                   nombre AS nombre,
                   cuit AS CUIT,
                   email AS email,
                   telefono AS teléfono,
                   direccion AS dirección,
                   saldo AS saldo,
                   activo AS Activo
            FROM clientes WHERE id_cliente=%s
        """, (cliente_id,))
        columnas = [col[0] for col in cursor.description]
        fila = cursor.fetchone()
        conexion.close()
        return dict(zip(columnas, fila)) if fila else None

    # ==================== FACTURAS ====================
    def obtener_facturas(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT f.id_factura as id, 
                   c.nombre as Cliente, 
                   f.fecha as Fecha, 
                   f.monto as Importe, 
                   f.estado as Estado
            FROM facturas f
            JOIN clientes c ON f.id_cliente = c.id_cliente
        """)
        columnas = [col[0] for col in cursor.description]
        filas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        conexion.close()
        return filas

    def agregar_factura(self, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = %s", (datos["Cliente"],))
            res_cliente = cursor.fetchone()
            if not res_cliente:
                raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
            id_cliente = res_cliente[0]

            # Convertir fecha de DD/MM/YYYY a YYYY-MM-DD para MySQL
            try:
                fecha = datetime.strptime(datos["Fecha"], "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                fecha = datos["Fecha"]

            monto = float(datos["Importe"].replace(",", "."))
            estado = datos["Estado"].strip().upper()

            cursor.execute("""
                INSERT INTO facturas (id_cliente, fecha, monto, estado)
                VALUES (%s, %s, %s, %s)
            """, (id_cliente, fecha, monto, estado))
            
            conexion.commit()
            nuevo_id = cursor.lastrowid
            return nuevo_id
        except Exception as e:
            conexion.rollback()
            raise e
        finally:
            conexion.close()

    def actualizar_factura(self, factura_id, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = %s", (datos["Cliente"],))
            res_cliente = cursor.fetchone()
            if not res_cliente:
                raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
            id_cliente = res_cliente[0]

            # Convertir fecha de DD/MM/YYYY a YYYY-MM-DD para MySQL
            try:
                fecha = datetime.strptime(datos["Fecha"], "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                fecha = datos["Fecha"]

            monto = float(datos["Importe"].replace(",", "."))
            estado = datos["Estado"].strip().upper()

            cursor.execute("""
                UPDATE facturas 
                SET id_cliente = %s, fecha = %s, monto = %s, estado = %s
                WHERE id_factura = %s
            """, (id_cliente, fecha, monto, estado, factura_id))
            
            conexion.commit()
        except Exception as e:
            conexion.rollback()
            raise e
        finally:
            conexion.close()

    def eliminar_factura(self, factura_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM facturas WHERE id_factura = %s", (factura_id,))
        conexion.commit()
        conexion.close()

    def obtener_factura(self, factura_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT f.id_factura AS id, 
                   c.nombre AS Cliente, 
                   f.fecha AS Fecha, 
                   f.monto AS Importe, 
                   f.estado AS Estado
            FROM facturas f
            JOIN clientes c ON f.id_cliente = c.id_cliente
            WHERE f.id_factura = %s
        """, (factura_id,))
        columnas = [col[0] for col in cursor.description]
        fila = cursor.fetchone()
        conexion.close()
        return dict(zip(columnas, fila)) if fila else None

    # ==================== PAGOS ====================
    def obtener_pagos(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.id_pago AS id, 
                   c.nombre AS Cliente, 
                   f.numero AS Factura, 
                   p.fecha AS Fecha, 
                   p.monto AS Monto, 
                   p.metodo_pago AS 'Medio de pago'
            FROM pagos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            JOIN facturas f ON p.id_factura = f.id_factura
        """)
        columnas = [col[0] for col in cursor.description]
        filas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        conexion.close()
        return filas

    def agregar_pago(self, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = %s", (datos["Cliente"],))
            resultado_cliente = cursor.fetchone()
            if not resultado_cliente:
                raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
            id_cliente = resultado_cliente[0]

            cursor.execute("SELECT id_factura FROM facturas WHERE id_cliente = %s LIMIT 1", (id_cliente,))
            resultado_factura = cursor.fetchone()
            if not resultado_factura:
                raise Exception("El cliente seleccionado no tiene facturas registradas para asociar al pago.")
            id_factura = resultado_factura[0]

            # Convertir fecha de DD/MM/YYYY a YYYY-MM-DD para MySQL
            try:
                fecha = datetime.strptime(datos["Fecha"], "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                fecha = datos["Fecha"]

            monto = float(datos["Monto"].replace(",", "."))
            metodo_pago = datos["Medio de pago"].strip().upper() 

            cursor.execute("""
                INSERT INTO pagos (id_cliente, id_factura, fecha, monto, metodo_pago)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_cliente, id_factura, fecha, monto, metodo_pago))

            conexion.commit()
        except Exception as e:
            conexion.rollback()
            raise e
        finally:
            conexion.close()

    def actualizar_pago(self, pago_id, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = %s", (datos["Cliente"],))
            res_cliente = cursor.fetchone()
            if not res_cliente:
                raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
            id_cliente = res_cliente[0]

            cursor.execute("SELECT id_factura FROM facturas WHERE id_cliente = %s LIMIT 1", (id_cliente,))
            res_factura = cursor.fetchone()
            if not res_factura:
                raise Exception("El cliente seleccionado no tiene facturas registradas para asociar al pago.")
            id_factura = res_factura[0]

            fecha = datos["Fecha"]
            monto = float(datos["Monto"].replace(",", "."))
            metodo_pago = datos["Medio de pago"].strip().upper()

            cursor.execute("""
                UPDATE pagos 
                SET id_cliente = %s, id_factura = %s, fecha = %s, monto = %s, metodo_pago = %s
                WHERE id_pago = %s
            """, (id_cliente, id_factura, fecha, monto, metodo_pago, pago_id))
            
            conexion.commit()
        except Exception as e:
            conexion.rollback()
            raise e
        finally:
            conexion.close()

    def eliminar_pago(self, pago_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM pagos WHERE id_pago = %s", (pago_id,))
        conexion.commit()
        conexion.close()

    def obtener_pago(self, pago_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.id_pago AS id, 
                   c.nombre AS Cliente, 
                   p.fecha AS Fecha, 
                   p.monto AS Monto, 
                   p.metodo_pago AS 'Medio de pago'
            FROM pagos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE p.id_pago = %s
        """, (pago_id,))
        columnas = [col[0] for col in cursor.description]
        fila = cursor.fetchone()
        conexion.close()
        return dict(zip(columnas, fila)) if fila else None