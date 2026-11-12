"""Servidor MCP: pesquisa na documentação do taskbot (RAG lexical com BM25)."""
import re
import unicodedata
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from rank_bm25 import BM25Okapi

DOCS_DIR = Path(__file__).parent / "docs"
mcp = FastMCP("taskbot-docs")

STOPWORDS = {
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "em", "no", "na",
    "que", "qual", "como", "para", "por", "um", "uma", "se", "nao", "onde",
}

def tokenize(text: str, remove_stopwords: bool = True) -> list[str]:
    # Separa as letras dos acentos e remove os sinais de acentuação.
    normalizado = unicodedata.normalize("NFD", text.lower())
    sem_acentos = "".join(c for c in normalizado if not unicodedata.combining(c))
    palavras = re.findall(r"\w+", sem_acentos)
    return [p for p in palavras if p not in STOPWORDS] if remove_stopwords else palavras

def load_chunks() -> list[dict]:
    """Parte cada ficheiro .md em chunks por título (#, ##, ###)."""
    chunks = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for part in re.split(r"(?m)^(?=#{1,3} )", text):
            if part.strip():
                chunks.append({"source": path.name, "text": part.strip()})
    return chunks

CHUNKS = load_chunks()
INDEX = BM25Okapi([tokenize(c["text"]) for c in CHUNKS]) if CHUNKS else None

@mcp.tool()
def search_docs(query: str, k: int = 3) -> str:
    """Pesquisa na documentação do taskbot e devolve os k trechos mais relevantes,
    com o ficheiro de origem. Usar para perguntas sobre decisões, formato de ficheiro,
    comandos da CLI e convenções do projeto."""
    if INDEX is None:
        return "Sem documentação indexada."
    scores = INDEX.get_scores(tokenize(query))
    top = sorted(range(len(CHUNKS)), key=lambda i: scores[i], reverse=True)[:k]
    out = [
        f"[fonte: {CHUNKS[i]['source']}]\n{CHUNKS[i]['text']}"
        for i in top
        if scores[i] > 0
    ]
    return "\n\n---\n\n".join(out) or "Nada relevante encontrado."

if __name__ == "__main__":
    mcp.run()  # transporte stdio — nunca uses print() aqui