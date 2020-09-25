# sscalvo@gmail.com
# 05/08/2020

from flask import Markup
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, RadioField, TextAreaField, TextField, validators
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp, Optional
from .spanishID import spanishID

class UploadForm(FlaskForm):
    msg_obligatorio = "Campo obligatorio"
    # Etiquetas con html incrustado
    lbl_fileYear0 = Markup('<b>Fichero CSV</b> del último ejercicio')
    lbl_fileYear1 = Markup('<b>Fichero exportado</b> año anterior')
    lbl_fileYear2 = Markup('<b>Fichero exportado</b> hace 2 años')
    
    fileFieldNames = ['fileYear0', 'fileYear1', 'fileYear2'] # CUSTOM FIELD: Actualizar si agregas o quitas FieldFields !!!
    fileYear0 = FileField(lbl_fileYear0, validators=[FileRequired(msg_obligatorio)]) # 'fileYear0'
    fileYear1 = FileField(lbl_fileYear1, validators=[Optional()])                    # 'fileYear1'
    fileYear2 = FileField(lbl_fileYear2, validators=[Optional()])                    # 'fileYear2'
    
    ejercicio    = IntegerField(Markup('<b>EJERCICIO</b> actual'), validators=[DataRequired(msg_obligatorio), NumberRange(min=2015, max=2050, message='Debe ser un año entre 2015 y 2050')])
    NIF          = StringField(Markup('<b>NIF</b> del declarante'), validators=[DataRequired("Debe ingresar un NIF"), spanishID()])
    denominacion = StringField(Markup('<b>DENOMINACIÓN</b> del declarante'), validators=[DataRequired("Ingresar nombre completo (Denominación) de la entidad, sin el anagrama")])
    telefono     = StringField(Markup('<b>TELÉFONO</b> de contacto'), validators=[DataRequired("Campo obligatorio (9 dígitos)"),Regexp(regex='[0-9]{9}')])
    persona      = StringField(Markup('<b>PERSONA</b> de contacto'), validators=[DataRequired("Ingrese el nombre de la persona de contacto")])
    justificante = StringField(Markup('<b>NÚMERO</b> justificante declaración'), validators=[DataRequired("Campo numérico de 13 dígitos"),Regexp(regex='[0-9]{13}', message='Campo numérico de 13 dígitos')])
    # idAnterior: En caso de que se haya consignado "S" en el campo "Declaración sustitutiva", se consignará el número identificativo correspondiente a la declaración a la que sustituye. 
    idAnterior   = StringField(Markup('<b>ID</b> declaración anterior'), validators=[DataRequired("Campo numérico de 13 dígitos"),Regexp(regex='[0-9]{13}', message='Campo numérico de 13 dígitos') ])
    
    tipoDeclaracion = RadioField('Label', choices=[('XX','Normal'),('CX','Complementaria'),('XS','Sustitutiva')],  default='XX')
    submit = SubmitField('Generar modelo 182')
    
class ContactForm(FlaskForm):
	nombre = TextField('Nombre', [validators.DataRequired("Nombre")])
	email = TextField('E-mail', [validators.DataRequired("Correo al que quieres que te respondamos"), validators.Email("No parece un correo válido")])
	titulo = TextField('Titulo', [validators.DataRequired("Título?")])
	mensaje = TextAreaField('Tu mensaje..', [validators.DataRequired("Tu mensaje..")])
	submit = SubmitField('Enviar')