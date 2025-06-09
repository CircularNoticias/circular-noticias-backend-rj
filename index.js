const express = require("express");
const Parser = require("rss-parser");
const moment = require("moment");
moment.locale("pt-br");

const app = express();
const port = 3000;

const parser = new Parser();

const feeds = {
  extra: "https://extra.globo.com/rss.xml",
  odia: "https://odia.ig.com.br/rss.xml",
  terra: "https://www.terra.com.br/rss",
  cartacapital: "https://www.cartacapital.com.br/feed/"
};

const categorias = {
  "ultimas": [
    "últimas notícias", "notícias de hoje", "resumo do dia", "notícias agora"
  ],
  "politica": [
    "política", "governo do estado", "assembleia legislativa", "eleições", "vereadores", "prefeitos"
  ],
  "seguranca": [
    "segurança pública", "polícia", "crime", "violência", "prisão", "assalto"
  ],
  "economia": [
    "economia", "comércio", "emprego", "indústria", "negócios"
  ],
  "ciencia": [
    "ciência", "pesquisa", "tecnologia", "descobertas"
  ],
  "cultura": [
    "cultura", "música", "arte", "exposição", "evento cultural"
  ],
  "tecnologia": [
    "tecnologia", "inovação", "aplicativo", "rede social"
  ],
  "comercio": [
    "comércio", "vendas", "lojas", "shopping", "varejo"
  ],
  "esporte": [
    "esporte", "futebol", "flamengo", "vasco", "botafogo", "fluminense"
  ],
  "entretenimento": [
    "entretenimento", "famosos", "tv", "cinema", "novela"
  ],
  "rio": [
    "capital do estado do rio", "baixada fluminense", "zona oeste", 
    "região sul fluminense", "niterói", "duque de caxias", 
    "são gonçalo", "nova iguaçu", "volta redonda", "angra dos reis"
  ]
};

const limitarResumo = (texto) => {
  const lim = 150;
  return texto.length <= lim ? texto : texto.slice(0, lim).trim() + "...";
};

const tempoRelativo = (data) => {
  return moment(data).fromNow();
};

app.get("/noticias", async (req, res) => {
  const noticias = [];

  for (const [fonte, url] of Object.entries(feeds)) {
    try {
      const feed = await parser.parseURL(url);
      let count = 0;

      for (const item of feed.items) {
        const titulo = item.title || "";
        const conteudo = item.contentSnippet || item.content || "";
        const data = item.isoDate || item.pubDate || new Date();

        const texto = `${titulo} ${conteudo}`.toLowerCase();

        const pertence = Object.entries(categorias).some(([cat, palavras]) =>
          palavras.some(p => texto.includes(p.toLowerCase()))
        );

        if (pertence && count < 3) {
          noticias.push({
            titulo: titulo,
            link: item.link,
            resumo: limitarResumo(conteudo),
            data: tempoRelativo(data),
            fonte: fonte
          });
          count++;
        }
      }
    } catch (e) {
      console.error(`Erro ao buscar feed de ${fonte}:`, e.message);
    }
  }

  noticias.sort((a, b) => new Date(b.data) - new Date(a.data));
  res.json(noticias.slice(0, 25));
});

app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
