import sqlite3
import os

def obtener_conexion():
    """Establece y devuelve una conexión a la base de datos SQLite."""
    conexion = sqlite3.connect("contabilidad.db")
    conexion.row_factory = sqlite3.Row 
    return conexion

def inicializar_base_de_datos():
    """Lee el archivo 'esquema_normalizado.sql' y crea las tablas si no existen."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    archivo_sql = "esquema_normalizado.sql"

    if os.path.exists(archivo_sql):
        try:
            with open(archivo_sql, "r", encoding="utf-8") as f:
                script_sql = f.read()
            
          
            cursor.executescript(script_sql)
            conexion.commit()
            print("Base de datos inicializada correctamente desde el esquema SQL.")
        except Exception as e:
            print(f"Error al inicializar la base de datos desde el script SQL: {e}")
    else:
        print(f"Advertencia: No se encontró el archivo '{archivo_sql}' en la carpeta.")

    conexion.close()