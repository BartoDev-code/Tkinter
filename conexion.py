import mysql.connector
import os


def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="45241587",
        database="contabilidad_facil"
    )


def crear_indices_si_no_existen(conexion):
    """Crea los índices necesarios solamente si todavía no existen."""

    indices = [
        ("facturas", "idx_facturas_cliente", "id_cliente"),
        ("pagos", "idx_pagos_cliente", "id_cliente"),
        ("pagos", "idx_pagos_factura", "id_factura"),
        ("movimientos", "idx_movimientos_cliente", "id_cliente"),
    ]

    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT DATABASE()")
        base_datos = cursor.fetchone()[0]

        for tabla, indice, columna in indices:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM information_schema.statistics
                WHERE table_schema = %s
                  AND table_name = %s
                  AND index_name = %s
                """,
                (base_datos, tabla, indice)
            )

            existe = cursor.fetchone()[0] > 0

            if not existe:
                consulta = (
                    f"CREATE INDEX {indice} "
                    f"ON {tabla} ({columna})"
                )

                cursor.execute(consulta)
                print(f"Índice creado: {indice}")

            else:
                print(f"El índice ya existe: {indice}")

        conexion.commit()

    finally:
        cursor.close()


def inicializar_base_de_datos():
    """Inicializa las tablas y comprueba los índices."""

    archivo_sql = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "esquema_normalizado.sql"
    )

    if not os.path.exists(archivo_sql):
        print(
            f"Advertencia: No se encontró el archivo "
            f"'{archivo_sql}'."
        )
        return

    conexion = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        with open(archivo_sql, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

       
        for sentencia in contenido.split(";"):
            lineas = [
                linea
                for linea in sentencia.splitlines()
                if not linea.strip().startswith("--")
                and linea.strip()
            ]

            sentencia_limpia = " ".join(lineas).strip()

            if sentencia_limpia:
                cursor.execute(sentencia_limpia)

                
                if cursor.with_rows:
                    cursor.fetchall()

        cursor.close()
        conexion.commit()

        
        crear_indices_si_no_existen(conexion)

        print(
            "Base de datos inicializada correctamente "
            "en MySQL."
        )

    except mysql.connector.Error as error:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()

        print(
            "Error al inicializar la base de datos "
            f"desde el script SQL: {error}"
        )

    except OSError as error:
        print(f"Error al leer el archivo SQL: {error}")

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()
