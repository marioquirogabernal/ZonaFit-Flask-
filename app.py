from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate

from database import db
from models import Cliente
from forms import Cliente_form


app = Flask(__name__)

# Configuramos la BD
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'Zona_Fit_DB'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configurar Flask-Migrate
migrate = Migrate()
migrate.init_app(app, db)

# Configuracion Flask-WTF
app.config['SECRET_KEY']='absk213k21msa@231@@@123'

@app.route('/') # url: http://localhost:5000/
def inicio():
    titulo = "Zona Fit (GYM)"
    clientes = Cliente.query.order_by(Cliente.id)
    cliente = Cliente()
    formulario_cliente = Cliente_form(obj=cliente)
    return render_template('/index.html', titulo=titulo, clientes=clientes, formulario_cliente=formulario_cliente)

@app.route("/guardar", methods=['POST'])
def guardar():
    cliente = Cliente()
    formulario_cliente = Cliente_form(obj=cliente)
    if request.method == 'POST':
        if formulario_cliente.validate_on_submit():
            formulario_cliente.populate_obj(cliente)
            app.logger.debug(f'Cliente: {cliente}')
            db.session.add(cliente)
            db.session.commit()
            return redirect(url_for('inicio'))

@app.route("/editar/<int:id>", methods=['GET','POST'])
def editar(id):
    cliente = Cliente.query.get_or_404(id)
    formulario_cliente = Cliente_form(obj=cliente)
    if request.method == 'POST':
        if formulario_cliente.validate_on_submit():
            formulario_cliente.populate_obj(cliente)
            app.logger.debug(f'Cliente: {cliente}')
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('/editar.html', formulario_cliente=formulario_cliente)

@app.route("/eliminar/<int:id>")
def eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    app.logger.debug(f'Cliente: {cliente}')
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('inicio'))
