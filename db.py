import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("impacta-SPAP/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


db = firestore.client()



# cred = db.collection("users").document("11111111111").get()
# print(cred.to_dict())

# testes

# cria uma nova documentação com id automatico
# dados = {'CPF':12345678910, 'SALDO': 12000, 'FATURA': 200}
# db.collection('contas').add(dados)

# doc_ref = db.collection("users").document("11111111111")

# doc = doc_ref.get()
# if doc.exists:
#     print(f"Dados do usuario: {doc.to_dict()}")
#     conta = db.collection("contas").document("11111111111").get()
#     print(f"Dados da conta: {conta.to_dict()}")

# else:
#     print("No such document!")
