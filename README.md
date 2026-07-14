# Capisso DEW Cloud Security Prototype

This repository documents the development of a cloud security and serverless processing prototype for the Capisso.ai Document Extraction Workflow (DEW) system.

The project focuses on securing an AI-driven document processing pipeline for receipts and invoices. The implementation demonstrates secure upload initiation, encrypted cloud storage, metadata tracking, audit logging, event-driven pre-processing, and least-privilege access controls.

## Current Implementation

Implemented:

- AWS API Gateway REST API
- Initial `/upload` POST endpoint
- Secure upload initiation flow
- AWS Lambda upload handler
- Metadata validation for uploaded documents
- File type validation for PDF, JPEG, and PNG
- 10 MB file size validation
- Filename sanitization
- UUID-based document/job tracking
- S3 pre-signed upload URL generation
- Structured S3 object key under the `raw/` prefix
- S3 bucket with Block Public Access enabled
- S3 default server-side encryption enabled
- S3 prefixes for `raw/`, `processed/`, `rejected/`, and `audit-artifacts/`
- Supabase PostgreSQL document metadata table
- Supabase audit logging table
- Upload Lambda integration with Supabase metadata/audit records
- SQS preprocessing queue
- SQS dead-letter queue
- S3 ObjectCreated event notification for the `raw/` prefix
- Pre-processing Lambda triggered through SQS
- Supabase document status updates during pre-processing
- CloudWatch safe structured logging with trace IDs
- IAM policy templates for least-privilege upload and pre-processing functions
- Test events and implementation documentation

## Current Pipeline

```text
Client/API test event
- API Gateway
- Upload Lambda
- S3 pre-signed upload URL
- S3 raw document storage
- S3 ObjectCreated event
- SQS preprocessing queue
- Pre-processing Lambda
- Supabase status and audit updates
- CloudWatch trace logs
- Extraction SQS queue
- Extraction dead-letter queue
- Extraction Lambda triggered through SQS
- Supabase `processing_runs` table
- Supabase `extraction_results` table
- Mock structured receipt/invoice extraction
- Confidence score calculation
- `needs_human_review` flag for HITL readiness
- Extraction audit events
