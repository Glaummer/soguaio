from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import os

app = Flask(__name__)

API_KEY = "AIzaSyB0LcCXY31Kt3cH3p7bY__LbF5rXoVS4LY"
MODELO = "gemini-2.5-flash"

PERSONALIDADE = """Você é o SOGUAIO, um assistente de inteligência artificial especializado em análise de obras de arte, combate ao plágio artístico e proteção de direitos autorais.
Seu criador é Edmilson Celso Chaúque (Glaummer), estudante da Universidade Pedagógica de Maputo, Moçambique.
O nome SOGUAIO é uma homenagem ao avô do criador, Soguaio Fernando Chaúque.
Só se apresente se perguntarem seu nome ou criador.
Responda em português de Moçambique, de forma educada e profissional."""


def perguntar_gemini(pergunta):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent?key={API_KEY}"
    dados = {
        "contents": [{
            "parts": [{"text": f"{PERSONALIDADE}\n\nUSUÁRIO: {pergunta}\n\nSOGUAIO:"}]
        }]
    }
    req = urllib.request.Request(url, data=json.dumps(dados).encode('utf-8'), method='POST')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=30) as resposta:
            resultado = json.loads(resposta.read().decode('utf-8'))
            return resultado["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Erro: {str(e)}"


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat_resposta():
    dados = request.get_json()
    pergunta = dados.get('pergunta', '')
    if not pergunta:
        return jsonify({'resposta': 'Digite uma mensagem.'})
    resposta = perguntar_gemini(pergunta)
    return jsonify({'resposta': resposta})


if __name__ == '__main__':
    porta = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=porta)
