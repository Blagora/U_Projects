from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length
import json

# Middleware para manejar métodos HTTP personalizados
class HTTPMethodOverrideMiddleware(object):
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
        if method in self.allowed_methods:
            method = method.encode('ascii', 'replace')
            environ['REQUEST_METHOD'] = method
        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)

app = Flask(__name__)
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-3V3HASL\\SQLEXPRESS/SistemaPlanetario?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Para ver las consultas SQL

# Configuración de la base de datos
db = SQLAlchemy(app)

def create_session():
    """Crea una nueva sesión con autocommit deshabilitado"""
    return db.create_scoped_session(options={
        'autocommit': False,
        'expire_on_commit': False,
        'bind': db.engine
    })

# Establecer la sesión personalizada como sesión por defecto
db.session = create_session()

# Inicializar la base de datos
with app.app_context():
    try:
        db.create_all()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")

class Planeta(db.Model):
    __tablename__ = 'PLANETA'
    id_planeta = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    distancia_a_sol = db.Column(db.Float, nullable=False)
    inclinacion_orb = db.Column(db.Float, nullable=False)
    periodo_orbital = db.Column(db.Float, nullable=False)
    velocidad_orb = db.Column(db.Float, nullable=False)
    
    # Relación con satélites
    satelites = db.relationship('Satelite', backref='planeta', lazy=True)

    @staticmethod
    def get_next_id():
        max_id = db.session.query(db.func.max(Planeta.id_planeta)).scalar()
        return (max_id or 0) + 1

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

    @staticmethod
    def get_next_id():
        max_id = db.session.query(db.func.max(Satelite.id_satelite)).scalar()
        return (max_id or 0) + 1

    def update(self, nombre, excentricidad, periodo_orb, inclinacion_orb, session):
        """
        Actualiza los datos del satélite con validaciones
        """
        try:
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
                
            # Actualizar los valores directamente en el objeto
            print(f"Actualizando satélite ID {self.id_satelite}")
            print(f"Antes: {self.nombre}, {self.excentricidad}, {self.periodo_orb}, {self.inclinacion_orb}")
            print(f"Después: {nombre}, {excentricidad}, {periodo_orb}, {inclinacion_orb}")
            
            # Asegurar que el objeto esté en la sesión
            if self not in session:
                print(f"Advertencia: Satélite ID {self.id_satelite} no está en la sesión")
                session.add(self)
                session.flush()
            
            # Actualizar explícitamente cada campo
            session.query(Satelite).filter_by(id_satelite=self.id_satelite).update({
                'nombre': nombre,
                'excentricidad': excentricidad,
                'periodo_orb': periodo_orb,
                'inclinacion_orb': inclinacion_orb
            })
            
            # Ejecutar la actualización
            session.flush()
            
            # Verificar si la actualización tuvo éxito
            updated = session.query(Satelite).filter_by(id_satelite=self.id_satelite).first()
            if not updated:
                raise ValueError(f"No se encontró satélite con ID {self.id_satelite} después de la actualización")
            
            # Actualizar los valores del objeto
            self.nombre = updated.nombre
            self.excentricidad = updated.excentricidad
            self.periodo_orb = updated.periodo_orb
            self.inclinacion_orb = updated.inclinacion_orb
            
        except Exception as e:
            print(f"Error al actualizar satélite: {str(e)}")
            session.rollback()
            raise

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
    id_planeta = IntegerField('ID Planeta', validators=[
        DataRequired(message='El ID del planeta es requerido')
    ], render_kw={'readonly': True})
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
    try:
        planetas = Planeta.query.order_by(Planeta.distancia_a_sol).all()
        print("Planetas encontrados:")
        for planeta in planetas:
            print(f"- {planeta.nombre} (ID: {planeta.id_planeta})")
        return render_template('index.html', planetas=planetas)
    except Exception as e:
        flash(f'Error al cargar los planetas: {str(e)}', 'error')
        return render_template('index.html', planetas=[])

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
    """
    Crea un nuevo planeta
    """
    try:
        # Crear una nueva sesión
        session = create_session()
        try:
            form = PlanetaForm()
            
            if form.validate_on_submit():
                try:
                    # Validar los datos
                    nombre = form.nombre.data
                    distancia_a_sol = form.distancia_a_sol.data
                    inclinacion_orb = form.inclinacion_orb.data
                    periodo_orbital = form.periodo_orbital.data
                    velocidad_orb = form.velocidad_orb.data

                    # Validaciones adicionales
                    if not Planeta.validate_name(nombre):
                        flash('El nombre del planeta ya existe', 'error')
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

                    # Crear nuevo planeta
                    nuevo_id = Planeta.get_next_id()
                    planeta = Planeta(
                        id_planeta=nuevo_id,
                        nombre=nombre,
                        distancia_a_sol=distancia_a_sol,
                        inclinacion_orb=inclinacion_orb,
                        periodo_orbital=periodo_orbital,
                        velocidad_orb=velocidad_orb
                    )

                    # Agregar a la sesión
                    session.add(planeta)
                    
                    # Registrar en la auditoría
                    Auditoria.log_accion(
                        id_entidad=nuevo_id,
                        entidad='PLANETA',
                        accion='INSERT',
                        datos_anteriores=None,
                        datos_nuevos={
                            'id_planeta': nuevo_id,
                            'nombre': nombre,
                            'distancia_a_sol': distancia_a_sol,
                            'inclinacion_orb': inclinacion_orb,
                            'periodo_orbital': periodo_orbital,
                            'velocidad_orb': velocidad_orb
                        }
                    )

                    # Commit manual
                    session.commit()
                    flash('Planeta creado exitosamente', 'success')
                    return redirect(url_for('ver_planeta', id_planeta=nuevo_id))
                except Exception as e:
                    session.rollback()
                    flash(f'Error al crear el planeta: {str(e)}', 'error')
                    return render_template('nuevo_planeta.html', form=form)

            return render_template('nuevo_planeta.html', form=form)
        except Exception as e:
            print(f"Error en nuevo_planeta: {str(e)}")
            session.rollback()
            flash(f'Error al crear el planeta: {str(e)}', 'error')
            return render_template('nuevo_planeta.html', form=form)
        finally:
            session.close()
    except Exception as e:
        print(f"Error inesperado en nuevo_planeta: {str(e)}")
        flash(f'Error inesperado: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/satelite/editar/<int:id_satelite>', methods=['GET', 'POST'])
