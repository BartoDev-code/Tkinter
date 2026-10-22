from conexion import obtener_conexion

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
            "SELECT * FROM usuarios WHERE usuario = ? AND password = ?", 
            (usuario, password)
        )
        fila = cursor.fetchone()
        conexion.close()
        return fila is not None 
    
    def obtener_clientes(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes")
        filas = [dict(fila) for fila in cursor.fetchall()]
        conexion.close()
        return filas

    def agregar_cliente(self, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes (Nombre, CUIT, Email, Telefono, Direccion, Activo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (datos["Nombre"], datos["CUIT"], datos["Email"], datos["Teléfono"], datos["Dirección"], 1 if datos["Activo"] else 0))
        conexion.commit()
        nuevo_id = cursor.lastrowid
        conexion.close()
        return nuevo_id

    def actualizar_cliente(self, cliente_id, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE clientes 
            SET Nombre=?, CUIT=?, Email=?, Telefono=?, Direccion=?, Activo=?
            WHERE id_cliente=?
        """, (datos["Nombre"], datos["CUIT"], datos["Email"], datos["Teléfono"], datos["Dirección"], 1 if datos["Activo"] else 0, cliente_id))
        conexion.commit()
        conexion.close()

    def eliminar_cliente(self, cliente_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente=?", (cliente_id,))
        conexion.commit()
        conexion.close()

    def obtener_cliente(self, cliente_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id_cliente=?", (cliente_id,))
        fila = cursor.fetchone()
        conexion.close()
        return dict(fila) if fila else None

    # ==================== FACTURAS ====================
    def obtener_facturas(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        # Hacemos un JOIN para traer el nombre del cliente en lugar de solo su ID numérico
        cursor.execute("""
            SELECT f.id_factura as id, 
                   c.nombre as Cliente, 
                   f.fecha as Fecha, 
                   f.monto as Importe, 
                   f.estado as Estado
            FROM facturas f
            JOIN clientes c ON f.id_cliente = c.id_cliente
        """)
        filas = [dict(fila) for fila in cursor.fetchall()]
        conexion.close()
        return filas

    def agregar_factura(self, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            # 1. Buscar el id_cliente a partir del nombre que viene del formulario
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = ?", (datos["Cliente"],))
            res_cliente = cursor.fetchone()
            if not res_cliente:
                raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
            id_cliente = res_cliente[0]

            # 2. Adaptar y validar valores
            fecha = datos["Fecha"]
            monto = float(datos["Importe"].replace(",", "."))
            estado = datos["Estado"].strip().upper()

            # 3. Insertar utilizando los nombres reales de la tabla
            cursor.execute("""
                INSERT INTO facturas (id_cliente, fecha, monto, estado)
                VALUES (?, ?, ?, ?)
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
            # 1. Buscar el id_cliente del cliente seleccionado
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = ?", (datos["Cliente"],))
            res_cliente = cursor.fetchone()
            if not res_cliente:
                raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
            id_cliente = res_cliente[0]

            fecha = datos["Fecha"]
            monto = float(datos["Importe"].replace(",", "."))
            estado = datos["Estado"].strip().upper()

            # 2. Actualizar usando id_factura como clave de búsqueda
            cursor.execute("""
                UPDATE facturas 
                SET id_cliente = ?, fecha = ?, monto = ?, estado = ?
                WHERE id_factura = ?
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
        # Corregido: se elimina por id_factura y no por id_cliente
        cursor.execute("DELETE FROM facturas WHERE id_factura = ?", (factura_id,))
        conexion.commit()
        conexion.close()

    def obtener_factura(self, factura_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        # Corregido: se busca por id_factura utilizando JOIN para traer el nombre del cliente
        cursor.execute("""
            SELECT f.id_factura AS id, 
                   c.nombre AS Cliente, 
                   f.fecha AS Fecha, 
                   f.monto AS Importe, 
                   f.estado AS Estado
            FROM facturas f
            JOIN clientes c ON f.id_cliente = c.id_cliente
            WHERE f.id_factura = ?
        """, (factura_id,))
        fila = cursor.fetchone()
        conexion.close()
        return dict(fila) if fila else None

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
        filas = [dict(fila) for fila in cursor.fetchall()]
        conexion.close()
        return filas

    def agregar_pago(self, datos):
     
    
      conexion = obtener_conexion()
      cursor = conexion.cursor()

      try:
        cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = ?", (datos["Cliente"],))
        resultado_cliente = cursor.fetchone()
        if not resultado_cliente:
            raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
        id_cliente = resultado_cliente[0]

        
        cursor.execute("SELECT id_factura FROM facturas WHERE id_cliente = ? LIMIT 1", (id_cliente,))
        resultado_factura = cursor.fetchone()
        if not resultado_factura:
            raise Exception("El cliente seleccionado no tiene facturas registradas para asociar al pago.")
        id_factura = resultado_factura[0]

        fecha = datos["Fecha"]
        monto = float(datos["Monto"].replace(",", "."))
        
        metodo_pago = datos["Medio de pago"].strip().upper() 

        cursor.execute("""
            INSERT INTO pagos (id_cliente, id_factura, fecha, monto, metodo_pago)
            VALUES (?, ?, ?, ?, ?)
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
            # 1. Buscar el id_cliente a partir del nombre que viene del formulario
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = ?", (datos["Cliente"],))
            res_cliente = cursor.fetchone()
            if not res_cliente:
                raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
            id_cliente = res_cliente[0]

            # 2. Buscar una factura válida para asociar al pago
            cursor.execute("SELECT id_factura FROM facturas WHERE id_cliente = ? LIMIT 1", (id_cliente,))
            res_factura = cursor.fetchone()
            if not res_factura:
                raise Exception("El cliente seleccionado no tiene facturas registradas para asociar al pago.")
            id_factura = res_factura[0]

            fecha = datos["Fecha"]
            monto = float(datos["Monto"].replace(",", "."))
            metodo_pago = datos["Medio de pago"].strip().upper()

            # 3. Actualizar utilizando los nombres reales de las columnas y id_pago
            cursor.execute("""
                UPDATE pagos 
                SET id_cliente = ?, id_factura = ?, fecha = ?, monto = ?, metodo_pago = ?
                WHERE id_pago = ?
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
        # Corregido: se usa id_pago en lugar de id
        cursor.execute("DELETE FROM pagos WHERE id_pago = ?", (pago_id,))
        conexion.commit()
        conexion.close()

    def obtener_pago(self, pago_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        # Corregido: se usa id_pago y se hace JOIN para que la interfaz reciba las claves correctas
        cursor.execute("""
            SELECT p.id_pago AS id, 
                   c.nombre AS Cliente, 
                   p.fecha AS Fecha, 
                   p.monto AS Monto, 
                   p.metodo_pago AS 'Medio de pago'
            FROM pagos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE p.id_pago = ?
        """, (pago_id,))
        fila = cursor.fetchone()
        conexion.close()
        return dict(fila) if fila else None