# AWS Lambda Function Map

This document maps AWS Lambda functions to repository files, triggers, and pipeline responsibilities.

| AWS Lambda Function | Repository File | Trigger | Purpose | Status |
|---|---|---|---|---|
| `document-processing-upload-lambda` | `lambda/upload/lambda_function.py` | API Gateway `POST /upload` or `POST /upload/initiate` | Validates upload metadata, creates document ID, generates S3 pre-signed upload URL, and writes initial Supabase document/audit records | Active |
| `document-processing-preprocess-lambda` | `lambda/preprocess/lambda_function.py` | SQS queue `capisso-preprocess-queue` | Handles S3 ObjectCreated events, validates uploaded S3 object, updates Supabase document status, and writes pre-processing audit events | Active |

## Current Pipeline Flow

```text
Client/API test event
→ API Gateway
→ Upload Lambda
→ S3 pre-signed upload URL
→ Client uploads file to S3 raw/
→ S3 ObjectCreated event
→ SQS preprocessing queue
→ Pre-processing Lambda
→ Supabase status/audit updates
→ CloudWatch trace logs
