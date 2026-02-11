# RAG PDF API

API RAG (Retrieval-Augmented Generation) en FastAPI pour indexer des PDFs et répondre à des questions sur leur contenu.

## 🚀 Fonctionnalités

- **Extraction de texte** : Extraction automatique du texte depuis des PDFs avec `pdfplumber`
- **Découpage intelligent** : Découpage en chunks de ~1000 caractères avec overlap de 150 caractères
- **Embeddings** : Génération d'embeddings via OpenAI `text-embedding-ada-002`
- **Stockage vectoriel** : Stockage dans Supabase (PostgreSQL + pgvector)
- **Recherche sémantique** : Recherche par similarité cosinus
- **Génération de réponses** : Réponses contextuelles via GPT-4o-mini

## 📋 Prérequis

- Python 3.11+
- Docker et Docker Compose
- Compte OpenAI avec clé API
- Projet Supabase avec pgvector activé

## 🛠️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-username/rag-pdf.git
cd rag-pdf
```

### 2. Configuration

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et remplir les variables :
# - OPENAI_API_KEY
# - SUPABASE_URL
# - SUPABASE_KEY
# - SUPABASE_SERVICE_KEY
```

### 3. Initialiser Supabase

1. Aller dans Supabase → SQL Editor
2. Exécuter le contenu de `sql/setup.sql`
3. Vérifier que l'extension `vector` est activée

### 4. Démarrer l'API

```bash
docker compose up
```

L'API sera disponible sur http://localhost:8000

## 📚 Documentation API

Une fois l'API démarrée, accédez à la documentation Swagger :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔌 Endpoints

### Health Check
```bash
GET /health
```

### Indexation PDF (base64)
```bash
POST /ingest/pdf
Content-Type: application/json

{
  "user_id": "user1",
  "pdf_base64": "JVBERi0...",
  "file_name": "document.pdf"
}
```

### Indexation PDF (upload)
```bash
POST /ingest/upload
Content-Type: multipart/form-data

user_id: user1
file: @document.pdf
```

### Chat / Question
```bash
POST /chat
Content-Type: application/json

{
  "user_id": "user1",
  "question": "De quoi parle le document ?"
}
```

## 🏗️ Structure du projet

```
rag-pdf/
├── app/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Configuration depuis .env
│   ├── models/
│   │   └── schemas.py       # Schémas Pydantic
│   ├── routers/
│   │   ├── ingest.py        # Routes d'indexation
│   │   └── chat.py           # Route de chat
│   └── services/
│       ├── extractor.py     # Extraction PDF
│       ├── chunker.py       # Découpage en chunks
│       ├── embeddings.py    # Génération d'embeddings
│       ├── vectorstore.py   # Stockage Supabase
│       └── llm.py           # Génération de réponses
├── sql/
│   └── setup.sql            # Script SQL Supabase
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## 🔧 Stack technique

- **Framework** : FastAPI (Python 3.11)
- **PDF** : pdfplumber
- **Embeddings** : OpenAI text-embedding-ada-002 (1536 dimensions)
- **LLM** : OpenAI GPT-4o-mini
- **Vector Store** : Supabase (PostgreSQL + pgvector)
- **HTTP Client** : httpx (async)
- **Config** : pydantic-settings

## 📝 Variables d'environnement

| Variable | Description | Exemple |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Clé API OpenAI | `sk-proj-...` |
| `EMBEDDING_MODEL` | Modèle d'embedding | `text-embedding-ada-002` |
| `CHAT_MODEL` | Modèle de chat | `gpt-4o-mini` |
| `SUPABASE_URL` | URL du projet Supabase | `https://xxx.supabase.co` |
| `SUPABASE_KEY` | Clé anonyme Supabase | `eyJhbGci...` |
| `SUPABASE_SERVICE_KEY` | Clé service Supabase | `eyJhbGci...` |
| `CHUNK_SIZE` | Taille des chunks | `1000` |
| `CHUNK_OVERLAP` | Overlap entre chunks | `150` |
| `SEARCH_TOP_K` | Nombre de résultats | `5` |

## 🧪 Tests

```bash
# Tests de structure
python3 test_structure.py

# Tests du fichier .env.example
python3 test_env_example.py
```

## 🚢 Déploiement

### Docker

```bash
docker compose up -d
```

### Azure Container Apps

Le projet est prêt pour un déploiement sur Azure Container Apps. Voir la documentation Azure pour les détails.

## 📄 Licence

MIT

## 👤 Auteur

Votre nom

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

