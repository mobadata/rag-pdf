"""Insert et recherche sémantique dans Supabase (pgvector)."""

import json
import httpx
from app.config import get_settings


async def store(
    user_id: str,
    chunks: list[str],
    embeddings: list[list[float]],
    source: str = ""
) -> int:
    """Insère les chunks + embeddings dans la table documents."""
    settings = get_settings()

    rows = [
        {
            "content": chunk,
            "embedding": emb,
            "user_id": user_id,
            "metadata": json.dumps({
                "source": source,
                "chunk_index": i,
                "chunks_total": len(chunks),
            })
        }
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings))
    ]

    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        for i in range(0, len(rows), 50):
            resp = await client.post(
                f"{settings.supabase_url}/rest/v1/documents",
                headers=headers,
                json=rows[i:i + 50]
            )
            if resp.status_code == 404:
                raise Exception(
                    "Table 'documents' introuvable dans Supabase. "
                    "Veuillez exécuter le script sql/setup.sql dans Supabase → SQL Editor."
                )
            resp.raise_for_status()

    return len(rows)


async def search(
    user_id: str,
    query_embedding: list[float],
    top_k: int | None = None
) -> list[dict]:
    """Recherche les chunks les plus similaires via distance cosinus."""
    settings = get_settings()

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(
            f"{settings.supabase_url}/rest/v1/rpc/match_documents",
            headers={
                "apikey": settings.supabase_key,
                "Authorization": f"Bearer {settings.supabase_key}",
                "Content-Type": "application/json",
            },
            json={
                "query_embedding": query_embedding,
                "match_count": top_k or settings.search_top_k,
                "filter_user_id": user_id,
            }
        )
        if resp.status_code == 404:
            raise Exception(
                "Fonction 'match_documents' introuvable dans Supabase. "
                "Veuillez exécuter le script sql/setup.sql dans Supabase → SQL Editor."
            )
        resp.raise_for_status()
        return resp.json()
