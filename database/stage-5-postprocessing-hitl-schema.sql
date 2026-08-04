-- Stage 5C: Post-processing validation and HITL workflow
--
-- This migration:
-- 1. Extends extraction_results with validation evidence.
-- 2. Creates the backend Human-in-the-Loop review_tasks table.
-- 3. Preserves existing extraction results.
-- 4. Enables Row Level Security on review_tasks.

create extension if not exists pgcrypto;

-- ================================================================
-- PART 1: Extend extraction_results
-- ================================================================

alter table public.extraction_results
add column if not exists schema_version text
not null default 'receipt-extraction-v1';

alter table public.extraction_results
add column if not exists validation_status text
not null default 'not_validated';

alter table public.extraction_results
add column if not exists validation_errors jsonb
not null default '[]'::jsonb;

alter table public.extraction_results
add column if not exists review_reasons jsonb
not null default '[]'::jsonb;

alter table public.extraction_results
add column if not exists validated_at timestamptz;

do $$
begin
    if not exists (
        select 1
        from pg_constraint
        where conname = 'extraction_results_validation_status_check'
    ) then
        alter table public.extraction_results
        add constraint extraction_results_validation_status_check
        check (
            validation_status in (
                'not_validated',
                'valid',
                'invalid',
                'review_required'
            )
        );
    end if;
end
$$;

do $$
begin
    if not exists (
        select 1
        from pg_constraint
        where conname = 'extraction_results_validation_errors_array_check'
    ) then
        alter table public.extraction_results
        add constraint extraction_results_validation_errors_array_check
        check (
            jsonb_typeof(validation_errors) = 'array'
        );
    end if;
end
$$;

do $$
begin
    if not exists (
        select 1
        from pg_constraint
        where conname = 'extraction_results_review_reasons_array_check'
    ) then
        alter table public.extraction_results
        add constraint extraction_results_review_reasons_array_check
        check (
            jsonb_typeof(review_reasons) = 'array'
        );
    end if;
end
$$;

-- ================================================================
-- PART 2: Create Human-in-the-Loop review tasks
-- ================================================================

create table if not exists public.review_tasks (
    id uuid primary key default gen_random_uuid(),

    document_id uuid not null
        references public.documents(id)
        on delete cascade,

    extraction_result_id uuid not null unique
        references public.extraction_results(id)
        on delete cascade,

    processing_run_id uuid not null
        references public.processing_runs(id)
        on delete cascade,

    company_id text not null,
    user_id text not null,

    status text not null default 'pending'
        check (
            status in (
                'pending',
                'in_review',
                'approved',
                'corrected',
                'rejected'
            )
        ),

    priority text not null default 'medium'
        check (
            priority in (
                'low',
                'medium',
                'high'
            )
        ),

    review_reasons jsonb not null default '[]'::jsonb
        check (
            jsonb_typeof(review_reasons) = 'array'
        ),

    validation_errors jsonb not null default '[]'::jsonb
        check (
            jsonb_typeof(validation_errors) = 'array'
        ),

    assigned_to text,
    reviewer_notes text,
    corrected_json jsonb,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    completed_at timestamptz
);

-- ================================================================
-- PART 3: Indexes
-- ================================================================

create index if not exists idx_review_tasks_document_id
on public.review_tasks(document_id);

create index if not exists idx_review_tasks_company_id
on public.review_tasks(company_id);

create index if not exists idx_review_tasks_status
on public.review_tasks(status);

create index if not exists idx_review_tasks_priority
on public.review_tasks(priority);

create index if not exists idx_review_tasks_created_at
on public.review_tasks(created_at);

-- ================================================================
-- PART 4: Row Level Security
-- ================================================================

alter table public.review_tasks enable row level security;
