from pydantic import BaseModel


class IngestPDFRequest(BaseModel):
    user_id: str
    pdf_base64: str
    file_name: str = "upload.pdf"


class IngestResponse(BaseModel):
    success: bool
    chunks_count: int
    user_id: str
    file_name: str


class ChatRequest(BaseModel):
    user_id: str
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources_used: int
