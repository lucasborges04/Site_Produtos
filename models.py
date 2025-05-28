from db import db

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    unidade_medida = db.Column(db.String(100), nullable=False)
    peso = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<{self.nome}>"