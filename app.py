from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import db
from models import Produto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

@app.route('/')
def index():
    produtos = db.session.query(Produto).all()
    return render_template('index.html', produtos=produtos)

@app.route('/registrar', methods=['GET', 'POST'])
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
            categoria = categoria,
            preco = preco,
            quantidade = quantidade,
            unidade_medida = unidade_medida,
            peso = peso
        )
        db.session.add(novo_produto)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=["GET", "POST"])
def editar(id):
    produto = db.session.query(Produto).filter_by(id=id).first()
    if request.method == "GET":
        return render_template('editar_produto.html', produto=produto)
    elif request.method == "POST":
        nome = request.form['nomeForm']
        marca = request.form['marcaForm']
        categoria = request.form['categoriaForm']
        preco = request.form['precoForm']
        quantidade = request.form['quantidadeForm']
        unidade_medida = request.form['uniMedidaForm']
        peso = request.form['pesoForm']

        produto.nome = nome
        produto.marca = marca
        produto.categoria = categoria
        produto.preco = preco
        produto.quantidade = quantidade
        produto.unidade_medida = unidade_medida
        produto.peso = peso
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    produto = db.session.query(Produto).filter_by(id=id).first()
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)