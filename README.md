# Chatbot RAG embutido — template estático

Chatbot que responde **apenas** com base nos seus 10 arquivos, 100% estático
(sirva no GitHub Pages, offline, ou em qualquer servidor — sem build de Node,
sem dependências no cliente).

## Estrutura

```
/
├── index.html           ← a página com o bot embutido (arquivo único)
├── knowledge.json       ← gerado a partir de docs/ (não editar à mão)
├── build_knowledge.py   ← converte PDF/DOCX/TXT/MD → knowledge.json
└── docs/                ← COLOQUE AQUI seus 10 arquivos
```

## Como usar (3 passos)

1. Copie seus 10 arquivos (PDF, DOCX, TXT ou MD) para a pasta `docs/`.
2. Rode: `python3 build_knowledge.py`
   (requer `pip install pypdf python-docx` só para PDF/DOCX)
3. Publique tudo (index.html + knowledge.json) no GitHub Pages.

## Como o bot responde

- **Modo local (padrão)**: busca por palavras-chave nos pedaços dos documentos
  e exibe os trechos mais relevantes **com citação do arquivo de origem**.
  Funciona offline, sem chave nenhuma.
- **Modo LLM (opcional)**: informe o endpoint de um backend OpenAI-compatível
  (ex.: um Cloudflare Worker na frente do Hermes API Server) e o bot envia os
  trechos recuperados como contexto para gerar uma resposta redigida.
  O token é digitado em tempo de execução e fica só no localStorage do navegador.

## ⚠️ Segurança

**Nunca** coloque uma chave de API no código do index.html: página pública no
GitHub Pages significa chave pública. Use um proxy (Worker) que guarda a chave
no servidor. O template já vem preparado para isso (token opcional em runtime,
nunca embutido).

## Atualizar os documentos

Adicione/troque arquivos em `docs/` → rode `build_knowledge.py` novamente →
faça commit do novo `knowledge.json`. A página lê o JSON no carregamento.