def editar_satelite(id_satelite):
    """
    Edita un satélite existente
    """
    try:
        # Crear una nueva sesión
        session = create_session()
        
        # Obtener el satélite
        satelite = session.query(Satelite).get(id_satelite)
        if not satelite:
            flash('Satélite no encontrado', 'error')
            session.close()
            return redirect(url_for('index'))

        # Obtener el planeta asociado
        planeta = session.query(Planeta).get(satelite.id_planeta)
        if not planeta:
            flash('Planeta asociado no encontrado', 'error')
            session.close()
            return redirect(url_for('index'))

        form = SateliteForm(obj=satelite)
        form.id_planeta.data = satelite.id_planeta
        
        if form.validate_on_submit():
            try:
                # Validar que el nombre sea único por planeta
                if not Satelite.validate_nombre(form.nombre.data, form.id_planeta.data, satelite.id_satelite):
                    flash('El nombre del satélite ya existe para este planeta', 'error')
                    return render_template('editar_satelite.html', form=form, satelite=satelite)

                # Validar que el periodo orbital sea menor al del planeta
                if form.periodo_orb.data >= planeta.periodo_orbital:
                    flash('El periodo orbital del satélite debe ser menor al del planeta', 'error')
                    return render_template('editar_satelite.html', form=form, satelite=satelite)

                # Asegurar que el satélite esté en la sesión
                if satelite not in session:
                    session.add(satelite)
                
                # Guardar los datos anteriores antes de actualizar
                datos_anteriores = {
                    'nombre': satelite.nombre,
                    'excentricidad': satelite.excentricidad,
                    'periodo_orb': satelite.periodo_orb,
                    'inclinacion_orb': satelite.inclinacion_orb
                }

                # Actualizar el satélite usando el método update
                satelite.update(
                    nombre=form.nombre.data,
                    excentricidad=form.excentricidad.data,
                    periodo_orb=form.periodo_orb.data,
                    inclinacion_orb=form.inclinacion_orb.data,
                    session=session
                )

                # Registrar en la auditoría
                datos_nuevos = {
                    'nombre': form.nombre.data,
                    'excentricidad': form.excentricidad.data,
                    'periodo_orb': form.periodo_orb.data,
                    'inclinacion_orb': form.inclinacion_orb.data
                }

                # Crear una nueva instancia de Auditoria y agregarla a la sesión
                auditoria = Auditoria(
                    id_entidad=id_satelite,
                    entidad='SATELITE',
                    accion='UPDATE',
                    datos_anteriores=json.dumps(datos_anteriores),
                    datos_nuevos=json.dumps(datos_nuevos)
                )
                session.add(auditoria)

                # Commit manual
                session.commit()
                flash('Satélite actualizado exitosamente', 'success')
                return redirect(url_for('ver_planeta', id_planeta=satelite.id_planeta))
            except Exception as e:
                session.rollback()
                flash(f'Error al guardar los cambios: {str(e)}', 'error')
                return render_template('editar_satelite.html', form=form, satelite=satelite)

        return render_template('editar_satelite.html', form=form, satelite=satelite)
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'error')
        session.close()
        return redirect(url_for('index'))

