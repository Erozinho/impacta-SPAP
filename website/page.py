from flask import Blueprint, request, render_template, session
from db import db

page = Blueprint('login', __name__, template_folder="template")

@page.route('/register', methods=['GET'])
def carregar():
    return render_template("registrar.html")

@page.route('/register', methods=['POST'])
def register():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    senha = request.form.get('senha')
    dados = {"nome":nome, "cpf":cpf, "senha":senha}
    db.collection('users').document(cpf).set(dados)
    db.collection('contas').document(cpf).set({"saldo": 0, "fatura":0})
    return '<h1>REGISTRADO COM SUCESSO</h1>'


