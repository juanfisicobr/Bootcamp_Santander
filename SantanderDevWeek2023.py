sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'
#Extract
#Extraia a lista de IDs de usuário a partir do arquivo CSV. Para cada ID, faça uma requisição GET para obter os dados do usuário correspondente.
import pandas as pd

df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

import requests
import json

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

#Transform
#Utilize a API do OpenAI GPT-4 para gerar uma mensagem de marketing personalizada para cada usuário.
openai_api_key = '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'
import openai

openai.api_key = openai_api_key

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em Mercado Financeiro."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre como aumentar o limite de crédito (máximo de 150 caracteres)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })

def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")

#[6010, 6012, 6013]
#[
#  {
#    "id": 6010,
#    "name": "Juan Teran",
#    "account": {
#      "id": 6360,
#      "number": "000999-1",
#      "agency": "00015-1",
#      "balance": 2500.0,
#      "limit": 1000.0
#    },
#    "card": {
#      "id": 5839,
#      "number": "**** **** 1256 *532",
#      "limit": 3000.0
#    },
#    "features": [
#      {
#        "id": 1791,
#        "icon": "string",
#        "description": "string"
#      }
#    ],
#    "news": [
#      {
#        "id": 11042,
#        "icon": "string",
#        "description": "string"
#      },
#      {
#        "id": 11045,
#        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
#        "description": "Ol\u00e1 Juan, para aumentar seu limite de cr\u00e9dito, mantenha suas contas em dia, aumente sua renda e atualize seus dados no banco."
#      }
#    ]
#  },
#  {
#    "id": 6012,
#    "name": "Selena Valentina",
#    "account": {
#      "id": 6362,
#      "number": "000999-2",
#      "agency": "00015-1",
#      "balance": 1500.0,
#      "limit": 500.0
#    },
#    "card": {
#      "id": 5840,
#      "number": "**** **** 7852 *5122",
#      "limit": 1000.0
#    },
#    "features": [
#      {
#        "id": 1792,
#        "icon": "string",
#        "description": "string"
#      }
#    ],
#    "news": [
#      {
#        "id": 11043,
#        "icon": "string",
#        "description": "string"
#      },
#      {
#        "id": 11046,
#        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
#        "description": "Oi Selena, para aumentar o limite de cr\u00e9dito, mantenha seu hist\u00f3rico de cr\u00e9dito limpo, pague contas em dia e aumente sua renda."
#      }
#    ]
#  },
#  {
#    "id": 6013,
#    "name": "Wilmer Medina",
#    "account": {
#      "id": 6363,
#      "number": "000999-3",
#      "agency": "00015-1",
#      "balance": 5500.0,
#      "limit": 2500.0
#    },
#    "card": {
#      "id": 5841,
#      "number": "**** **** 1111 *512",
#      "limit": 10000.0
#    },
#    "features": [
#      {
#        "id": 1793,
#        "icon": "string",
#        "description": "string"
#      }
#    ],
#    "news": [
#      {
#        "id": 11044,
#        "icon": "string",
#        "description": "string"
#      },
#      {
#        "id": 11047,
#        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
#        "description": "Ol\u00e1 Wilmer, para aumentar seu limite de cr\u00e9dito, mantenha pagamentos pontuais, reduza sua d\u00edvida existente e, ocasionamente, solicite uma revis\u00e3o ao seu banco."
#      }
#    ]
#  }
#]
#Ol� Juan, para aumentar seu limite de cr�dito, mantenha bons h�bitos financeiros: pague faturas em dia, evite d�vidas e aumente a renda. Sucesso!
#Ol� Selena, aumente seu limite de cr�dito melhorando seu hist�rico de cr�dito, mantendo baixos saldos e pagando contas em dia.
#Ol� Wilmer, aumente seu limite de cr�dito mantendo um bom hist�rico de cr�dito, pagando empr�stimos em dia e aumentando sua renda.
#User Juan Teran updated? True!
#User Selena Valentina updated? True!
#User Wilmer Medina updated? True!