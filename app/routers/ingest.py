"""Routes d'indexation PDF."""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models.schemas import IngestPDFRequest, IngestResponse
from app.services import chunker, embeddings, vectorstore, extractor

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/pdf", response_model=IngestResponse)
async def ingest_pdf_base64(req: IngestPDFRequest):
    """
    Indexe un PDF envoyé en base64.
    
    Exemple curl :
      curl -X POST http://localhost:8000/ingest/pdf \
        -H "Content-Type: application/json" \
        -d '{"user_id": "user1", "pdf_base64": "JVBERi0...", "file_name": "doc.pdf"}'
    """
    # 1. Extraire le texte
    text = extractor.extract_text_from_base64(req.pdf_base64)
    if not text or len(text.strip()) < 30:
        raise HTTPException(400, "Aucun texte extrait du PDF")

    # 2. Nettoyer + chunker
    cleaned = chunker.clean_text(text)
    chunks = chunker.chunk_text(cleaned)
    if not chunks:
        raise HTTPException(400, "Texte trop court après découpage")

    # 3. Embeddings
    embs = await embeddings.embed_texts(chunks)

    # 4. Stocker
    count = await vectorstore.store(
        user_id=req.user_id,
        chunks=chunks,
        embeddings=embs,
        source=req.file_name
    )

    return IngestResponse(
        success=True,
        chunks_count=count,
        user_id=req.user_id,
        file_name=req.file_name
    )


@router.post("/upload", response_model=IngestResponse)
async def ingest_pdf_upload(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Indexe un PDF uploadé en multipart (drag & drop, formulaire, Postman...).
    
    Exemple curl :
      curl -X POST http://localhost:8000/ingest/upload \
        -F "user_id=user1" \
        -F "file=@mon_document.pdf"
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Fichier PDF attendu")

    pdf_bytes = await file.read()
    if len(pdf_bytes) == 0:
        raise HTTPException(400, "Fichier vide")

    # 1. Extraire
    text = extractor.extract_text_from_bytes(pdf_bytes)
    if not text or len(text.strip()) < 30:
        raise HTTPException(400, "Aucun texte extrait du PDF")

    # 2. Chunker
    cleaned = chunker.clean_text(text)
    chunks = chunker.chunk_text(cleaned)
    if not chunks:
        raise HTTPException(400, "Texte trop court après découpage")

    # 3. Embeddings
    embs = await embeddings.embed_texts(chunks)

    # 4. Stocker
    count = await vectorstore.store(
        user_id=user_id,
        chunks=chunks,
        embeddings=embs,
        source=file.filename
    )

    return IngestResponse(
        success=True,
        chunks_count=count,
        user_id=user_id,
        file_name=file.filename
    )
