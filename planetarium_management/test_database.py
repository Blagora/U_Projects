import pyodbc
import json

# Configuración de la conexión
server = 'DESKTOP-3V3HASL\\SQLEXPRESS'
database = 'SistemaPlanetario'
username = ''
password = ''

# Conectar a la base de datos
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION=yes'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

try:
    print("=== PRUEBA DE OPERACIONES CRUD ===")
    
    # Limpiar la base de datos
    print("\nLimpiando la base de datos...")
    cursor.execute("""
        DELETE FROM AUDITORIA;
        DELETE FROM SATELITE;
        DELETE FROM PLANETA;
    """)
    conn.commit()
    print("Base de datos limpia")
    
    # 1. Insertar un planeta
    print("\n1. Insertando planeta de prueba...")
    cursor.execute("""
        INSERT INTO PLANETA (id_planeta, nombre, distancia_a_sol, inclinacion_orb, periodo_orbital, velocidad_orb)
        VALUES (1, 'Prueba', 1.0, 0.5, 365.25, 30.0)
    """)
    conn.commit()
    print("Planeta insertado exitosamente")

    # 2. Verificar el trigger de inserción
    print("\n2. Verificando trigger de inserción...")
    cursor.execute("""
        SELECT TOP 1 * FROM AUDITORIA
        WHERE entidad = 'PLANETA' AND accion = 'INSERT'
        ORDER BY id DESC
    """)
    result = cursor.fetchone()
    if result:
        print("Trigger de inserción funcionando correctamente")
        print(f"ID: {result[0]}")
        print(f"ID Entidad: {result[1]}")
        print(f"Entidad: {result[2]}")
        print(f"Acción: {result[3]}")
        print(f"Datos anteriores: {result[4]}")
        print(f"Datos nuevos: {result[5]}")
        print(f"Fecha: {result[6]}")
        print(f"Usuario: {result[7]}")
    else:
        print("ERROR: El trigger de inserción no funcionó")

    # 3. Actualizar el planeta
    print("\n3. Actualizando planeta...")
    cursor.execute("""
        UPDATE PLANETA
        SET distancia_a_sol = 1.5, inclinacion_orb = 0.7
        WHERE id_planeta = 1
    """)
    conn.commit()
    print("Planeta actualizado exitosamente")

    # 4. Verificar el trigger de actualización
    print("\n4. Verificando trigger de actualización...")
    cursor.execute("""
        SELECT TOP 1 * FROM AUDITORIA
        WHERE entidad = 'PLANETA' AND accion = 'UPDATE'
        ORDER BY id DESC
    """)
    result = cursor.fetchone()
    if result:
        print("Trigger de actualización funcionando correctamente")
        print(f"ID: {result[0]}")
        print(f"ID Entidad: {result[1]}")
        print(f"Entidad: {result[2]}")
        print(f"Acción: {result[3]}")
        print(f"Datos anteriores: {result[4]}")
        print(f"Datos nuevos: {result[5]}")
        print(f"Fecha: {result[6]}")
        print(f"Usuario: {result[7]}")
    else:
        print("ERROR: El trigger de actualización no funcionó")

    # 5. Insertar un satélite
    print("\n5. Insertando satélite...")
    cursor.execute("""
        INSERT INTO SATELITE (id_satelite, nombre, excentricidad, periodo_orb, inclinacion_orb, id_planeta)
        VALUES (1, 'Satélite Prueba', 0.1, 27.32, 0.05, 1)
    """)
    conn.commit()
    print("Satélite insertado exitosamente")

    # 6. Verificar el trigger de inserción de satélite
    print("\n6. Verificando trigger de inserción de satélite...")
    cursor.execute("""
        SELECT TOP 1 * FROM AUDITORIA
        WHERE entidad = 'SATELITE' AND accion = 'INSERT'
        ORDER BY id DESC
    """)
    result = cursor.fetchone()
    if result:
        print("Trigger de inserción de satélite funcionando correctamente")
        print(f"ID: {result[0]}")
        print(f"ID Entidad: {result[1]}")
        print(f"Entidad: {result[2]}")
        print(f"Acción: {result[3]}")
        print(f"Datos anteriores: {result[4]}")
        print(f"Datos nuevos: {result[5]}")
        print(f"Fecha: {result[6]}")
        print(f"Usuario: {result[7]}")
    else:
        print("ERROR: El trigger de inserción de satélite no funcionó")

    # 7. Eliminar el planeta (esto debería eliminar el satélite por cascada)
    print("\n7. Eliminando planeta...")
    cursor.execute("""
        DELETE FROM PLANETA WHERE id_planeta = 1
    """)
    conn.commit()
    print("Planeta eliminado exitosamente")

    # 8. Verificar el trigger de eliminación
    print("\n8. Verificando trigger de eliminación...")
    cursor.execute("""
        SELECT TOP 1 * FROM AUDITORIA
        WHERE entidad = 'PLANETA' AND accion = 'DELETE'
        ORDER BY id DESC
    """)
    result = cursor.fetchone()
    if result:
        print("Trigger de eliminación funcionando correctamente")
        print(f"ID: {result[0]}")
        print(f"ID Entidad: {result[1]}")
        print(f"Entidad: {result[2]}")
        print(f"Acción: {result[3]}")
        print(f"Datos anteriores: {result[4]}")
        print(f"Datos nuevos: {result[5]}")
        print(f"Fecha: {result[6]}")
        print(f"Usuario: {result[7]}")
    else:
        print("ERROR: El trigger de eliminación no funcionó")

    # 9. Verificar que el satélite fue eliminado por cascada
    print("\n9. Verificando eliminación en cascada del satélite...")
    cursor.execute("SELECT COUNT(*) FROM SATELITE WHERE id_satelite = 1")
    result = cursor.fetchone()
    if result[0] == 0:
        print("Satélite eliminado correctamente por cascada")
    else:
        print("ERROR: El satélite no fue eliminado por cascada")

except Exception as e:
    print(f"\nERROR: {str(e)}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
