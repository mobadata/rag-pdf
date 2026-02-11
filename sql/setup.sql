-- Exécuter UNE FOIS dans Supabase → SQL Editor → New Query → Run

-- 1. Activer pgvector
create extension if not exists vector;

-- 2. Table documents
create table if not exists documents (
    id         uuid default gen_random_uuid() primary key,
    content    text not null,
    embedding  vector(1536),
    user_id    text not null,
    metadata   jsonb default '{}',
    created_at timestamptz default now()
);

-- 3. Index recherche vectorielle
create index if not exists documents_embedding_idx
    on documents using ivfflat (embedding vector_cosine_ops)
    with (lists = 100);

create index if not exists documents_user_id_idx
    on documents (user_id);

-- 4. Fonction de recherche sémantique
create or replace function match_documents(
    query_embedding vector(1536),
    match_count int default 5,
    filter_user_id text default null
)
returns table (
    id         uuid,
    content    text,
    metadata   jsonb,
    similarity float
)
language plpgsql
as $$
begin
    return query
        select
            d.id,
            d.content,
            d.metadata,
            1 - (d.embedding <=> query_embedding) as similarity
        from documents d
        where (filter_user_id is null or d.user_id = filter_user_id)
        order by d.embedding <=> query_embedding
        limit match_count;
end;
$$;
