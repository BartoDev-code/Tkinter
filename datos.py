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
        cursor.execute("SELECT * FROM facturas")
        filas = [dict(fila) for fila in cursor.fetchall()]
        conexion.close()
        return filas

    def agregar_factura(self, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO facturas (Cliente, Fecha, Importe, Estado)
            VALUES (?, ?, ?, ?)
        """, (datos["Cliente"], datos["Fecha"], datos["Importe"], datos["Estado"]))
        conexion.commit()
        nuevo_id = cursor.lastrowid
        conexion.close()
        return nuevo_id

    def actualizar_factura(self, factura_id, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE facturas 
            SET Cliente=?, Fecha=?, Importe=?, Estado=?
            WHERE id=?
        """, (datos["Cliente"], datos["Fecha"], datos["Importe"], datos["Estado"], factura_id))
        conexion.commit()
        conexion.close()

    def eliminar_factura(self, factura_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM facturas WHERE id_cliente=?", (factura_id,))
        conexion.commit()
        conexion.close()

    def obtener_factura(self, factura_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM facturas WHERE id_cliente=?", (factura_id,))
        fila = cursor.fetchone()
        conexion.close()
        return dict(fila) if fila else None

    # ==================== PAGOS ====================
    def obtener_pagos(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM pagos")
        filas = [dict(fila) for fila in cursor.fetchall()]
        conexion.close()
        return filas

    def agregar_pago(self, datos):
    # 'datos' viene del formulario con: 
    # {"Cliente": "Juan Perez", "Fecha": "30/09/2026", "Monto": "1500", "Estado": "Confirmado", "Medio de pago": "Efectivo"}
    
      conexion = obtener_conexion()
      cursor = conexion.cursor()

      try:
        # 1. Buscar el id_cliente a partir del nombre que viene del formulario
        cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = ?", (datos["Cliente"],))
        resultado_cliente = cursor.fetchone()
        if not resultado_cliente:
            raise Exception(f"El cliente '{datos['Cliente']}' no existe en la base de datos.")
        id_cliente = resultado_cliente[0]

        # 2. Buscar una factura válida para este cliente (requerido por el NOT NULL de la BD)
        cursor.execute("SELECT id_factura FROM facturas WHERE id_cliente = ? LIMIT 1", (id_cliente,))
        resultado_factura = cursor.fetchone()
        if not resultado_factura:
            raise Exception("El cliente seleccionado no tiene facturas registradas para asociar al pago.")
        id_factura = resultado_factura[0]

        # 3. Adaptar los valores restantes
        fecha = datos["Fecha"]
        monto = float(datos["Monto"].replace(",", "."))
        
        # Convertir a mayúsculas para que coincida con el CHECK ('EFECTIVO', 'TRANSFERENCIA', etc.)
        metodo_pago = datos["Medio de pago"].strip().upper() 

        # 4. Ejecutar el INSERT utilizando exclusivamente las columnas reales de la base de datos
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
        cursor.execute("""
            UPDATE pagos 
            SET Cliente=?, Fecha=?, Monto=?, Estado=?, Medio_de_pago=?
            WHERE id=?
        """, (datos["Cliente"], datos["Fecha"], datos["Monto"], datos["Estado"], datos["Medio de pago"], pago_id))
        conexion.commit()
        conexion.close()

    def eliminar_pago(self, pago_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM pagos WHERE id=?", (pago_id,))
        conexion.commit()
        conexion.close()

    def obtener_pago(self, pago_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM pagos WHERE id=?", (pago_id,))
        fila = cursor.fetchone()
        conexion.close()
        return dict(fila) if fila else None