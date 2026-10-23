from conexion import obtener_conexion
from datetime import datetime
import mysql.connector

class GestorDatos:
    def __init__(self):
        self.cliente_edicion = None
        self.factura_edicion = None
        self.pago_edicion = None

    # ==================== CLIENTES ====================
    def verificar_usuario(self, usuario, password):
        conexion = None
        cursor = None
        try:

        
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM usuarios WHERE usuario = %s AND password = %s", 
                (usuario, 1234)
            )
            fila = cursor.fetchone()
            return fila is not None 
        except mysql.connector.Error as err:
            print(f"Error en verificar_usuario: {err}")
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()
    
    def obtener_clientes(self):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM clientes")
            columnas = [col[0] for col in cursor.description]
            filas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
            return filas
        except mysql.connector.Error as err:
            print(f"Error en obtener_clientes: {err}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def agregar_cliente(self, datos):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO clientes (nombre, cuit, email, telefono, direccion, activo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (datos["nombre"], datos["CUIT"], datos["email"], datos["teléfono"], datos["dirección"], 1 if datos["Activo"] else 0))
            conexion.commit()
            nuevo_id = cursor.lastrowid
            return nuevo_id
        except Exception as e:
            if conexion and conexion.is_connected():
                conexion.rollback()
            raise e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def actualizar_cliente(self, cliente_id, datos):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            activo_valor = 1 if datos.get("Activo", datos.get("activo", 1)) else 0

            cursor.execute("""
                UPDATE clientes 
                SET nombre=%s, cuit=%s, email=%s, telefono=%s, direccion=%s, activo=%s
                WHERE id_cliente=%s
            """, (datos["nombre"], datos["CUIT"], datos["email"], datos["teléfono"], datos["dirección"], 1 if datos["activo"] else 0, cliente_id))
            conexion.commit()
        except Exception as e:
            if conexion and conexion.is_connected():
                conexion.rollback()
            raise e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def eliminar_cliente(self, cliente_id):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # 1. Borrar movimientos del cliente
            cursor.execute("DELETE FROM movimientos WHERE id_cliente = %s", (cliente_id,))
            
            # 2. Borrar pagos del cliente
            cursor.execute("DELETE FROM pagos WHERE id_cliente = %s", (cliente_id,))
            
            # 3. Borrar facturas del cliente
            cursor.execute("DELETE FROM facturas WHERE id_cliente = %s", (cliente_id,))
            
            # 4. Finalmente, borrar el cliente
            cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (cliente_id,))
            
            conexion.commit()
        except Exception as e:
            if conexion and conexion.is_connected():
                conexion.rollback()
            raise e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def obtener_cliente(self, cliente_id):
        conexion = None
        cursor = None
        try:
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
            return dict(zip(columnas, fila)) if fila else None
        except mysql.connector.Error as err:
            print(f"Error en obtener_cliente: {err}")
            return None
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    # ==================== FACTURAS ====================
    def obtener_facturas(self):
        conexion = None
        cursor = None
        try:
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
            return filas
        except mysql.connector.Error as err:
            print(f"Error en obtener_facturas: {err}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def agregar_factura(self, datos):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = %s LIMIT 1", (datos["Cliente"],))
            res_cliente = cursor.fetchone()
            if not res_cliente:
                raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
            id_cliente = res_cliente[0]

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

        except mysql.connector.Error as err:
            if conexion and conexion.is_connected():
                conexion.rollback()
            if err.errno == 1264:
                raise Exception("El monto ingresado es demasiado grande para la base de datos.")
            else:
                raise err
            
        except Exception as e:
            if conexion and conexion.is_connected():
                conexion.rollback()
            raise e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def actualizar_factura(self, factura_id, datos):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = %s LIMIT 1", (datos["Cliente"],))
            res_cliente = cursor.fetchone()
            if not res_cliente:
                raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
            id_cliente = res_cliente[0]

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
            if conexion and conexion.is_connected():
                conexion.rollback()
            raise e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def eliminar_factura(self, factura_id):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM facturas WHERE id_factura = %s", (factura_id,))
            conexion.commit()
        except mysql.connector.Error as err:
            if conexion and conexion.is_connected():
                conexion.rollback()
            if err.errno == 1451:
                raise Exception("No se puede eliminar esta factura porque tiene pagos asociados. Debes eliminar los pagos vinculados primero.")
            else:
                raise err
        except Exception as e:
            if conexion and conexion.is_connected():
                conexion.rollback()
            raise e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def obtener_factura(self, factura_id):
        conexion = None
        cursor = None
        try:
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
            return dict(zip(columnas, fila)) if fila else None
        except mysql.connector.Error as err:
            print(f"Error en obtener_factura: {err}")
            return None
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    # ==================== PAGOS ====================
    def obtener_pagos(self):
        conexion = None
        cursor = None
        try:
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
            return filas
        except mysql.connector.Error as err:
            print(f"Error en obtener_pagos: {err}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def agregar_pago(self, datos):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # 1. Obtener ID del cliente
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = %s LIMIT 1", (datos["Cliente"],))
            resultado_cliente = cursor.fetchone()
            if not resultado_cliente:
                raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
            id_cliente = resultado_cliente[0]

            # 2. Obtener factura pendiente del cliente (o la asociada)
            cursor.execute("SELECT id_factura, monto FROM facturas WHERE id_cliente = %s AND estado != 'PAGADA' LIMIT 1", (id_cliente,))
            resultado_factura = cursor.fetchone()
            if not resultado_factura:
                raise Exception("El cliente seleccionado no tiene facturas pendientes de pago.")
            id_factura, monto_factura = resultado_factura[0], resultado_factura[1]

            # Convertir fecha
            try:
                fecha = datetime.strptime(datos["Fecha"], "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                fecha = datos["Fecha"]

            monto_pago = float(datos["Monto"].replace(",", "."))
            metodo_pago = datos["Medio de pago"].strip().upper() 

            # 3. Insertar el pago
            cursor.execute("""
                INSERT INTO pagos (id_cliente, id_factura, fecha, monto, metodo_pago)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_cliente, id_factura, fecha, monto_pago, metodo_pago))

            # 4. Determinar si la factura queda PAGADA o PAGADA_PARCIAL
            # (Opcional: puedes sumar pagos previos si haces pagos fraccionados reales)
            if monto_pago >= float(monto_factura):
                nuevo_estado = 'PAGADA'
            else:
                nuevo_estado = 'PAGADA_PARCIAL'

            cursor.execute("""
                UPDATE facturas SET estado = %s WHERE id_factura = %s
            """, (nuevo_estado, id_factura))

            # 5. Registrar automáticamente el movimiento en la cuenta corriente
            cursor.execute("""
                INSERT INTO movimientos (id_cliente, fecha, monto, tipo, descripcion)
                VALUES (%s, %s, %s, 'CREDITO', %s)
            """, (id_cliente, fecha, monto_pago, f"Pago de factura ID {id_factura}"))

            conexion.commit()
        except Exception as e:
            if conexion and conexion.is_connected():
                conexion.rollback()
            raise e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def actualizar_pago(self, pago_id, datos):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = %s LIMIT 1", (datos["Cliente"],))
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
            if conexion and conexion.is_connected():
                conexion.rollback()
            raise e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def eliminar_pago(self, pago_id):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM pagos WHERE id_pago = %s", (pago_id,))
            conexion.commit()
        except Exception as e:
            if conexion and conexion.is_connected():
                conexion.rollback()
            raise e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def obtener_pago(self, pago_id):
        conexion = None
        cursor = None
        try:
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
            return dict(zip(columnas, fila)) if fila else None
        except mysql.connector.Error as err:
            print(f"Error en obtener_pago: {err}")
            return None
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    # ==================== MOVIMIENTOS ====================

    def obtener_movimientos(self):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT m.id_movimiento AS id, 
                       c.nombre AS Cliente, 
                       m.descripcion AS Descripcion, 
                       m.fecha AS Fecha, 
                       m.monto AS Importe, 
                       m.tipo AS Tipo
                FROM movimientos m
                JOIN clientes c ON m.id_cliente = c.id_cliente
            """)
            columnas = [col[0] for col in cursor.description]
            filas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
            return filas
        except mysql.connector.Error as err:
            print(f"Error en obtener_movimientos: {err}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()

    def agregar_movimiento(self, datos):
        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = %s LIMIT 1", (datos["Cliente"],))
            res_cliente = cursor.fetchone()
            if not res_cliente:
                raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
            id_cliente = res_cliente[0]

            try:
                fecha = datetime.strptime(datos["Fecha"], "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                fecha = datos["Fecha"]

            monto = float(datos["Monto"].replace(",", "."))
            tipo = datos["Tipo"].strip().upper()
            descripcion = datos["Descripción"]

            cursor.execute("""
                INSERT INTO movimientos (id_cliente, fecha, monto, tipo, descripcion)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_cliente, fecha, monto, tipo, descripcion))
            
            conexion.commit()
            return cursor.lastrowid
        except Exception as e:
            if conexion and conexion.is_connected():
                conexion.rollback()
            raise e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conexion and conexion.is_connected():
                conexion.close()