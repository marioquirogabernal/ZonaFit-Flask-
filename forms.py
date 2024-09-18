from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired

class Cliente_form(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    membresia = StringField('Membresia', validators=[DataRequired()])
    enviar = SubmitField('Guardar')

