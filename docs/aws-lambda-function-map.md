# AWS Lambda Function Map

This document maps the active AWS Lambda functions to repository files, triggers, responsibilities and key security boundaries.

| AWS Lambda Function | Repository File | Trigger | Primary Responsibility | Security Boundary |
|---|---|---|---|---|
| `document-processing-upload-lambda` | `lambda/upload/lambda_function.py` | API Gateway `POST /upload` | Validates upload metadata, generates UUID identifiers and a short-lived S3 pre-signed PUT URL, and writes initial Supabase document/audit records | Input validation, private S3 destination, short-lived upload authority, Secrets Manager credential retrieval |
| `document-processing-preprocess-lambda` | `lambda/preprocess/lambda_function.py` | SQS `capisso-preprocess-queue` populated by S3 ObjectCreated events | Validates the uploaded S3 object and queues eligible documents for extraction | S3 raw-prefix validation, content-type validation, SQS buffering/DLQ, least-privilege S3/SQS access |
| `document-processing-extraction-lambda` | `lambda/extraction/lambda_function.py` | SQS `capisso-extraction-queue` | Creates extraction results and applies deterministic post-processing validation and HITL routing | SQS/DLQ isolation, schema/financial/confidence checks, prompt-injection indicators, review routing, Secrets Manager |
| `document-processing-deletion-lambda` | `lambda/deletion/lambda_function.py` | Controlled direct Lambda invocation | Executes manual or retention-authorised secure deletion | Exact S3 bucket/prefix validation, S3 deletion verification, database cleanup, audit minimisation, idempotent tombstone |
| `document-processing-retention-lambda` | `lambda/retention/lambda_function.py` | EventBridge Scheduler (`rate(1 day)`) or controlled manual test | Finds retention-enabled expired documents and delegates deletion | No direct destructive S3 permission, bounded scan, deletion delegation, scheduler DLQ/monitoring |

## Current Processing Flow

```text
Client / API test
→ API Gateway POST /upload
→ Upload Lambda
   ↘ AWS Secrets Manager (Supabase backend credential)
→ Pre-signed S3 PUT URL
→ Private S3 raw/ storage
→ S3 ObjectCreated
→ Pre-processing SQS + DLQ
→ Pre-processing Lambda
   ↘ AWS Secrets Manager
→ Extraction SQS + DLQ
→ Extraction Lambda
   ↘ AWS Secrets Manager
→ Post-processing validation
→ Supabase documents / processing_runs / extraction_results / review_tasks / audit_logs
→ CloudWatch structured logs and alarms
→ SNS security notifications
```

## Retention and Deletion Flow

```text
EventBridge Scheduler
→ Retention Lambda
   ↘ AWS Secrets Manager
→ Eligible expired document selection
→ Secure-deletion Lambda
   ↘ AWS Secrets Manager
→ S3 raw/ deletion and verification
→ Database cascade cleanup
→ Audit redaction/minimisation
→ Minimal deletion tombstone
```

## Access-Control Boundary

Authenticated tenant-facing Supabase reads are limited by RLS using JWT `app_metadata.company_id`. A mandatory restrictive policy prevents cross-tenant document visibility. Internal operational/security tables remain unavailable to the authenticated tenant role.

The trusted AWS backend uses a privileged server-side Supabase credential retrieved from AWS Secrets Manager. This credential must never be exposed to the client.
