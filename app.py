from flask import Flask, jsonify
import feedparser
import json
from utils import format_time, summarize

app = Flask(__name__)

# Carrega os feeds RSS
with open('feeds.json', 'r') as f:
    feeds = json.load(f)

# Palavras-chave organizadas por categorias (exemplo simplificado)
palavras_chave = {
    "ultimas": ["últimas", "notícias de hoje", "destaque", "atualizado"],
    "politica": ["política", "governo", "prefeito", "vereador", "eleição"],
    "seguranca": ["crime", "polícia", "homicídio", "assalto", "violência"],
    "economia": ["economia", "preço", "inflação", "comércio", "emprego"],
    "cultura": ["cultura", "arte", "evento", "show", "exposição"],
    "entretenimento": ["tv", "novela", "famosos", "celebridade", "filme"],
    "esporte": ["futebol", "jogo", "partida", "flamengo", "vasco"],
    "rio": ["rio de janeiro", "niterói", "baixada fluminense", "duque de caxias"]
}

@app.route('/')
def home():
    return jsonify({'status': 'OK'})

@app.route('/news')
def get_news():
    todas_noticias = []

    for fonte, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            count = 0

            for item in feed.entries:
                titulo = item.get('title', '')
                resumo = item.get('summary', '')
                data = item.get('published', '')

                texto = f"{titulo} {resumo}".lower()

                if any(palavra in texto for chave in palavras_chave.values() for palavra in chave):
                    if count < 3:
                        todas_noticias.append({
                            "titulo": titulo,
                            "link": item.get('link'),
                            "resumo": summarize(resumo),
                            "data": format_time(data),
                            "fonte": fonte
                        })
                        count += 1
        except Exception as e:
            print(f"Erro com {fonte}: {str(e)}")

    return jsonify(todas_noticias[:25])
