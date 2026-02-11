# PROMPT CURSOR — RAG PDF API

Colle ce prompt dans Cursor (Cmd+I ou Ctrl+I) pour qu'il comprenne le projet.

---

## Contexte

Ce projet est une API RAG (Retrieval-Augmented Generation) en FastAPI qui :
1. Reçoit des PDFs (en base64 via POST ou en upload multipart)
2. Extrait le texte avec pdfplumber
3. Découpe le texte en chunks de ~1000 caractères avec 150 chars d'overlap
4. Génère les embeddings via OpenAI text-embedding-ada-002
5. Stocke les chunks + embeddings dans Supabase (PostgreSQL + pgvector)
6. Permet de poser des questions : embed la question → recherche sémantique → envoie le contexte à GPT-4o-mini → retourne la réponse

## Stack technique

- **Framework** : FastAPI (Python 3.11)
- **PDF** : pdfplumber (extraction texte uniquement, pas d'OCR)
- **Embeddings** : OpenAI text-embedding-ada-002 (1536 dimensions)
- **LLM** : OpenAI GPT-4o-mini
- **Vector Store** : Supabase (PostgreSQL + pgvector)
- **HTTP client** : httpx (async)
- **Config** : pydantic-settings (.env)
- **Déploiement** : Docker → Azure Container Apps

## Structure du projet

```
rag-pdf/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── requirements.txt
├── sql/setup.sql                ← SQL à exécuter dans Supabase
├── app/
│   ├── main.py                  ← point d'entrée FastAPI
│   ├── config.py                ← settings depuis .env
│   ├── models/
│   │   └── schemas.py           ← Pydantic request/response
│   ├── routers/
│   │   ├── ingest.py            ← POST /ingest/pdf (base64) et /ingest/upload (multipart)
│   │   └── chat.py              ← POST /chat
│   └── services/
│       ├── chunker.py           ← découpe le texte en chunks
│       ├── embeddings.py        ← appel OpenAI embeddings API
│       ├── extractor.py         ← extraction texte PDF avec pdfplumber
│       ├── vectorstore.py       ← insert + recherche sémantique Supabase
│       └── llm.py               ← appel OpenAI chat completions
```

## Règles de code

- Les routes (routers/) ORCHESTRENT, elles ne contiennent pas de logique métier
- Les services (services/) font le travail, ils sont réutilisables et testables seuls
- Tout est async (httpx, pas requests)
- Les clés API sont dans .env, jamais en dur dans le code
- Les erreurs sont gérées avec HTTPException
- Pas d'OCR, pas de crawling web, juste du PDF → texte → chunks → embeddings → stockage

## Pour lancer

```bash
cp .env.example .env    # remplir les clés
docker compose up       # localhost:8000/docs
```
