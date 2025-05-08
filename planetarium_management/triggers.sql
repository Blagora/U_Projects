-- Eliminar triggers existentes
DROP TRIGGER IF EXISTS trg_consistencia_periodos;
DROP TRIGGER IF EXISTS trg_registrar_cambios;
GO

-- Crear nuevo trigger para consistencia de periodos
CREATE TRIGGER trg_consistencia_periodos
ON SATELITE
AFTER INSERT, UPDATE
AS
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM inserted i
        JOIN PLANETA p ON i.id_planeta = p.id_planeta
        WHERE i.periodo_orb > p.periodo_orbital
    )
    BEGIN
        RAISERROR('El periodo orbital de un satélite no puede ser mayor al periodo orbital de su planeta', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO

-- Crear nuevo trigger para auditoría
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
GO

-- Crear trigger para auditoría de satélites
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
        (SELECT i.id_satelite, i.excentricidad, i.periodo_orb, i.inclinacion_orb, i.id_planeta 
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
        (SELECT d.id_satelite, d.excentricidad, d.periodo_orb, d.inclinacion_orb, d.id_planeta 
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
        (SELECT d.id_satelite, d.excentricidad, d.periodo_orb, d.inclinacion_orb, d.id_planeta 
         FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
        (SELECT i.id_satelite, i.excentricidad, i.periodo_orb, i.inclinacion_orb, i.id_planeta 
         FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
        SYSTEM_USER
    FROM inserted i
    JOIN deleted d ON i.id_satelite = d.id_satelite
    WHERE i.excentricidad != d.excentricidad OR
          i.periodo_orb != d.periodo_orb OR
          i.inclinacion_orb != d.inclinacion_orb OR
          i.id_planeta != d.id_planeta;
END;
GO
