"""Appel OpenAI Embeddings API."""

import httpx
from app.config import get_settings


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed une liste de textes par batch de 100."""
    settings = get_settings()
    if not texts:
        return []

    all_embs: list[list[float]] = []

    async with httpx.AsyncClient(timeout=60.0) as client:
        for i in range(0, len(texts), 100):
            batch = texts[i:i + 100]
            resp = await client.post(
                "https://api.openai.com/v1/embeddings",
                headers={"Authorization": f"Bearer {settings.openai_api_key}"},
                json={"model": settings.embedding_model, "input": batch}
            )
            resp.raise_for_status()
            all_embs.extend([d["embedding"] for d in resp.json()["data"]])

    return all_embs


async def embed_query(text: str) -> list[float]:
    """Embed une seule question."""
    return (await embed_texts([text]))[0]
