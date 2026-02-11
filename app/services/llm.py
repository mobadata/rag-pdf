"""Génération de réponse via OpenAI Chat API."""

import httpx
from app.config import get_settings

SYSTEM_PROMPT = """Tu es un assistant qui répond aux questions en utilisant 
UNIQUEMENT le contexte fourni. N'invente aucune information.
Si le contexte ne contient pas la réponse, dis-le clairement.
Réponds dans la langue de la question."""


async def generate_answer(question: str, context_chunks: list[str]) -> str:
    settings = get_settings()
    context = "\n\n---\n\n".join(context_chunks) if context_chunks else "(vide)"

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={
                "model": settings.chat_model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Contexte :\n{context}\n\n---\n\nQuestion : {question}"}
                ],
                "temperature": 0.2,
                "max_tokens": 1500,
            }
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
