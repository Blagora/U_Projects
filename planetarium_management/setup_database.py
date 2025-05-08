import pyodbc
import os

# Configuración de la conexión
server = 'DESKTOP-3V3HASL\\SQLEXPRESS'
database = 'SistemaPlanetario'
username = ''
password = ''

# Crear la base de datos si no existe
conn_str = f'DRIVER={{SQL Server}};SERVER={server};TRUSTED_CONNECTION=yes'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Crear la base de datos si no existe
cursor.execute(f"""
    IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{database}')
    BEGIN
        CREATE DATABASE {database}
    END
""")

# Conectarse a la base de datos
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION=yes'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Crear tablas
try:
    cursor.execute(f"""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'PLANETA')
        BEGIN
            CREATE TABLE PLANETA (
                id_planeta INT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                distancia_a_sol FLOAT NOT NULL,
                inclinacion_orb FLOAT NOT NULL,
                periodo_orbital FLOAT NOT NULL,
                velocidad_orb FLOAT NOT NULL
            )
        END
    """)

    cursor.execute(f"""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SATELITE')
        BEGIN
            CREATE TABLE SATELITE (
                id_satelite INT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                excentricidad FLOAT NOT NULL,
                periodo_orb FLOAT NOT NULL,
                inclinacion_orb FLOAT NOT NULL,
                id_planeta INT NOT NULL,
                FOREIGN KEY (id_planeta) REFERENCES PLANETA(id_planeta)
            )
        END
    """)

    cursor.execute(f"""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AUDITORIA')
        BEGIN
            CREATE TABLE AUDITORIA (
                id INT IDENTITY(1,1) PRIMARY KEY,
                id_entidad INT NOT NULL,
                entidad VARCHAR(50) NOT NULL,
                accion VARCHAR(10) NOT NULL,
                datos_anteriores TEXT,
                datos_nuevos TEXT,
                fecha_modificacion DATETIME DEFAULT GETDATE(),
                usuario_modificacion VARCHAR(100)
            )
        END
    """)

    # Eliminar todos los triggers existentes
    cursor.execute("""
        DECLARE @sql NVARCHAR(MAX) = N'';
        SELECT @sql += N'
        IF EXISTS (SELECT * FROM sys.triggers WHERE name = ''' + name + ''')
            DROP TRIGGER ' + name + ';'
        FROM sys.triggers;
        EXEC sp_executesql @sql;
    """)

    # Crear triggers
    triggers = [
        """
        IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_registrar_cambios')
            DROP TRIGGER trg_registrar_cambios;
        """,
        """
        CREATE TRIGGER trg_registrar_cambios
        ON PLANETA
        AFTER INSERT, UPDATE, DELETE
        AS
        BEGIN
            -- Insertar registros para INSERT
            INSERT INTO AUDITORIA (id_entidad, entidad, accion, datos_nuevos, usuario_modificacion)
            SELECT 
                i.id_planeta,
                'PLANETA',
                'INSERT',
                (SELECT i.id_planeta, i.nombre, i.distancia_a_sol, i.inclinacion_orb, i.periodo_orbital, i.velocidad_orb 
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
                SYSTEM_USER
            FROM inserted i
            WHERE NOT EXISTS (SELECT 1 FROM deleted d WHERE d.id_planeta = i.id_planeta);

            -- Insertar registros para DELETE
            INSERT INTO AUDITORIA (id_entidad, entidad, accion, datos_anteriores, usuario_modificacion)
            SELECT 
                d.id_planeta,
                'PLANETA',
                'DELETE',
                (SELECT d.id_planeta, d.nombre, d.distancia_a_sol, d.inclinacion_orb, d.periodo_orbital, d.velocidad_orb 
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
                SYSTEM_USER
            FROM deleted d
            WHERE NOT EXISTS (SELECT 1 FROM inserted i WHERE i.id_planeta = d.id_planeta);

            -- Insertar registros para UPDATE
            INSERT INTO AUDITORIA (id_entidad, entidad, accion, datos_anteriores, datos_nuevos, usuario_modificacion)
            SELECT 
                i.id_planeta,
                'PLANETA',
                'UPDATE',
                (SELECT d.id_planeta, d.nombre, d.distancia_a_sol, d.inclinacion_orb, d.periodo_orbital, d.velocidad_orb 
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
                (SELECT i.id_planeta, i.nombre, i.distancia_a_sol, i.inclinacion_orb, i.periodo_orbital, i.velocidad_orb 
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
                SYSTEM_USER
            FROM inserted i
            JOIN deleted d ON i.id_planeta = d.id_planeta
            WHERE i.nombre != d.nombre OR
                  i.distancia_a_sol != d.distancia_a_sol OR
                  i.inclinacion_orb != d.inclinacion_orb OR
                  i.periodo_orbital != d.periodo_orbital OR
                  i.velocidad_orb != d.velocidad_orb;
        END;
        """,
        """
        IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_registrar_cambios_satelite')
            DROP TRIGGER trg_registrar_cambios_satelite;
        """,
        """
        CREATE TRIGGER trg_registrar_cambios_satelite
        ON SATELITE
        AFTER INSERT, UPDATE, DELETE
        AS
        BEGIN
            -- Insertar registros para INSERT
            INSERT INTO AUDITORIA (id_entidad, entidad, accion, datos_nuevos, usuario_modificacion)
            SELECT 
                i.id_satelite,
                'SATELITE',
                'INSERT',
                (SELECT i.id_satelite, i.nombre, i.excentricidad, i.periodo_orb, i.inclinacion_orb, i.id_planeta 
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
                SYSTEM_USER
            FROM inserted i
            WHERE NOT EXISTS (SELECT 1 FROM deleted d WHERE d.id_satelite = i.id_satelite);

            -- Insertar registros para DELETE
            INSERT INTO AUDITORIA (id_entidad, entidad, accion, datos_anteriores, usuario_modificacion)
            SELECT 
                d.id_satelite,
                'SATELITE',
                'DELETE',
                (SELECT d.id_satelite, d.nombre, d.excentricidad, d.periodo_orb, d.inclinacion_orb, d.id_planeta 
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
                SYSTEM_USER
            FROM deleted d
            WHERE NOT EXISTS (SELECT 1 FROM inserted i WHERE i.id_satelite = d.id_satelite);

            -- Insertar registros para UPDATE
            INSERT INTO AUDITORIA (id_entidad, entidad, accion, datos_anteriores, datos_nuevos, usuario_modificacion)
            SELECT 
                i.id_satelite,
                'SATELITE',
                'UPDATE',
                (SELECT d.id_satelite, d.nombre, d.excentricidad, d.periodo_orb, d.inclinacion_orb, d.id_planeta 
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
                (SELECT i.id_satelite, i.nombre, i.excentricidad, i.periodo_orb, i.inclinacion_orb, i.id_planeta 
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
                SYSTEM_USER
            FROM inserted i
            JOIN deleted d ON i.id_satelite = d.id_satelite
            WHERE i.excentricidad != d.excentricidad OR
                  i.periodo_orb != d.periodo_orb OR
                  i.inclinacion_orb != d.inclinacion_orb OR
                  i.id_planeta != d.id_planeta;
        END;
        """,
        """
        CREATE TRIGGER TRIGGER_SATELITE_DELETE
        ON SATELITE
        AFTER DELETE
        AS
        BEGIN
            INSERT INTO AUDITORIA
            (id_entidad, entidad, accion, datos_anteriores, usuario_modificacion)
            SELECT 
                d.id_satelite,
                'SATELITE',
                'DELETE',
                (SELECT * FROM deleted FOR JSON AUTO),
                SYSTEM_USER
            FROM deleted d;
        END;
        """
    ]

    # Ejecutar cada trigger en un lote separado
    for trigger_sql in triggers:
        cursor.execute(trigger_sql)
        conn.commit()

    # Confirmar cambios
    conn.commit()
    print("Base de datos, tablas y triggers creados exitosamente")

except Exception as e:
    print(f"Error: {str(e)}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
