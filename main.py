from flask import Flask, request, render_template, redirect, url_for, flash
from db import db
from models import Produto, Usuario
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.secret_key = 'chave-secreta'  # Troque por algo mais seguro em produção
db.init_app(app)

# Configurar LoginManager
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('index'))
        else:
            flash("Email ou senha inválidos.")
            return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/registrar-usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'GET':
        return render_template('registro_usuario.html')
    else:
        email = request.form['email']
        senha = request.form['senha']

        if not senha_forte(senha):
            flash("A senha deve ter pelo menos 6 caracteres, incluindo letra maiúscula, minúscula, número e símbolo.")
            return redirect(url_for('registrar_usuario'))

        if Usuario.query.filter_by(email=email).first():
            flash("Usuário já existe.")
            return redirect(url_for('registrar_usuario'))

        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Usuário registrado com sucesso.")
        return redirect(url_for('login'))
    
def senha_forte(senha):
    if(len(senha) < 6 or
        not re.search(r'[A-Z]', senha) or
        not re.search(r'[a-z]', senha) or
        not re.search(r'[0-9]', senha) or
        not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha)):
        return False
    return True

@app.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'GET':
        return render_template('esqueci_senha.html')
    else:
        email = request.form['email']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            token = str(uuid.uuid4())
            usuario.reset_token = token
            db.session.commit()
            # Aqui, em um sistema real, você enviaria por e-mail
            flash(f"Link de redefinição: {url_for('resetar_senha', token=token, _external=True)}")
        else:
            flash("Email não encontrado.")
        return redirect(url_for('esqueci_senha'))

@app.route('/resetar-senha/<token>', methods=['GET', 'POST'])
def resetar_senha(token):
    usuario = Usuario.query.filter_by(reset_token=token).first()
    if not usuario:
        flash("Token inválido ou expirado.")
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('resetar_senha.html', token=token)
    else:
        nova_senha = request.form['senha']
        if not senha_forte(nova_senha):
            flash("A senha deve ter pelo menos 8 caracteres, incluindo letra maiúscula, minúscula, número e símbolo.")
            return redirect(url_for('resetar_senha', token=token))

        usuario.senha = generate_password_hash(nova_senha)
        usuario.reset_token = None
        db.session.commit()
        flash("Senha redefinida com sucesso.")
        return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    produtos = db.session.query(Produto).all()
    return render_template('index.html', produtos=produtos)

@app.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'GET':
        return render_template('registrar_produto.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        marca = request.form['marcaForm']
        categoria = request.form['categoriaForm']
        preco = request.form['precoForm']
        quantidade = request.form['quantidadeForm']
        unidade_medida = request.form['uniMedidaForm']
        peso = request.form['pesoForm']

        novo_produto = Produto(
            nome=nome,
            marca=marca,
            categoria=categoria,
            preco=preco,
            quantidade=quantidade,
            unidade_medida=unidade_medida,
            peso=peso
        )
        db.session.add(novo_produto)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=["GET", "POST"])
@login_required
def editar(id):
    produto = db.session.query(Produto).filter_by(id=id).first()
    if request.method == "GET":
        return render_template('editar_produto.html', produto=produto)
    elif request.method == "POST":
        produto.nome = request.form['nomeForm']
        produto.marca = request.form['marcaForm']
        produto.categoria = request.form['categoriaForm']
        produto.preco = request.form['precoForm']
        produto.quantidade = request.form['quantidadeForm']
        produto.unidade_medida = request.form['uniMedidaForm']
        produto.peso = request.form['pesoForm']
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
@login_required
def deletar(id):
    produto = db.session.query(Produto).filter_by(id=id).first()
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
