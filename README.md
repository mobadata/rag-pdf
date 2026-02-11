# RAG PDF API

API FastAPI pour indexer des PDFs et répondre à des questions sur leur contenu.

## Installation

```bash
cp .env.example .env
# Remplir les variables dans .env
docker compose up
```

## Configuration

Variables d'environnement requises :
- `OPENAI_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_KEY`

## Initialisation Supabase

Exécuter `sql/setup.sql` dans Supabase SQL Editor.

## Endpoints

- `POST /ingest/pdf` - Indexer un PDF en base64
- `POST /ingest/upload` - Indexer un PDF via upload
- `POST /chat` - Poser une question
- `GET /health` - Health check

Documentation Swagger : http://localhost:8000/docs

## Stack

- FastAPI
- OpenAI (embeddings + GPT-4o-mini)
- Supabase (PostgreSQL + pgvector)
- pdfplumber

