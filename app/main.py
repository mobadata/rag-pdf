from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ingest, chat

app = FastAPI(title="RAG PDF API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # en prod : mettre les vrais domaines
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    """Page d'accueil avec les endpoints disponibles."""
    return {
        "message": "RAG PDF API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "ingest_pdf": "/ingest/pdf",
            "ingest_upload": "/ingest/upload",
            "chat": "/chat"
        }
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
