from flask import Flask, jsonify
import feedparser
import json
import html
from utils import format_time, summarize

app = Flask(__name__)

# Carrega os feeds RSS
with open('feeds.json', 'r') as f:
    feeds = json.load(f)

# Palavras-chave por categoria (RJ + nacional para "brasil")
palavras_chave = {
    "ultimas": ["rio de janeiro", "estado do rio", "baixada fluminense", "niterói", "duque de caxias", "nova iguaçu"],
    "politica": ["governo do estado", "prefeitura", "prefeito", "vereador", "alerg", "palácio guanabara"],
    "seguranca": ["polícia civil", "polícia militar", "crime no rio", "delegacia", "miliciano", "facção"],
    "economia": ["comércio no rio", "emprego no rio", "inflação no estado", "investimentos no rio"],
    "cultura": ["evento no rio", "carnaval", "exposição", "museu", "teatro municipal", "maracanãzinho"],
    "esporte": ["flamengo", "vasco", "botafogo", "fluminense", "campeonato carioca"],
    "brasil": ["brasil", "governo federal", "congresso", "senado", "presidência", "lula", "bolsonaro"]
}

@app.route('/')
def home():
    return jsonify({'status': 'OK'})

@app.route('/news')
def get_news_geral():
    return filtrar_noticias()

@app.route('/news/<categoria>')
def get_news_por_categoria(categoria):
    return filtrar_noticias(categoria)

def filtrar_noticias(categoria=None):
    todas_noticias = []

    for fonte, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            count = 0

            for item in feed.entries:
                titulo = html.unescape(item.get('title', '').replace('<![CDATA[', '').replace(']]>', '')).strip()
                resumo = item.get('summary', '') or item.get('description', '')
                data = item.get('published') or item.get('pubDate') or item.get('updated') or getattr(item, 'published_parsed', '')

                texto = f"{titulo} {resumo}".lower()

                if categoria:
                    palavras = palavras_chave.get(categoria, [])
                else:
                    palavras = [p for chave in palavras_chave.values() for p in chave]

                if any(p in texto for p in palavras):
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
