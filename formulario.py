from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,  IntegerField,SelectField
from wtforms.fields import DecimalField, EmailField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired


class Registro(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su usuario"})
    correo = EmailField('Correo', validators=[DataRequired(message='No dejar vacío, completar' )],render_kw = {"placeholder": "Digite el Correo Electronico"})
    password =PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacío, completar')],render_kw = {"placeholder": "Digite la Contraseña"})

    nombres = StringField('Nombres', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite sus nombres", "id":"nombres"})
    apellidos = StringField('Apellidos', validators=[DataRequired(message='No dejar vacío, completar' )],render_kw = {"placeholder": "Digite sus apellidos", "id":"apellidos"})
    #fechaDeNacimiento =DateField('Fecha De Nacimiento', validators=[DataRequired(message='No dejar vacío, completar')], format='%d-%m-%Y', render_kw = {"placeholder": "Digite su fecha de nacimiento" , "disabled":"true"})
    fechaDeNacimiento =StringField('Fecha De Nacimiento', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su fecha de nacimiento" , "id":"fechaDeNacimiento" })
    identificacion =IntegerField('Identificación', validators=[DataRequired(message='No dejar vacío, completar')],render_kw = {"placeholder": "Digite su identificación" , "id":"identificacion"})
    correo =EmailField('Correo', validators=[DataRequired(message='No dejar vacío, completar')],render_kw = {"placeholder": "Digite su correo electronico", "id":"correo" })
    celular = IntegerField('Celular', validators=[DataRequired(message='No dejar vacío, completar')],render_kw = {"placeholder": "Digite el número de celular", "id":"celular" })
    enviar = SubmitField('Crear Usuario') 
    
class Contactenos(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su Nombre"})
    correo = EmailField('Correo', validators=[DataRequired(message='No dejar vacío, completar' )],render_kw = {"placeholder": "Digite el Correo Electronico"})
    telefono = StringField('Telefono', validators=[DataRequired(message='No dejar vacío, completar')],render_kw = {"placeholder": "Digite el Telefono"})
    mensaje = TextAreaField('Mensaje', validators=[DataRequired(message='No dejar vacío, completar')],render_kw = {"placeholder": "Digite el Mensaje"})
    enviar = SubmitField('Enviar Mensaje') 

class Menu(FlaskForm):
    busqueda = StringField('', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Que Desea comer hoy"})
    enviar = SubmitField('Buscar')

class Plato(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Nombre del plato"})
    precio = DecimalField('Precio', validators=[DataRequired(message='No dejar vacío, completar')],
                         render_kw={"placeholder": "Precio del plato"})
    descripcion = TextAreaField('Descripción', validators=[DataRequired(message='No dejar vacío, completar')],render_kw = {"placeholder": "Descripción del plato"})
    aceptar = SubmitField('Aceptar')

    
class Nosotros(FlaskForm):    
    enviar = SubmitField('Buscar') 

        
class Pedido(FlaskForm):
    enviar = SubmitField('Realizar Pedido') 

class ListaDeseo(FlaskForm):
    enviar = SubmitField('Agregar') 

class Usuario(FlaskForm):
    nombres = StringField('Nombres', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite sus nombres", "id":"nombres", "disabled":"true"})
    usuario = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite sus nombre de usuario", "id":"usuario"})
    contraseña = PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite la contraseña", "id":"contraseña"})
    apellidos = StringField('Apellidos', validators=[DataRequired(message='No dejar vacío, completar' )],render_kw = {"placeholder": "Digite sus apellidos", "id":"apellidos", "disabled":"true"})
    # fechaDeNacimiento =DateField('Fecha De Nacimiento', validators=[DataRequired(message='No dejar vacío, completar')], format='%d-%m-%Y', render_kw = {"placeholder": "Digite su fecha de nacimiento" , "disabled":"true"})
    fechaDeNacimiento =StringField('Fecha De Nacimiento', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su fecha de nacimiento" , "id":"fechaDeNacimiento" , "disabled":"true"})
    identificacion =IntegerField('Identificación', validators=[DataRequired(message='No dejar vacío, completar')],render_kw = {"placeholder": "Digite su identificación" , "id":"identificacion" , "disabled":"true"})
    correo =EmailField('Correo', validators=[DataRequired(message='No dejar vacío, completar')],render_kw = {"placeholder": "Digite su correo electronico", "id":"correo" , "disabled":"true"})
    celular = IntegerField('Celular', validators=[DataRequired(message='No dejar vacío, completar')],render_kw = {"placeholder": "Digite el número de celular", "id":"celular" , "disabled":"true"})
    rol = IntegerField('Rol', validators=[DataRequired(message='No dejar vacío, completar' )],render_kw = {"placeholder": "Digite el codigo del rol (1:Usuario, 2:Administrador, 3:Superadministrador)", "id":"rol", "disabled":"true"})    
    # rol = SelectField('Rol', choices=[(1,'Cliente'),(2,'Administrador'),(3,'Super Administrador')])