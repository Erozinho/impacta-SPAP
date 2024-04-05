from flask import Blueprint, request, render_template, session, redirect, flash, url_for
from db import db
import pyimgur
import requests, json
from werkzeug.utils import secure_filename
import os

user = os.path.expanduser('~')
dir_root = user + '\\Downloads'

clientid = "ede3ed94c337f67"

page = Blueprint('login', __name__, template_folder="template")

@page.route('/')
def home():
    return redirect("/login", code=302)


@page.route('/register', methods=['GET'])
def carregar():
    return render_template("registrar.html")


@page.route('/register', methods=['POST'])
def register():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    cpf = cpf.replace(".","").replace("-","")
    senha = request.form.get('senha')
    dados = {"nome":nome, "cpf":cpf, "senha":senha, "email":email, "pfp":"https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"}

    doc_ref = db.collection('users').document(cpf)
    doc = doc_ref.get()

    if doc.exists:
        flash("Já existe uma conta criado com esse CPF!", "info")
        return render_template('/register',code=302)
    
    db.collection('users').document(cpf).set(dados)
    db.collection('contas').document(cpf).set({"saldo": 0, "fatura":0})
    flash("Conta cadastrada com sucesso!", "info")
    return redirect('/login',code=302)


@page.route('/login', methods=['GET'])
def carregar_l():
    return render_template('login.html')


@page.route('/login', methods=['POST'])
def login():
    cpf = request.form.get('cpf')
    cpf = cpf.replace(".","").replace("-","")
    senha = request.form.get('senha')

    cred = db.collection("users").document(cpf).get()
    sec = (cred.to_dict())
    if cred.exists and sec['senha'] == senha:
        infos = db.collection("contas").document(cpf).get()
        infos = infos.to_dict()
        session["cpf"] = sec['cpf']
        session["nome"] = sec['nome']
        session["email"] = sec['email']
        session["pfp"] = sec['pfp']
        session["senha"] = sec['senha']
        session["saldo"] = infos['saldo']
        session["fatura"] = infos['fatura']
        flash("Acesso bem sucedido!", "info")
        return redirect('/home',code=302)

    flash("INFORMAÇÕES INCORRETAS", "error")
    return render_template('login.html')


@page.route('/logout')
def logout():
    session.pop('cpf', None)
    session.pop('nome', None)
    session.pop('saldo', None)
    session.pop('email', None)
    session.pop('pfp', None)
    session.pop('fatura', None)
    flash("Saida bem sucedida!", "info")
    return redirect('/login', code=302)


@page.route('/home', methods=['GET'])
def carregar_h():
    if 'cpf' in session:
        return render_template('home.html')
    flash("Você não esta logado!", "warning")
    return redirect("/login", code=302)


@page.route('/transfer', methods=['GET'])
def carregar_t():

    if 'cpf' in session:
        return render_template('transfer.html')

    flash("Você não esta logado!", "warning")
    return redirect("/login", code=302)


@page.route('/transfer', methods=['POST'])
def transferir():
    cpf = request.form.get('cpf')
    print(cpf)
    cpf = cpf.replace(".", "").replace("-", "")
    valor = float(request.form.get('valor'))

    doc_ref = db.collection('users').document(cpf).get()
    if doc_ref.exists:
        conta_alvo = db.collection("contas").document(cpf).get()  # pega as informações da conta(saldo e afins)
        ca_conta = conta_alvo.to_dict()
        conta_alvo = db.collection("users").document(cpf).get()  # pega as informações de usuario(cpf e nome)
        ca_info = conta_alvo.to_dict()

        valor_total = float(session['saldo'])

        if valor_total < valor:
            flash("Saldo insucificente", "warning")
            return redirect("/transfer", code=302)

        db.collection("contas").document(ca_info['cpf']).update({"saldo": ca_conta['saldo']+valor})
        db.collection("contas").document(session['cpf']).update({"saldo": float(session['saldo']) - valor})

        session["saldo"] = valor_total - valor

        flash("Transferencia realizada com sucesso!", "warning")
        return redirect("/home", code=302)

    flash("CPF invalido/ Não Cadastrado", "warning")
    return redirect("/transfer", code=302)


@page.route('/fatura', methods=['GET'])
def carregar_f():

    if 'cpf' in session:
        return render_template('fatura.html')

    flash("Você não esta logado!", "warning")
    return redirect("/login", code=302)


@page.route('/fatura', methods=['POST'])
def fatura():

    valor = float(request.form.get('valor'))
    saldo = float(session['saldo'])
    fatura = float(session['fatura'])

    if saldo < valor:
        flash("Saldo insucificente", "warning")
        return redirect("/fatura", code=302) 

    if (fatura - valor) <= 0:
        flash("Favor informar um valor igual ou menor que sua fatura!", "warning")
        return redirect("/home", code=302)
    
    db.collection("contas").document(session['cpf']).update({"fatura": float(session['fatura']) - valor})
    db.collection("contas").document(session['cpf']).update({"saldo": float(session['saldo']) - valor})
    session['fatura'] = fatura - valor
    session['saldo'] = saldo - valor
    flash("Fatura paga com sucesso!", "warning")
    return redirect("/home", code=302)


@page.route('/profile', methods=['GET'])
def profile_c():
    return render_template('profile.html',)


@page.route('/profile', methods=['POST'])
def profile_e():
    # pega os edit do primo
    nome = request.form.get('nome')
    if nome != "":
        db.collection("users").document(session['cpf']).update({"nome": nome})

    email = request.form.get('email')
    if email != "":
        db.collection("users").document(session['cpf']).update({"email": email})
    passw = request.form.get('senha')
    if passw != "":
        db.collection("users").document(session['cpf']).update({"senha": passw})
    
    file = request.files['file']
    file.save((os.path.join(dir_root, secure_filename(file.filename))))
    file = os.path.join(dir_root, secure_filename(file.filename))

    print('printado',nome)

    # upando img e apagando temp
    im = pyimgur.Imgur(clientid)
    upimg = im.upload_image(file)
    os.remove(file)

    # att o banco e instancia no session dnv
    db.collection("users").document(session['cpf']).update({"pfp": upimg.link})
    cred = db.collection("users").document(session['cpf']).get()
    sec = (cred.to_dict())
    session["nome"] = sec['nome']
    session["email"] = sec['email']
    session["pfp"] = sec['pfp']
    session["senha"] = sec['senha']
    flash("Dados alterados com sucesso!", "warning")
    return redirect("/profile", code=302)


@page.route('/forgot', methods=['GET'])
def forgot_c():
    return render_template('forgot.html',)


@page.route('/forgot', methods=['POST'])
def forgot():
    cpf = request.form.get('cpf')
    cpf = cpf.replace(".","").replace("-","")
    senha = request.form.get('senha')

    doc_ref = db.collection('users').document(cpf)
    doc = doc_ref.get()

    if doc.exists:
        db.collection("users").document(cpf).update({"senha": senha})
        flash("Senha alterada com sucesso!", "warning")
        return redirect("/login", code=302)
    else:
        flash("CPF NÃO ENCONTRADO!", "warning")
        return redirect("/forgot", code=302)
