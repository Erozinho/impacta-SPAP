from flask import Blueprint, request, render_template, session, redirect, flash
from db import db

page = Blueprint('login', __name__, template_folder="template")

@page.route('/')
def home():
    return redirect('http://127.0.0.1:5000/login', code=302)


@page.route('/register', methods=['GET'])
def carregar():
    return render_template("registrar.html")


@page.route('/register', methods=['POST'])
def register():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    senha = request.form.get('senha')

    dados = {"nome":nome, "cpf":cpf, "senha":senha}

    doc_ref = db.collection('users').document(cpf)
    doc = doc_ref.get()

    if doc.exists:
        flash("Já existe uma conta criado com esse CPF!", "info")
        return render_template("registrar.html")
    
    db.collection('users').document(cpf).set(dados)
    db.collection('contas').document(cpf).set({"saldo": 0, "fatura":0})
    flash("Conta cadastrada com sucesso!", "info")
    return render_template("login.html")


@page.route('/login', methods=['GET'])
def carregar_l():
    return render_template('login.html')


@page.route('/login', methods=['POST'])
def login():
    cpf = request.form.get('cpf')
    senha = request.form.get('senha')

    cred = db.collection("users").document(cpf).get()
    cred = (cred.to_dict())

    if cred['senha'] == senha:
        print('PASSOU')
        infos = db.collection("contas").document(cpf).get()
        infos = infos.to_dict()
        session["cpf"] = cred['cpf']
        session["nome"] = cred['nome']
        session["saldo"] = infos['saldo']
        session["fatura"] = infos['fatura']
        flash("Acesso bem sucedido!", "info")
        return redirect("http://127.0.0.1:5000/home", code=302)

    flash("INFORMAÇÕES INCORRETAS", "info")
    return render_template('login.html')
