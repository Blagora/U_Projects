from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-3V3HASL\\SQLEXPRESS/SistemaPlanetario?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de la base de datos
db = SQLAlchemy(app)

# Inicializar la base de datos
with app.app_context():
    try:
        db.create_all()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")

class Planeta(db.Model):
    __tablename__ = 'PLANETA'
    id_planeta = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    distancia_a_sol = db.Column(db.Float, nullable=False)
    inclinacion_orb = db.Column(db.Float, nullable=False)
    periodo_orbital = db.Column(db.Float, nullable=False)
    velocidad_orb = db.Column(db.Float, nullable=False)

    @staticmethod
    def validate_name(nombre, id_planeta=None):
        """
        Valida que el nombre del planeta sea único, excluyendo el propio planeta si se está editando
        """
        query = Planeta.query.filter_by(nombre=nombre)
        if id_planeta:
            query = query.filter(Planeta.id_planeta != id_planeta)
        return not query.first()

    @staticmethod
    def validate_distance(distancia):
        return 0.3 <= distancia <= 31.0

    @staticmethod
    def validate_inclinacion_orb(inclinacion_orb):
        return 0 <= inclinacion_orb <= 180

    @staticmethod
    def validate_periodo_orbital(periodo_orbital):
        return periodo_orbital > 0

    @staticmethod
    def validate_velocidad_orb(velocidad_orb):
        return velocidad_orb > 0

class Auditoria(db.Model):
    __tablename__ = 'AUDITORIA'
    id = db.Column(db.Integer, primary_key=True)
    id_entidad = db.Column(db.Integer, nullable=False)
    entidad = db.Column(db.String(50), nullable=False)
    accion = db.Column(db.String(10), nullable=False)
    datos_anteriores = db.Column(db.Text)
    datos_nuevos = db.Column(db.Text)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_modificacion = db.Column(db.String(100))

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

class Satelite(db.Model):
    __tablename__ = 'SATELITE'
    id_satelite = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(100), nullable=False)
    excentricidad = db.Column(db.Float, nullable=False)
    periodo_orb = db.Column(db.Float, nullable=False)
    inclinacion_orb = db.Column(db.Float, nullable=False)
    id_planeta = db.Column(db.Integer, db.ForeignKey('PLANETA.id_planeta'), nullable=False)

    def get_next_id():
        max_id = db.session.query(db.func.max(Satelite.id_satelite)).scalar()
        return (max_id or 0) + 1

    def update(self, nombre, excentricidad, periodo_orb, inclinacion_orb):
        """
        Actualiza los datos del satélite con validaciones
        """
        # Validaciones
        if not nombre:
            raise ValueError('El nombre es requerido')
        
        if not self.validate_nombre(nombre, self.id_planeta, self.id_satelite):
            raise ValueError('Ya existe un satélite con ese nombre para este planeta')
            
        if not self.validate_excentricidad(excentricidad):
            raise ValueError('La excentricidad debe estar entre 0 y 1')
            
        if not self.validate_periodo_orb(periodo_orb):
            raise ValueError('El periodo orbital debe ser mayor a 0')
            
        if not self.validate_inclinacion_orb(inclinacion_orb):
            raise ValueError('La inclinación orbital debe estar entre 0 y 180°')
            
        # Actualizar los valores
        self.nombre = nombre
        self.excentricidad = excentricidad
        self.periodo_orb = periodo_orb
        self.inclinacion_orb = inclinacion_orb

    @staticmethod
    def validate_excentricidad(excentricidad):
        return 0 <= excentricidad <= 1

    @staticmethod
    def validate_periodo_orb(periodo_orb):
        return periodo_orb > 0

    @staticmethod
    def validate_inclinacion_orb(inclinacion_orb):
        return 0 <= inclinacion_orb <= 180

    @staticmethod
    def validate_nombre(nombre, id_planeta, id_satelite=None):
        """
        Valida que el nombre del satélite sea único por planeta, excluyendo el propio satélite si se está editando
        """
        query = Satelite.query.filter_by(nombre=nombre, id_planeta=id_planeta)
        if id_satelite:
            query = query.filter(Satelite.id_satelite != id_satelite)
        return not query.first()

