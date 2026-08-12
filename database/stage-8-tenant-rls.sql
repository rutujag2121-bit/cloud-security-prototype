-- ================================================================
-- Stage 8B: Tenant Isolation and Row Level Security
-- ================================================================

alter table public.documents enable row level security;
alter table public.processing_runs enable row level security;
alter table public.extraction_results enable row level security;
alter table public.review_tasks enable row level security;
alter table public.audit_logs enable row level security;
alter table public.deletion_requests enable row level security;

-- Anonymous users receive no application-data access.
revoke all on table public.documents from anon;
revoke all on table public.processing_runs from anon;
revoke all on table public.extraction_results from anon;
revoke all on table public.review_tasks from anon;
revoke all on table public.audit_logs from anon;
revoke all on table public.deletion_requests from anon;

-- Start authenticated role from least privilege.
revoke all on table public.documents from authenticated;
revoke all on table public.processing_runs from authenticated;
revoke all on table public.extraction_results from authenticated;
revoke all on table public.review_tasks from authenticated;
revoke all on table public.audit_logs from authenticated;
revoke all on table public.deletion_requests from authenticated;

-- Tenant-facing reads only.
grant select on table public.documents to authenticated;
grant select on table public.extraction_results to authenticated;
grant select on table public.review_tasks to authenticated;

drop policy if exists tenant_select_documents on public.documents;
drop policy if exists tenant_select_extraction_results on public.extraction_results;
drop policy if exists tenant_select_review_tasks on public.review_tasks;
drop policy if exists enforce_document_tenant_isolation on public.documents;

create policy tenant_select_documents
on public.documents
for select
to authenticated
using (
    company_id =
    (
        select auth.jwt()
            -> 'app_metadata'
            ->> 'company_id'
    )
);

create policy tenant_select_extraction_results
on public.extraction_results
for select
to authenticated
using (
    exists (
        select 1
        from public.documents d
        where d.id = extraction_results.document_id
          and d.company_id =
              (
                  select auth.jwt()
                      -> 'app_metadata'
                      ->> 'company_id'
              )
    )
);

create policy tenant_select_review_tasks
on public.review_tasks
for select
to authenticated
using (
    company_id =
    (
        select auth.jwt()
            -> 'app_metadata'
            ->> 'company_id'
    )
);

-- Mandatory tenant boundary added after the first cross-tenant test exposed
-- a row through permissive policy interaction.
create policy enforce_document_tenant_isolation
on public.documents
as restrictive
for select
to authenticated
using (
    company_id =
    (
        select auth.jwt()
            -> 'app_metadata'
            ->> 'company_id'
    )
);
