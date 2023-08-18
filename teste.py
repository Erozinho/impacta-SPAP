from db import db

dados = {}

nome = input("Insira seu nome\n")
senha = input("Insira sua senha\n")
cpf = input("Insira seu cpf\n")
dados['nome'] = nome
dados['cpf'] = cpf
dados['senha'] = senha

db.collection('users').document(dados['cpf']).set(dados)