@app.route('/consulta/distancia', methods=['GET', 'POST'])
def consulta_distancia():
    try:
        form = ConsultaDistanciaForm()
        if form.validate_on_submit():
            try:
                distancia = form.distancia.data
                orden = form.orden.data
                
                # Consultar planetas con distancia menor a la dada
                planetas = Planeta.query.filter(
                    Planeta.distancia_a_sol < distancia
                ).order_by(
                    Planeta.distancia_a_sol.asc() if orden == 'asc' else Planeta.distancia_a_sol.desc()
                ).all()
                
                # Verificar si hay resultados
                if not planetas:
                    flash('No se encontraron planetas con distancia menor a la especificada', 'warning')
                    return render_template('consulta_distancia.html', form=form, distancia=distancia)
                
                return render_template('consulta_distancia.html', form=form, planetas=planetas, distancia=distancia)
            except Exception as e:
                print(f"Error en la consulta de distancia: {str(e)}")
                flash(f'Error en la consulta de distancia: {str(e)}', 'error')
                return render_template('consulta_distancia.html', form=form)
        
        return render_template('consulta_distancia.html', form=form)
    except Exception as e:
        print(f"Error en consulta_distancia: {str(e)}")
        flash(f'Error en la consulta: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/consulta/inclinacion', methods=['GET', 'POST'])
def consulta_inclinacion():
    try:
        form = ConsultaInclinacionForm()
        
        # Llenar el campo de selección de planetas
        planetas = Planeta.query.all()
        form.id_planeta.choices = [(p.id_planeta, p.nombre) for p in planetas]
        
        if form.validate_on_submit():
            id_planeta = form.id_planeta.data
            
            # Obtener el planeta seleccionado
            planeta = Planeta.query.get(id_planeta)
            if not planeta:
                flash('Planeta no encontrado', 'error')
                return render_template('consulta_inclinacion.html', form=form)

            # Consultar planetas con inclinación menor a la del planeta seleccionado
            planetas = Planeta.query.filter(
                Planeta.inclinacion_orb < planeta.inclinacion_orb,
                Planeta.id_planeta != id_planeta
            ).order_by(
                Planeta.inclinacion_orb.asc()
            ).all()
            
            # Verificar si hay resultados
            if not planetas:
                flash('No se encontraron planetas con inclinación menor a la del planeta seleccionado', 'warning')
                return render_template('consulta_inclinacion.html', form=form, planeta=planeta)
            
            return render_template('consulta_inclinacion.html', form=form, planetas=planetas, planeta=planeta)
        
        return render_template('consulta_inclinacion.html', form=form)
    except Exception as e:
        print(f"Error en consulta_inclinacion: {str(e)}")
        flash(f'Error en la consulta: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/planeta/<int:id_planeta>', methods=['GET'])
