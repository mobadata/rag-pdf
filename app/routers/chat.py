"""Route question/réponse."""

from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services import embeddings, vectorstore, llm

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Pose une question → recherche dans les PDFs indexés → réponse.
    
    Exemple curl :
      curl -X POST http://localhost:8000/chat \
        -H "Content-Type: application/json" \
        -d '{"user_id": "user1", "question": "De quoi parle le document ?"}'
    """
    # 1. Embed la question
    query_emb = await embeddings.embed_query(req.question)

    # 2. Recherche sémantique
    results = await vectorstore.search(user_id=req.user_id, query_embedding=query_emb)

    if not results:
        return ChatResponse(
            answer="Je n'ai trouvé aucune information pertinente dans vos documents.",
            sources_used=0
        )

    # 3. Générer la réponse
    context = [r["content"] for r in results]
    answer = await llm.generate_answer(question=req.question, context_chunks=context)

    return ChatResponse(answer=answer, sources_used=len(context))
