"""Découpe le texte en chunks avec overlap."""

from app.config import get_settings


def clean_text(text: str) -> str:
    t = text.replace("\u0000", "").replace("\r\n", "\n")
    while "\n\n\n" in t:
        t = t.replace("\n\n\n", "\n\n")
    return t.strip()


def chunk_text(text: str) -> list[str]:
    settings = get_settings()
    size = settings.chunk_size
    overlap = settings.chunk_overlap

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    buffer = ""

    for para in paragraphs:
        candidate = f"{buffer}\n\n{para}" if buffer else para

        if len(candidate) <= size:
            buffer = candidate
            continue

        if buffer:
            chunks.append(buffer)

        if len(para) > size:
            i = 0
            while i < len(para):
                end = min(i + size, len(para))
                chunks.append(para[i:end])
                i = end - overlap if end < len(para) else end
            buffer = ""
        else:
            buffer = para

    if buffer:
        chunks.append(buffer)

    return [c.strip() for c in chunks if len(c.strip()) > 30]
