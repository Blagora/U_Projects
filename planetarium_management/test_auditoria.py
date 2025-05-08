from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-3V3HASL\\SQLEXPRESS/SistemaPlanetario?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Crear el contexto de la aplicación
app.app_context().push()

# Definir el modelo Planeta
class Planeta(db.Model):
    __tablename__ = 'PLANETA'
    id_planeta = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    distancia_a_sol = db.Column(db.Float, nullable=False)
    inclinacion_orb = db.Column(db.Float, nullable=False)
    periodo_orbital = db.Column(db.Float, nullable=False)
    velocidad_orb = db.Column(db.Float, nullable=False)

# Definir el modelo Auditoria
class Auditoria(db.Model):
    __tablename__ = 'AUDITORIA'
    id = db.Column(db.Integer, primary_key=True)
    id_entidad = db.Column(db.Integer, nullable=False)
    entidad = db.Column(db.String(50), nullable=False)
    accion = db.Column(db.String(10), nullable=False)
    datos_anteriores = db.Column(db.Text)
    datos_nuevos = db.Column(db.Text)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_modificacion = db.Column(db.String(50))

    @staticmethod
    def log_accion(id_entidad, entidad, accion, datos_anteriores=None, datos_nuevos=None):
        """
        Registra una acción en la tabla de auditoría
        """
        auditoria = Auditoria(
            id_entidad=id_entidad,
            entidad=entidad,
            accion=accion,
            datos_anteriores=json.dumps(datos_anteriores) if datos_anteriores else None,
            datos_nuevos=json.dumps(datos_nuevos) if datos_nuevos else None,
            usuario_modificacion='usuario'
        )
        db.session.add(auditoria)
        db.session.commit()

# Inicializar la base de datos
try:
    db.create_all()
    print("Base de datos inicializada correctamente")
except Exception as e:
    print(f"Error al inicializar la base de datos: {str(e)}")

# Limpiar la base de datos
print("\nLimpiando la base de datos...")
Planeta.query.delete()
Auditoria.query.delete()
db.session.commit()
print("Base de datos limpia")

# 1. Insertar un planeta
print("\n1. Insertando planeta de prueba...")
planeta = Planeta(
    id_planeta=1,
    nombre="Prueba",
    distancia_a_sol=1.0,
    inclinacion_orb=0.5,
    periodo_orbital=365.25,
    velocidad_orb=30.0
)
try:
    db.session.add(planeta)
    db.session.commit()
    print("Planeta insertado exitosamente")
except Exception as e:
    print(f"ERROR al insertar planeta: {str(e)}")
    db.session.rollback()

# 2. Verificar el registro de auditoría para la inserción
print("\n2. Verificando registro de auditoría para inserción...")
try:
    # Desactivar triggers temporariamente
    db.session.execute("ALTER TABLE AUDITORIA DISABLE TRIGGER ALL")
    auditoria = Auditoria.query.filter_by(accion='INSERT', entidad='PLANETA', id_entidad=1).first()
    if auditoria:
        print("Registro de auditoría encontrado")
        print(f"ID: {auditoria.id}")
        print(f"ID Entidad: {auditoria.id_entidad}")
        print(f"Entidad: {auditoria.entidad}")
        print(f"Acción: {auditoria.accion}")
        print(f"Datos anteriores: {auditoria.datos_anteriores}")
        print(f"Datos nuevos: {auditoria.datos_nuevos}")
        print(f"Fecha: {auditoria.fecha_modificacion}")
        print(f"Usuario: {auditoria.usuario_modificacion}")
    else:
        print("ERROR: No se encontró registro de auditoría para la inserción")
except Exception as e:
    print(f"ERROR al verificar auditoría: {str(e)}")
finally:
    # Reactivar triggers
    db.session.execute("ALTER TABLE AUDITORIA ENABLE TRIGGER ALL")

# 3. Actualizar el planeta
print("\n3. Actualizando planeta...")
try:
    planeta = Planeta.query.filter_by(id_planeta=1).first()
    if planeta:
        datos_anteriores = {
            'nombre': planeta.nombre,
            'distancia_a_sol': planeta.distancia_a_sol,
            'inclinacion_orb': planeta.inclinacion_orb,
            'periodo_orbital': planeta.periodo_orbital,
            'velocidad_orb': planeta.velocidad_orb
        }
        
        datos_nuevos = {
            'nombre': planeta.nombre,
            'distancia_a_sol': 1.5,
            'inclinacion_orb': 0.7,
            'periodo_orbital': planeta.periodo_orbital,
            'velocidad_orb': planeta.velocidad_orb
        }

        # Actualizar el planeta
        planeta.distancia_a_sol = 1.5
        planeta.inclinacion_orb = 0.7

        # Registrar en la auditoría
        Auditoria.log_accion(
            id_entidad=1,
            entidad='PLANETA',
            accion='UPDATE',
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos
        )

        db.session.commit()
        print("Planeta actualizado exitosamente")
    else:
        print("ERROR: No se encontró el planeta")
except Exception as e:
    print(f"ERROR al actualizar planeta: {str(e)}")
    db.session.rollback()

# 4. Verificar el registro de auditoría para la actualización
print("\n4. Verificando registro de auditoría para actualización...")
registro = Auditoria.query.filter_by(entidad='PLANETA', accion='UPDATE').first()
if registro:
    print("Registro de auditoría encontrado")
    print(f"ID: {registro.id}")
    print(f"ID Entidad: {registro.id_entidad}")
    print(f"Entidad: {registro.entidad}")
    print(f"Acción: {registro.accion}")
    print(f"Datos anteriores: {registro.datos_anteriores}")
    print(f"Datos nuevos: {registro.datos_nuevos}")
    print(f"Fecha: {registro.fecha_modificacion}")
    print(f"Usuario: {registro.usuario_modificacion}")
else:
    print("ERROR: No se encontró registro de auditoría para la actualización")

# 7. Eliminar el planeta (esto debería eliminar el satélite por cascada)
print("\n7. Eliminando planeta...")
try:
    db.session.delete(planeta)
    db.session.commit()
    print("Planeta eliminado exitosamente")
except Exception as e:
    print(f"ERROR al eliminar planeta: {str(e)}")
    db.session.rollback()

# 8. Verificar el registro de auditoría para la eliminación
print("\n8. Verificando registro de auditoría para eliminación...")
registro = Auditoria.query.filter_by(entidad='PLANETA', accion='DELETE').first()
if registro:
    print("Registro de auditoría encontrado")
    print(f"ID: {registro.id}")
    print(f"ID Entidad: {registro.id_entidad}")
    print(f"Entidad: {registro.entidad}")
    print(f"Acción: {registro.accion}")
    print(f"Datos anteriores: {registro.datos_anteriores}")
    print(f"Datos nuevos: {registro.datos_nuevos}")
    print(f"Fecha: {registro.fecha_modificacion}")
    print(f"Usuario: {registro.usuario_modificacion}")
else:
    print("ERROR: No se encontró registro de auditoría para la eliminación")
