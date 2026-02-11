# Guide de test - RAG PDF API

## Tests de structure

```bash
# Vérifier la structure du projet
python3 test_structure.py

# Vérifier le fichier .env.example
python3 test_env_example.py
```

## Tests avec Docker

### 1. Préparation

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et remplir les clés :
# - OPENAI_API_KEY
# - SUPABASE_URL
# - SUPABASE_KEY
# - SUPABASE_SERVICE_KEY
```

### 2. Initialiser Supabase

1. Aller dans Supabase → SQL Editor
2. Exécuter le contenu de `sql/setup.sql`
3. Vérifier que l'extension `vector` est activée

### 3. Démarrer l'API

```bash
# Démarrer avec Docker Compose
docker compose up

# L'API sera disponible sur http://localhost:8000
# Documentation Swagger : http://localhost:8000/docs
```

### 4. Tests manuels

#### Test de santé

```bash
curl http://localhost:8000/health
```

Résultat attendu :
```json
{"status": "ok"}
```

#### Test d'ingestion (base64)

```bash
# Encoder un PDF en base64
PDF_B64=$(base64 -i mon_document.pdf)

curl -X POST http://localhost:8000/ingest/pdf \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"test_user\",
    \"pdf_base64\": \"$PDF_B64\",
    \"file_name\": \"mon_document.pdf\"
  }"
```

Résultat attendu :
```json
{
  "success": true,
  "chunks_count": 5,
  "user_id": "test_user",
  "file_name": "mon_document.pdf"
}
```

#### Test d'ingestion (upload multipart)

```bash
curl -X POST http://localhost:8000/ingest/upload \
  -F "user_id=test_user" \
  -F "file=@mon_document.pdf"
```

#### Test de chat

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "question": "De quoi parle le document ?"
  }'
```

Résultat attendu :
```json
{
  "answer": "...",
  "sources_used": 5
}
```

## Tests automatisés (à venir)

Les tests unitaires et d'intégration peuvent être ajoutés avec `pytest` :

```bash
pip install pytest pytest-asyncio httpx
pytest tests/
```

## Vérifications

- ✅ Structure du projet complète
- ✅ Tous les fichiers Python ont une syntaxe valide
- ✅ .env.example contient toutes les variables
- ⏳ Tests d'intégration avec Docker
- ⏳ Tests unitaires des services