# Formularios
class PlanetaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(max=100, message='El nombre debe tener máximo 100 caracteres')
    ])
    distancia_a_sol = FloatField('Distancia al Sol (UA)', validators=[
        DataRequired(message='La distancia al Sol es requerida'),
        NumberRange(min=0.3, max=31.0, message='La distancia debe estar entre 0.3 y 31.0 UA')
    ])
    inclinacion_orb = FloatField('Inclinación Orbital (°)', validators=[
        DataRequired(message='La inclinación orbital es requerida'),
        NumberRange(min=0, max=180, message='La inclinación debe estar entre 0 y 180°')
    ])
    periodo_orbital = FloatField('Periodo Orbital (días)', validators=[
        DataRequired(message='El periodo orbital es requerido'),
        NumberRange(min=0, message='El periodo orbital debe ser mayor a 0')
    ])
    velocidad_orb = FloatField('Velocidad Orbital (km/s)', validators=[
        DataRequired(message='La velocidad orbital es requerida'),
        NumberRange(min=0, message='La velocidad orbital debe ser mayor a 0')
    ])
    submit = SubmitField('Guardar')

class SateliteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(max=100, message='El nombre debe tener máximo 100 caracteres')
    ])
    excentricidad = FloatField('Excentricidad', validators=[
        DataRequired(message='La excentricidad es requerida'),
        NumberRange(min=0, max=1, message='La excentricidad debe estar entre 0 y 1')
    ])
    periodo_orb = FloatField('Periodo Orbital (días)', validators=[
        DataRequired(message='El periodo orbital es requerido'),
        NumberRange(min=0, message='El periodo orbital debe ser mayor a 0')
    ])
    inclinacion_orb = FloatField('Inclinación Orbital (°)', validators=[
        DataRequired(message='La inclinación orbital es requerida'),
        NumberRange(min=0, max=180, message='La inclinación debe estar entre 0 y 180°')
    ])
    submit = SubmitField('Guardar')

class ConsultaDistanciaForm(FlaskForm):
    distancia = FloatField('Distancia al Sol (UA)', validators=[
        DataRequired(),
        NumberRange(min=0.3, max=31.0, message='La distancia debe estar entre 0.3 y 31.0 UA')
    ])
    orden = SelectField('Orden', choices=[('asc', 'Ascendente'), ('desc', 'Descendente')], default='asc')
    submit = SubmitField('Consultar')

