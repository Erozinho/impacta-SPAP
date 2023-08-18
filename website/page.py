from flask import Blueprint, request, render_template, session
import db
import requests


# Se comunica com o bd e puxa o conselho da api
page = Blueprint('login', __name__, template_folder="template")


@page.route('/register', methods=['GET'])
def carregar():
    return render_template("registrar.html")

# @page.route('/register', methods=['POST'])
# def ver_resultado():
#     nome = request.form.get('nome')

#     select = f"SELECT Consellho from alunos WHERE Nome='{nome}'"
#     mycursor.execute(select)
#     tabela = mycursor.fetchone()
    
#     aluno_conselho = str(tabela[0])
        
#     conselhos = ("https://api.adviceslip.com/advice/")
#     response = requests.get(f"{conselhos+aluno_conselho}")

#     if response.status_code == 200:
#         print("sucesso na requisição")
#         a = response.json()
#         b = (a['slip']['advice'])
#         return f"Conselho do Aluno {nome} é {b}"
#     else:
#        return "ERRO"