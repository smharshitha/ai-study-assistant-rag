# AI Study Assistant — Retrieval-Augmented Generation

A reference design for asking questions about user-provided study notes. This starter demonstrates chunking and lexical retrieval with no external model dependency. It is intentionally explicit about evidence: when no chunk is relevant, it says the answer is not found in the supplied notes.

## Features
- Split notes into overlapping chunks.
- Retrieve relevant chunks using a simple word-overlap baseline.
- Return source chunk IDs so answers can be checked.
- Refuse to infer an answer when retrieval finds no evidence.

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Then POST JSON to `/ask`, e.g. `{"question":"What is pipelining?","documents":[{"id":"notes-1","text":"Pipelining overlaps instruction stages..."}]}`.

## Production extensions
Use a proper embedding model and vector database; persist documents and user access controls; add PDF parsing, citations with page/offsets, chat history, authentication, tests, and retrieval evaluation. The current lexical retriever is not a semantic vector database.

## Evaluation
Measure retrieval recall@k, grounded-answer accuracy, citation correctness, and abstention quality. Test paraphrases, missing-answer questions, conflicting notes, malformed PDFs, and prompt injection embedded in documents.
