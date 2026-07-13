create table if not exists public.processing_runs (
  id uuid primary key default gen_random_uuid(),
  document_id uuid not null references public.documents(id) on delete cascade,
  provider text not null default 'mock',
  model_name text not null,
  model_version text not null,
  processing_method text not null check (
    processing_method in ('mock', 'single_pass', 'multi_pass', 'agentic')
  ),
  input_s3_object_key text not null,
  output_s3_object_key text,
  status text not null check (
    status in ('started', 'completed', 'failed')
  ),
  started_at timestamptz not null default now(),
  completed_at timestamptz,
  duration_ms integer,
  trace_id text,
  error_message text
);

create table if not exists public.extraction_results (
  id uuid primary key default gen_random_uuid(),
  document_id uuid not null references public.documents(id) on delete cascade,
  processing_run_id uuid not null references public.processing_runs(id) on delete cascade,
  extracted_json jsonb not null,
  supplier_name text,
  document_date text,
  currency text,
  total_amount numeric,
  confidence_overall numeric not null check (
    confidence_overall >= 0 and confidence_overall <= 1
  ),
  field_confidence jsonb not null default '{}'::jsonb,
  needs_human_review boolean not null default false,
  created_at timestamptz not null default now()
);

create index if not exists idx_processing_runs_document_id
on public.processing_runs(document_id);

create index if not exists idx_processing_runs_status
on public.processing_runs(status);

create index if not exists idx_extraction_results_document_id
on public.extraction_results(document_id);

create index if not exists idx_extraction_results_processing_run_id
on public.extraction_results(processing_run_id);

alter table public.processing_runs enable row level security;
alter table public.extraction_results enable row level security;
