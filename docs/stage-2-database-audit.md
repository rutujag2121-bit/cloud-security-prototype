# Stage 2: Supabase Document Metadata and Audit Logging

## Objective

Add persistent lifecycle tracking and audit logging to the secure upload initiation flow.

## Why This Stage Was Needed

The previous secure upload implementation generated a document ID, S3 object key, and pre-signed upload URL. However, the document metadata was not yet stored permanently. This meant the system could not reliably track document lifecycle state, user/company ownership, audit activity, or deletion later.

## Implemented Work

| Area | Implementation |
|---|---|
| Document metadata | Added `documents` table in Supabase |
| Audit trail | Added `audit_logs` table in Supabase |
| Upload Lambda | Updated Lambda to insert document metadata and audit event |
| Traceability | Stored `trace_id` in both database tables |
| Lifecycle state | Initial status set to `upload_url_created` |
| Security logging | Added `UPLOAD_INITIATED` audit action |

## Database Tables

| Table | Purpose |
|---|---|
| `documents` | Stores document ID, user ID, company ID, S3 object key, file metadata, lifecycle status, and trace ID |
| `audit_logs` | Stores security-relevant actions such as upload initiation, processing, review, access, and deletion |

## Security Value

| Security Requirement | Improvement |
|---|---|
| SEC-001 | Adds persistent audit evidence |
| SEC-003 | Prepares user/company-level data isolation |
| SEC-004 | Adds business-level security event logging |
| SEC-005 | Creates foundation for deletion and data access requests |
| SEC-006 | Supports secure API traceability |

## Evidence to Capture

- Supabase `documents` table created
- Supabase `audit_logs` table created
- Successful Lambda test response with database record confirmation
- `documents` row created after upload initiation
- `audit_logs` row created with `UPLOAD_INITIATED`
- CloudWatch log with `databaseWrite: completed`

## Status

Stage 2 creates the persistent database and audit foundation required for the later processing, HITL review, monitoring, and deletion stages.