class ConsultaInclinacionForm(FlaskForm):
    id_planeta = SelectField('Planeta', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Consultar')

class FiltroAuditoriaForm(FlaskForm):
    entidad = SelectField('Entidad', choices=[('TODAS', 'Todas las entidades'), ('PLANETA', 'Planeta'), ('SATELITE', 'Satélite')], validators=[DataRequired(message='Por favor seleccione una entidad')])
    accion = SelectField('Acción', choices=[('TODAS', 'Todas las acciones'), ('INSERT', 'Insertar'), ('UPDATE', 'Actualizar'), ('DELETE', 'Eliminar')], validators=[DataRequired(message='Por favor seleccione una acción')])
    fecha_inicio = StringField('Fecha inicio (YYYY-MM-DD)', validators=[DataRequired(message='Por favor ingrese una fecha de inicio')])
    fecha_fin = StringField('Fecha fin (YYYY-MM-DD)', validators=[DataRequired(message='Por favor ingrese una fecha de fin')])
    submit = SubmitField('Filtrar')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auditoria', methods=['GET', 'POST'])
def auditoria():
    form = FiltroAuditoriaForm()
    query = Auditoria.query
    
    if form.validate_on_submit():
        if form.entidad.data != 'TODAS':
            query = query.filter(Auditoria.entidad == form.entidad.data)
        if form.accion.data != 'TODAS':
            query = query.filter(Auditoria.accion == form.accion.data)
        if form.fecha_inicio.data:
            try:
                fecha_inicio = datetime.strptime(form.fecha_inicio.data, '%Y-%m-%d')
                query = query.filter(Auditoria.fecha_modificacion >= fecha_inicio)
            except ValueError:
                flash('Formato de fecha incorrecto', 'error')
        if form.fecha_fin.data:
            try:
                fecha_fin = datetime.strptime(form.fecha_fin.data, '%Y-%m-%d')
                query = query.filter(Auditoria.fecha_modificacion <= fecha_fin)
            except ValueError:
                flash('Formato de fecha incorrecto', 'error')
    
    registros = query.order_by(Auditoria.fecha_modificacion.desc()).all()
    return render_template('auditoria.html', auditoria=registros, form=form)

@app.route('/planeta/nuevo', methods=['GET', 'POST'])
def nuevo_planeta():
    form = PlanetaForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Obtener datos del formulario
                nombre = form.nombre.data
                distancia_a_sol = form.distancia_a_sol.data
                inclinacion_orb = form.inclinacion_orb.data
                periodo_orbital = form.periodo_orbital.data
                velocidad_orb = form.velocidad_orb.data

                # Validaciones
                if not nombre:
                    flash('El nombre es requerido', 'error')
                    return render_template('nuevo_planeta.html', form=form)
                
                if not Planeta.validate_name(nombre):
                    flash('Ya existe un planeta con ese nombre', 'error')
                    return render_template('nuevo_planeta.html', form=form)
                
                if not Planeta.validate_distance(distancia_a_sol):
                    flash('La distancia al Sol debe estar entre 0.3 y 31.0 UA', 'error')
                    return render_template('nuevo_planeta.html', form=form)
                
                if not Planeta.validate_inclinacion_orb(inclinacion_orb):
                    flash('La inclinación orbital debe estar entre 0 y 180°', 'error')
                    return render_template('nuevo_planeta.html', form=form)
                
                if not Planeta.validate_periodo_orbital(periodo_orbital):
                    flash('El periodo orbital debe ser mayor a 0', 'error')
                    return render_template('nuevo_planeta.html', form=form)
                
                if not Planeta.validate_velocidad_orb(velocidad_orb):
                    flash('La velocidad orbital debe ser mayor a 0', 'error')
                    return render_template('nuevo_planeta.html', form=form)

                # Crear el nuevo planeta
                nuevo_planeta = Planeta(
                    nombre=nombre,
                    distancia_a_sol=distancia_a_sol,
                    inclinacion_orb=inclinacion_orb,
                    periodo_orbital=periodo_orbital,
                    velocidad_orb=velocidad_orb
                )

                # Agregar el planeta a la sesión
                db.session.add(nuevo_planeta)
                
                # Commit para asegurar que el ID se genere
                db.session.commit()
                
                # Obtener el ID del planeta recién creado
                nuevo_planeta_id = nuevo_planeta.id_planeta
                
                # Registrar en la auditoría
                Auditoria.log_accion(
                    id_entidad=nuevo_planeta_id,
                    entidad='PLANETA',
                    accion='INSERT',
                    datos_nuevos={
                        'nombre': nombre,
                        'distancia_a_sol': distancia_a_sol,
                        'inclinacion_orb': inclinacion_orb,
                        'periodo_orbital': periodo_orbital,
                        'velocidad_orb': velocidad_orb
                    }
                )

                db.session.add(nuevo_planeta)
                db.session.commit()
                flash('Planeta agregado exitosamente', 'success')
                return redirect(url_for('index'))
                
            except Exception as e:
                db.session.rollback()
                error_msg = str(e)
                if 'periodo orbital' in error_msg.lower():
                    flash('Error: El periodo orbital de un satélite no puede ser mayor al periodo orbital de su planeta', 'error')
                else:
                    flash('Error al guardar el planeta: ' + error_msg, 'error')
                return render_template('nuevo_planeta.html', form=form)
    
    return render_template('nuevo_planeta.html', form=form)

@app.route('/planeta/<int:id_planeta>')
def ver_planeta(id_planeta):
    planeta = Planeta.query.get_or_404(id_planeta)
    satelites = Satelite.query.filter_by(id_planeta=id_planeta).all()
    return render_template('ver_planeta.html', planeta=planeta, satelites=satelites)

@app.route('/planeta/<int:id_planeta>/satelite/nuevo', methods=['GET', 'POST'])
def nuevo_satelite(id_planeta):
    form = SateliteForm()
    planeta = Planeta.query.get_or_404(id_planeta)
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Obtener datos del formulario
                nombre = form.nombre.data
                excentricidad = form.excentricidad.data
                periodo_orb = form.periodo_orb.data
                inclinacion_orb = form.inclinacion_orb.data

                # Validaciones
                if not nombre:
                    flash('El nombre es requerido', 'error')
                    return render_template('nuevo_satelite.html', form=form, id_planeta=id_planeta, planeta=planeta)
                
                if not Satelite.validate_nombre(nombre, id_planeta):
                    flash('Ya existe un satélite con ese nombre para este planeta', 'error')
                    return render_template('nuevo_satelite.html', form=form, id_planeta=id_planeta, planeta=planeta)
                
                if not Satelite.validate_excentricidad(excentricidad):
                    flash('La excentricidad debe estar entre 0 y 1', 'error')
                    return render_template('nuevo_satelite.html', form=form, id_planeta=id_planeta, planeta=planeta)
                
                if not Satelite.validate_periodo_orb(periodo_orb):
                    flash('El periodo orbital debe ser mayor a 0', 'error')
                    return render_template('nuevo_satelite.html', form=form, id_planeta=id_planeta, planeta=planeta)
                
                if not Satelite.validate_inclinacion_orb(inclinacion_orb):
                    flash('La inclinación orbital debe estar entre 0 y 180°', 'error')
                    return render_template('nuevo_satelite.html', form=form, id_planeta=id_planeta, planeta=planeta)

                # Verificar que el periodo orbital del satélite sea menor que el del planeta
                if periodo_orb >= planeta.periodo_orbital:
                    flash('El periodo orbital del satélite debe ser menor al del planeta', 'error')
                    return render_template('nuevo_satelite.html', form=form, id_planeta=id_planeta, planeta=planeta)

                # Crear el nuevo satélite
                nuevo_satelite = Satelite(
                    id_satelite=Satelite.get_next_id(),
                    nombre=nombre,
                    excentricidad=excentricidad,
                    periodo_orb=periodo_orb,
                    inclinacion_orb=inclinacion_orb,
                    id_planeta=id_planeta
                )

                # Registrar en la auditoría
                Auditoria.log_accion(
                    id_entidad=nuevo_satelite.id_satelite,
                    entidad='SATELITE',
                    accion='INSERT',
                    datos_nuevos={
                        'nombre': nombre,
                        'excentricidad': excentricidad,
                        'periodo_orb': periodo_orb,
                        'inclinacion_orb': inclinacion_orb,
                        'id_planeta': id_planeta
                    }
                )

                db.session.add(nuevo_satelite)
                db.session.commit()
                flash('Satélite agregado exitosamente', 'success')
                return redirect(url_for('ver_planeta', id_planeta=id_planeta))
                
            except Exception as e:
                db.session.rollback()
                flash('Error al guardar el satélite: ' + str(e), 'error')
                return render_template('nuevo_satelite.html', form=form, id_planeta=id_planeta, planeta=planeta)
    
    return render_template('nuevo_satelite.html', form=form, id_planeta=id_planeta, planeta=planeta)

@app.route('/satelite/eliminar/<int:id_satelite>', methods=['POST'])
def eliminar_satelite(id_satelite):
    satelite = Satelite.query.get_or_404(id_satelite)
    planeta_id = satelite.id_planeta
    
    db.session.delete(satelite)
    db.session.commit()
    flash('Satélite eliminado exitosamente', 'success')
    
    return redirect(url_for('ver_planeta', id_planeta=planeta_id))

@app.route('/satelite/editar/<int:id_satelite>', methods=['GET', 'POST'])
def editar_satelite(id_satelite):
    satelite = Satelite.query.get_or_404(id_satelite)
    planeta = Planeta.query.get_or_404(satelite.id_planeta)
    form = SateliteForm(obj=satelite)
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Obtener datos del formulario
                nombre = form.nombre.data
                excentricidad = form.excentricidad.data
                periodo_orb = form.periodo_orb.data
                inclinacion_orb = form.inclinacion_orb.data

                # Validaciones
                if not nombre:
                    flash('El nombre es requerido', 'error')
                    return render_template('editar_satelite.html', form=form, satelite=satelite)
                
                if not Satelite.validate_nombre(nombre, satelite.id_planeta, id_satelite):
                    flash('Ya existe un satélite con ese nombre para este planeta', 'error')
                    return render_template('editar_satelite.html', form=form, satelite=satelite)
                
                if not Satelite.validate_excentricidad(excentricidad):
                    flash('La excentricidad debe estar entre 0 y 1', 'error')
                    return render_template('editar_satelite.html', form=form, satelite=satelite)
                
                if not Satelite.validate_periodo_orb(periodo_orb):
                    flash('El periodo orbital debe ser mayor a 0', 'error')
                    return render_template('editar_satelite.html', form=form, satelite=satelite)
                
                if not Satelite.validate_inclinacion_orb(inclinacion_orb):
                    flash('La inclinación orbital debe estar entre 0 y 180°', 'error')
                    return render_template('editar_satelite.html', form=form, satelite=satelite)

                # Verificar que el periodo orbital del satélite sea menor que el del planeta
                if periodo_orb >= planeta.periodo_orbital:
                    flash('El periodo orbital del satélite debe ser menor al del planeta', 'error')
                    return render_template('editar_satelite.html', form=form, satelite=satelite)

                # Actualizar el satélite
                datos_anteriores = {
                    'nombre': satelite.nombre,
                    'excentricidad': satelite.excentricidad,
                    'periodo_orb': satelite.periodo_orb,
                    'inclinacion_orb': satelite.inclinacion_orb
                }
                
                datos_nuevos = {
                    'nombre': nombre,
                    'excentricidad': excentricidad,
                    'periodo_orb': periodo_orb,
                    'inclinacion_orb': inclinacion_orb
                }

                # Registrar en la auditoría
                Auditoria.log_accion(
                    id_entidad=id_satelite,
                    entidad='SATELITE',
                    accion='UPDATE',
                    datos_anteriores=datos_anteriores,
                    datos_nuevos=datos_nuevos
                )

                # Actualizar el satélite
                satelite.nombre = nombre
                satelite.excentricidad = excentricidad
                satelite.periodo_orb = periodo_orb
                satelite.inclinacion_orb = inclinacion_orb
                
                db.session.commit()
                flash('Satélite actualizado exitosamente', 'success')
                return redirect(url_for('ver_planeta', id_planeta=satelite.id_planeta))
                
            except Exception as e:
                db.session.rollback()
                error_msg = str(e)
                if 'periodo orbital' in error_msg.lower():
                    flash('Error: El periodo orbital de un satélite no puede ser mayor al periodo orbital de su planeta', 'error')
                else:
                    flash('Error al actualizar el satélite: ' + error_msg, 'error')
                return render_template('editar_satelite.html', form=form, satelite=satelite)
    
    return render_template('editar_satelite.html', form=form, satelite=satelite)

@app.route('/planeta/eliminar/<int:id_planeta>', methods=['POST'])
def eliminar_planeta(id_planeta):
    planeta = Planeta.query.get_or_404(id_planeta)
    
    try:
        # Primero eliminamos los satélites asociados
        Satelite.query.filter_by(id_planeta=id_planeta).delete()
        
        # Luego eliminamos el planeta
        db.session.delete(planeta)
        db.session.commit()
        flash('Planeta eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el planeta: ' + str(e), 'error')



@app.route('/planeta/editar/<int:id_planeta>', methods=['GET', 'POST'])
def editar_planeta(id_planeta):
    planeta = Planeta.query.get_or_404(id_planeta)
    form = PlanetaForm(obj=planeta)
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Validar campos manualmente
                nombre = form.nombre.data
                distancia_a_sol = form.distancia_a_sol.data
                inclinacion_orb = form.inclinacion_orb.data
                periodo_orbital = form.periodo_orbital.data
                velocidad_orb = form.velocidad_orb.data

                # Validaciones
                if not nombre:
                    flash('El nombre es requerido', 'error')
                    return render_template('editar_planeta.html', form=form, planeta=planeta)
                
                if not Planeta.validate_name(nombre, id_planeta):
                    flash('Ya existe un planeta con ese nombre', 'error')
                    return render_template('editar_planeta.html', form=form, planeta=planeta)
                
                if not Planeta.validate_distance(distancia_a_sol):
                    flash('La distancia al Sol debe estar entre 0.3 y 31.0 UA', 'error')
                    return render_template('editar_planeta.html', form=form, planeta=planeta)
                
                if not Planeta.validate_inclinacion_orb(inclinacion_orb):
                    flash('La inclinación orbital debe estar entre 0 y 180°', 'error')
                    return render_template('editar_planeta.html', form=form, planeta=planeta)
                
                if not Planeta.validate_periodo_orbital(periodo_orbital):
                    flash('El periodo orbital debe ser mayor a 0', 'error')
                    return render_template('editar_planeta.html', form=form, planeta=planeta)
                
                if not Planeta.validate_velocidad_orb(velocidad_orb):
                    flash('La velocidad orbital debe ser mayor a 0', 'error')
                    return render_template('editar_planeta.html', form=form, planeta=planeta)

                # Actualizar el planeta
                datos_anteriores = {
                    'nombre': planeta.nombre,
                    'distancia_a_sol': planeta.distancia_a_sol,
                    'inclinacion_orb': planeta.inclinacion_orb,
                    'periodo_orbital': planeta.periodo_orbital,
                    'velocidad_orb': planeta.velocidad_orb
                }
                
                datos_nuevos = {
                    'nombre': nombre,
                    'distancia_a_sol': distancia_a_sol,
                    'inclinacion_orb': inclinacion_orb,
                    'periodo_orbital': periodo_orbital,
                    'velocidad_orb': velocidad_orb
                }

                # Registrar en la auditoría
                Auditoria.log_accion(
                    id_entidad=id_planeta,
                    entidad='PLANETA',
                    accion='UPDATE',
                    datos_anteriores=datos_anteriores,
                    datos_nuevos=datos_nuevos
                )

                # Actualizar el planeta
                planeta.nombre = nombre
                planeta.distancia_a_sol = distancia_a_sol
                planeta.inclinacion_orb = inclinacion_orb
                planeta.periodo_orbital = periodo_orbital
                planeta.velocidad_orb = velocidad_orb
                
                db.session.commit()
                flash('Planeta actualizado exitosamente', 'success')
                return redirect(url_for('ver_planeta', id_planeta=planeta.id_planeta))
                
            except Exception as e:
                db.session.rollback()
                error_msg = str(e)
                if 'periodo orbital' in error_msg.lower():
                    flash('Error: El periodo orbital de un satélite no puede ser mayor al periodo orbital de su planeta', 'error')
                else:
                    flash('Error al actualizar el planeta: ' + error_msg, 'error')
                return render_template('editar_planeta.html', form=form, planeta=planeta)
    
    return render_template('editar_planeta.html', form=form, planeta=planeta)

@app.route('/consulta/distancia', methods=['GET', 'POST'])
def consulta_distancia():
    form = ConsultaDistanciaForm()
    planetas = []
    
    if form.validate_on_submit():
        try:
            distancia = form.distancia.data
            orden = form.orden.data
            
            # Consultar planetas con distancia menor que la especificada
            planetas = Planeta.query.filter(Planeta.distancia_a_sol < distancia).order_by(Planeta.distancia_a_sol.desc())
            
            planetas = planetas.all()
            
            if not planetas:
                flash(f'No se encontraron planetas con distancia menor a {distancia} UA', 'info')
            else:
                flash(f'Se encontraron {len(planetas)} planetas con distancia menor a {distancia} UA', 'info')
            
        except Exception as e:
            flash('Error en la consulta: ' + str(e), 'error')
    
    return render_template('consulta_distancia.html', form=form, planetas=planetas)

@app.route('/consulta/inclinacion', methods=['GET', 'POST'])
def consulta_inclinacion():
    form = ConsultaInclinacionForm()
    planetas = []
    inclinacion_referencia = None
    
    # Poblar el campo de selección de planetas
    form.id_planeta.choices = [(p.id_planeta, p.nombre) for p in Planeta.query.all()]
    
    if form.validate_on_submit():
        id_planeta = form.id_planeta.data
        
        # Obtener el planeta de referencia
        planeta_referencia = Planeta.query.get_or_404(id_planeta)
        inclinacion_referencia = planeta_referencia.inclinacion_orb
        
        # Consultar planetas con inclinación menor a la del planeta seleccionado
        planetas = Planeta.query.filter(
            Planeta.inclinacion_orb < planeta_referencia.inclinacion_orb,
            Planeta.id_planeta != id_planeta
        ).order_by(Planeta.inclinacion_orb).all()
            
        if not planetas:
            flash(f'No se encontraron planetas con inclinación menor a {planeta_referencia.inclinacion_orb:.2f}°', 'info')
        else:
            flash(f'Se encontraron {len(planetas)} planetas con inclinación menor a {planeta_referencia.inclinacion_orb:.2f}°', 'info')
    
    return render_template('consulta_inclinacion.html', form=form, planetas=planetas, inclinacion_referencia=inclinacion_referencia)

if __name__ == '__main__':
    app.run(debug=True)
