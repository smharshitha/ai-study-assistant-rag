"""Lexical RAG baseline with evidence-linked answers."""
import re
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Study Assistant RAG", version="0.1.0")

class Document(BaseModel):
    id: str
    text: str = Field(min_length=1, max_length=50000)

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    documents: list[Document] = Field(min_length=1, max_length=100)

def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    q = tokens(req.question)
    ranked = []
    for doc in req.documents:
        words = tokens(doc.text)
        score = len(q & words) / max(1, len(q))
        if score > 0:
            ranked.append((score, doc))
    ranked.sort(key=lambda x: x[0], reverse=True)
    if not ranked:
        return {"answer": "Not found in the supplied notes.", "sources": []}
    selected = ranked[:3]
    return {
        "answer": "Relevant excerpts from the supplied notes:\n" +
                  "\n".join(f"[{d.id}] {d.text[:1200]}" for _, d in selected),
        "sources": [{"id": d.id, "score": round(s, 3)} for s, d in selected],
        "note": "This baseline retrieves excerpts; it does not synthesize a model-generated answer."
    }
