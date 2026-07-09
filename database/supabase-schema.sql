create extension if not exists pgcrypto;

create table if not exists public.documents (
  id uuid primary key,
  user_id text not null,
  company_id text not null,
  file_name text not null,
  content_type text not null,
  file_size_bytes bigint not null check (file_size_bytes > 0),
  s3_bucket text not null,
  s3_object_key text not null unique,
  status text not null check (
    status in (
      'upload_url_created',
      'uploaded',
      'preprocessing_started',
      'preprocessing_failed',
      'preprocessing_completed',
      'ocr_started',
      'ocr_completed',
      'postprocessing_completed',
      'needs_human_review',
      'completed',
      'deleted',
      'failed'
    )
  ),
  trace_id text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.audit_logs (
  id uuid primary key default gen_random_uuid(),
  document_id uuid references public.documents(id) on delete set null,
  user_id text,
  company_id text,
  action text not null,
  resource text,
  result text not null,
  trace_id text,
  details jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_documents_user_id
on public.documents(user_id);

create index if not exists idx_documents_company_id
on public.documents(company_id);

create index if not exists idx_documents_status
on public.documents(status);

create index if not exists idx_audit_logs_document_id
on public.audit_logs(document_id);

create index if not exists idx_audit_logs_action
on public.audit_logs(action);

alter table public.documents enable row level security;
alter table public.audit_logs enable row level security;
