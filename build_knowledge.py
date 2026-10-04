#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_knowledge.py — Gera knowledge.json a partir dos arquivos em ./docs/
Suporta: .pdf, .docx, .txt, .md
Uso:  python3 build_knowledge.py
Saída: knowledge.json (mesma pasta do index.html)
"""
import json, re, sys
from pathlib import Path

BASE = Path(__file__).parent
DOCS = BASE / "docs"
OUT = BASE / "knowledge.json"
CHUNK_SIZE = 900   # caracteres por pedaço
CHUNK_OVERLAP = 150

def read_pdf(p: Path) -> str:
    from pypdf import PdfReader
    r = PdfReader(str(p))
    return "\n".join((pg.extract_text() or "") for pg in r.pages)

def read_docx(p: Path) -> str:
    import docx
    d = docx.Document(str(p))
    return "\n".join(par.text for par in d.paragraphs)

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

READERS = {".pdf": read_pdf, ".docx": read_docx,
           ".txt": read_text, ".md": read_text}

def clean(t: str) -> str:
    t = re.sub(r"\r", "", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

def chunk_text(t: str):
    t = clean(t)
    chunks, i = [], 0
    while i < len(t):
        piece = t[i:i + CHUNK_SIZE]
        # tenta quebrar em fim de parágrafo/frase
        cut = max(piece.rfind("\n\n"), piece.rfind(". "))
        if cut > CHUNK_SIZE // 2 and i + CHUNK_SIZE < len(t):
            piece = piece[:cut + 1]
        chunks.append(piece.strip())
        i += max(len(piece) - CHUNK_OVERLAP, 1) if i + CHUNK_SIZE < len(t) else CHUNK_SIZE
    return [c for c in chunks if len(c) > 40]

def main():
    if not DOCS.exists():
        print("Crie a pasta docs/ e coloque seus arquivos lá."); sys.exit(1)
    kb, n_files, n_chunks = [], 0, 0
    for p in sorted(DOCS.iterdir()):
        ext = p.suffix.lower()
        if ext not in READERS or p.name.startswith("~$"):
            continue
        try:
            text = READERS[ext](p)
        except Exception as e:
            print(f"[ERRO] {p.name}: {e}"); continue
        chunks = chunk_text(text)
        if not chunks:
            print(f"[vazio] {p.name}"); continue
        kb.append({"name": p.name, "chunks": chunks})
        n_files += 1; n_chunks += len(chunks)
        print(f"[ok] {p.name}: {len(chunks)} pedaços")
    OUT.write_text(json.dumps(kb, ensure_ascii=False), encoding="utf-8")
    print(f"\n=> {OUT.name}: {n_files} arquivo(s), {n_chunks} pedaços. Pronto para publicar.")

if __name__ == "__main__":
    main()
