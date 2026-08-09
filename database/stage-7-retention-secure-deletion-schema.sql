-- Stage 7: Retention and Secure Deletion

create extension if not exists pgcrypto;

alter table public.documents
add column if not exists retention_until timestamptz;

update public.documents
set retention_until = created_at + interval '30 days'
where retention_until is null;

alter table public.documents
alter column retention_until
set default (now() + interval '30 days');

alter table public.documents
alter column retention_until
set not null;

alter table public.documents
add column if not exists retention_policy text
not null default 'prototype-30-day';

create table if not exists public.deletion_requests (
    id uuid primary key default gen_random_uuid(),
    document_id uuid references public.documents(id) on delete set null,
    document_fingerprint text not null,
    request_type text not null check (request_type in ('manual','retention')),
    status text not null default 'requested'
        check (status in ('requested','in_progress','completed','failed')),
    reason text not null,
    s3_objects_deleted integer not null default 0 check (s3_objects_deleted >= 0),
    database_deleted boolean not null default false,
    audit_redacted boolean not null default false,
    trace_id text,
    error_code text,
    error_message text,
    requested_at timestamptz not null default now(),
    completed_at timestamptz
);

create index if not exists idx_documents_retention_until
on public.documents(retention_until);

create index if not exists idx_deletion_requests_document_id
on public.deletion_requests(document_id);

create index if not exists idx_deletion_requests_status
on public.deletion_requests(status);

create index if not exists idx_deletion_requests_requested_at
on public.deletion_requests(requested_at);

create unique index if not exists idx_deletion_requests_fingerprint_completed
on public.deletion_requests(document_fingerprint)
where status = 'completed';

alter table public.deletion_requests enable row level security;

alter table public.documents
add column if not exists retention_enforcement_enabled boolean;

update public.documents
set retention_enforcement_enabled = false
where retention_enforcement_enabled is null;

alter table public.documents
alter column retention_enforcement_enabled
set default true;

alter table public.documents
alter column retention_enforcement_enabled
set not null;

create index if not exists idx_documents_retention_enforcement
on public.documents(retention_until)
where retention_enforcement_enabled = true;