def ver_planeta(id_planeta):
    """
    Muestra los detalles de un planeta y sus satélites
    """
    try:
        # Crear una nueva sesión
        session = create_session()
        try:
            # Consultar el planeta
            planeta = session.query(Planeta).get(id_planeta)
            if not planeta:
                flash(f'No se encontró planeta con ID {id_planeta}', 'error')
                session.close()
                return redirect(url_for('index'))

            # Obtener satélites del planeta
            satelites = session.query(Satelite).filter_by(id_planeta=id_planeta).all()
            return render_template('ver_planeta.html', planeta=planeta, satelites=satelites)
        except Exception as e:
            flash(f'Error al ver el planeta: {str(e)}', 'error')
            session.close()
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/planeta/editar/<int:id_planeta>', methods=['GET', 'POST'])
def editar_planeta(id_planeta):
    """
    Edita un planeta existente
    """
    try:
        # Crear una nueva sesión
        session = create_session()
        try:
            # Consultar el planeta
            planeta = session.query(Planeta).get(id_planeta)
            if not planeta:
                flash(f'No se encontró planeta con ID {id_planeta}', 'error')
                return redirect(url_for('index'))

            # Obtener satélites del planeta
            satelites = session.query(Satelite).filter_by(id_planeta=id_planeta).all()

            form = PlanetaForm(obj=planeta)
            
            if form.validate_on_submit():
                try:
                    # Obtener datos del formulario
                    nombre = form.nombre.data
                    distancia_a_sol = form.distancia_a_sol.data
                    inclinacion_orb = form.inclinacion_orb.data
                    periodo_orbital = form.periodo_orbital.data
                    velocidad_orb = form.velocidad_orb.data

                    # Validar que el nombre sea único
                    if not Planeta.validate_name(nombre, id_planeta):
                        flash('El nombre del planeta ya existe', 'error')
                        return render_template('editar_planeta.html', form=form, planeta=planeta, satelites=satelites)

                    # Validar que la distancia sea única
                    query = session.query(Planeta).filter_by(distancia_a_sol=distancia_a_sol)
                    if id_planeta:
                        query = query.filter(Planeta.id_planeta != id_planeta)
                    if query.first():
                        flash('Ya existe un planeta con esta distancia al Sol', 'error')
                        return render_template('editar_planeta.html', form=form, planeta=planeta, satelites=satelites)

                    # Asegurar que el planeta esté en la sesión
                    if planeta not in session:
                        session.add(planeta)
                        session.flush()

                    # Actualizar explícitamente cada campo usando SQLAlchemy
                    session.query(Planeta).filter_by(id_planeta=id_planeta).update({
                        'nombre': nombre,
                        'distancia_a_sol': distancia_a_sol,
                        'inclinacion_orb': inclinacion_orb,
                        'periodo_orbital': periodo_orbital,
                        'velocidad_orb': velocidad_orb
                    })
                    
                    # Ejecutar la actualización
                    session.flush()
                    
                    # Verificar si la actualización tuvo éxito
                    updated = session.query(Planeta).filter_by(id_planeta=id_planeta).first()
                    if not updated:
                        raise ValueError(f"No se encontró planeta con ID {id_planeta} después de la actualización")
                    
                    # Actualizar los valores del objeto
                    planeta.nombre = nombre
                    planeta.distancia_a_sol = distancia_a_sol
                    planeta.inclinacion_orb = inclinacion_orb
                    planeta.periodo_orbital = periodo_orbital
                    planeta.velocidad_orb = velocidad_orb

                    # Registrar en la auditoría
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

                    Auditoria.log_accion(
                        id_entidad=id_planeta,
                        entidad='PLANETA',
                        accion='UPDATE',
                        datos_anteriores=datos_anteriores,
                        datos_nuevos=datos_nuevos
                    )

                    # Commit manual
                    session.commit()
                    flash('Planeta actualizado exitosamente', 'success')
                    return redirect(url_for('ver_planeta', id_planeta=id_planeta))
                except Exception as e:
                    print(f"Error al actualizar el planeta: {str(e)}")
                    session.rollback()
                    flash(f'Error al actualizar el planeta: {str(e)}', 'error')
                    return render_template('editar_planeta.html', form=form, planeta=planeta, satelites=satelites)

            return render_template('editar_planeta.html', form=form, planeta=planeta, satelites=satelites)
        except Exception as e:
            print(f"Error en la operación de planeta: {str(e)}")
            flash(f'Error al editar el planeta: {str(e)}', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        print(f"Error en editar_planeta: {str(e)}")
        session.rollback()
        flash(f'Error al editar el planeta: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        # Cerrar la sesión
        session.close()

@app.route('/planeta/<int:id_planeta>/satelite/nuevo', methods=['GET', 'POST'])
def nuevo_satelite(id_planeta):
    try:
        # Crear una nueva sesión
        session = create_session()
        
        # Verificar que el planeta existe
        planeta = session.query(Planeta).get(id_planeta)
        if not planeta:
            flash('El planeta no existe', 'error')
            return redirect(url_for('index'))

        form = SateliteForm()
        
        if form.validate_on_submit():
            try:
                # Validar los datos antes de crear el objeto
                nombre = form.nombre.data
                excentricidad = form.excentricidad.data
                periodo_orb = form.periodo_orb.data
                inclinacion_orb = form.inclinacion_orb.data

                # Validaciones adicionales
                if not Satelite.validate_nombre(nombre, id_planeta):
                    flash('El nombre del satélite ya existe para este planeta', 'error')
                    return render_template('nuevo_satelite.html', form=form, planeta=planeta)

                if periodo_orb >= planeta.periodo_orbital:
                    flash('El periodo orbital del satélite debe ser menor al del planeta', 'error')
                    return render_template('nuevo_satelite.html', form=form, planeta=planeta)

                # Validar la excentricidad
                if not Satelite.validate_excentricidad(excentricidad):
                    flash('La excentricidad debe estar entre 0 y 1', 'error')
                    return render_template('nuevo_satelite.html', form=form, planeta=planeta)

                # Validar la inclinación orbital
                if not Satelite.validate_inclinacion_orb(inclinacion_orb):
                    flash('La inclinación orbital debe estar entre 0 y 180°', 'error')
                    return render_template('nuevo_satelite.html', form=form, planeta=planeta)

                # Crear nuevo satélite
                nuevo_id = Satelite.get_next_id()
                satelite = Satelite(
                    id_satelite=nuevo_id,
                    nombre=nombre,
                    excentricidad=excentricidad,
                    periodo_orb=periodo_orb,
                    inclinacion_orb=inclinacion_orb,
                    id_planeta=id_planeta
                )

                # Agregar a la sesión
                session.add(satelite)
                
                # Registrar en la auditoría
                Auditoria.log_accion(
                    id_entidad=nuevo_id,
                    entidad='SATELITE',
                    accion='INSERT',
                    datos_anteriores=None,
                    datos_nuevos={
                        'id_satelite': nuevo_id,
                        'nombre': nombre,
                        'excentricidad': excentricidad,
                        'periodo_orb': periodo_orb,
                        'inclinacion_orb': inclinacion_orb,
                        'id_planeta': id_planeta
                    }
                )

                # Commit manual
                session.commit()
                flash('Satélite creado exitosamente', 'success')
                return redirect(url_for('ver_planeta', id_planeta=id_planeta))
            except Exception as e:
                session.rollback()
                flash(f'Error al crear el satélite: {str(e)}', 'error')
                return render_template('nuevo_satelite.html', form=form, planeta=planeta)

        return render_template('nuevo_satelite.html', form=form, planeta=planeta)
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        # Cerrar la sesión
        session.close()

@app.route('/planeta/<int:id_planeta>/satelite/<int:id_satelite>/eliminar', methods=['GET', 'POST'])
def eliminar_satelite(id_planeta, id_satelite):
    try:
        # Crear una nueva sesión
        session = create_session()
        try:
            # Verificar que el planeta existe
            planeta = session.query(Planeta).get(id_planeta)
            if not planeta:
                flash('El planeta no existe', 'error')
                return redirect(url_for('index'))

            # Verificar que el satélite existe
            satelite = session.query(Satelite).get(id_satelite)
            if not satelite:
                flash('El satélite no existe', 'error')
                return redirect(url_for('ver_planeta', id_planeta=id_planeta))

            # Registrar en la auditoría
            datos_anteriores = {
                'nombre': satelite.nombre,
                'excentricidad': satelite.excentricidad,
                'periodo_orb': satelite.periodo_orb,
                'inclinacion_orb': satelite.inclinacion_orb,
                'id_planeta': satelite.id_planeta
            }

            Auditoria.log_accion(
                id_entidad=id_satelite,
                entidad='SATELITE',
                accion='DELETE',
                datos_anteriores=datos_anteriores,
                datos_nuevos=None
            )

            # Eliminar el satélite
            session.delete(satelite)

            # Commit manual
            session.commit()
            flash('Satélite eliminado exitosamente', 'success')
            return redirect(url_for('ver_planeta', id_planeta=id_planeta))
        except Exception as e:
            print(f"Error al eliminar el satélite: {str(e)}")
            session.rollback()
            flash(f'Error al eliminar el satélite: {str(e)}', 'error')
            return redirect(url_for('ver_planeta', id_planeta=id_planeta))
    except Exception as e:
        print(f"Error en eliminar_satelite: {str(e)}")
        session.rollback()
        flash(f'Error al eliminar el satélite: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        # Cerrar la sesión
        session.close()

if __name__ == '__main__':
    app.run(debug=True)
