# Security Controls Implemented

This file maps implemented security controls to the Capisso DEW cloud security prototype.

---

## Stage 1: Secure Upload Initiation

### Endpoint

`POST /upload/initiate`

### Previous State

The initial `/upload` endpoint accepted metadata, validated basic fields, generated a UUID `jobId`, and returned status `received`.

### Improved Security Posture

The upload flow was upgraded to generate a controlled S3 pre-signed upload URL. The uploaded document is stored directly in encrypted S3 object storage under a structured `raw/` prefix.

### Implemented Controls

| Security Area | Implemented Control | Reason |
|---|---|---|
| Input validation | Requires `fileName`, `contentType`, and `fileSizeBytes` | Prevents malformed upload requests |
| File type restriction | Allows only PDF, JPEG, and PNG | Reduces malicious or unsupported file risk |
| File size control | Rejects files over 10 MB | Prevents oversized uploads and resource abuse |
| Filename sanitization | Removes unsafe filename characters | Reduces object-key and filename abuse |
| Object storage | Uses S3 for uploaded document storage | Separates permanent file storage from Lambda execution |
| Storage prefixing | Uses `raw/{companyId}/{userId}/{documentId}/{fileName}` | Supports lifecycle tracking and tenant separation |
| Least privilege | Upload Lambda role requires only S3 upload access to the raw prefix | Reduces blast radius |
| CORS control | Allowed origins configured through environment variable | Replaces wildcard origin design |
| Safe logging | Logs trace ID, document ID, status, content type, and file size only | Avoids PII and document-content leakage |
| Traceability | Returns `documentId`, `jobId`, `objectKey`, and `traceId` | Supports audit and debugging |

---

## Stage 2: Supabase Metadata and Audit Logging

### Purpose

Stage 2 adds persistent document metadata and audit logging. This ensures that the system does not only return a temporary upload response, but also records document lifecycle state and security-relevant events.

### Implemented Controls

| Security Area | Implemented Control | Reason |
|---|---|---|
| Metadata tracking | Supabase `documents` table stores document ID, owner/context, file metadata, S3 location, status, and trace ID | Enables lifecycle governance |
| Audit logging | Supabase `audit_logs` table stores actions such as `UPLOAD_INITIATED` | Supports compliance and incident review |
| Traceability | `trace_id` is stored in both documents and audit logs | Connects API, Lambda, CloudWatch, and database evidence |
| Data ownership preparation | `user_id` and `company_id` are stored with each document | Prepares for user/company isolation |
| Backend-only key use | Supabase service role key is stored only as a Lambda environment variable | Prevents exposing privileged DB access in GitHub/frontend |
| Lifecycle status | Initial document status is `upload_url_created` | Creates a controlled state transition model |

---

## Stage 3: Event-Driven Pre-processing

### Architecture

```text
S3 ObjectCreated event
→ SQS queue
→ Pre-processing Lambda
→ Supabase status/audit update
```
### Implemented Controls

| Security Area           | Implemented Control                                                  | Reason                                                                          |
| ----------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Event-driven processing | S3 upload events trigger SQS messages                                | Starts processing automatically after upload                                    |
| Queue buffering         | SQS queue receives upload events                                     | Prevents processing events from being lost if Lambda is temporarily unavailable |
| Failure handling        | DLQ stores repeatedly failed messages                                | Supports investigation and graceful failure handling                            |
| Least privilege         | Pre-processing Lambda has scoped S3, SQS, and CloudWatch permissions | Reduces blast radius                                                            |
| Prefix isolation        | S3 event notification is limited to `raw/`                           | Prevents processed/rejected artifacts from re-triggering this stage             |
| Safe logging            | CloudWatch logs metadata only                                        | Prevents leakage of document contents or PII                                    |
| Audit logging           | Supabase audit logs record upload and pre-processing events          | Supports traceability and compliance evidence                                   |
| Status tracking         | Supabase document status is updated across pipeline stages           | Enables lifecycle governance                                                    |

## Stage 4: Mock Extraction Security Controls

### Architecture

```text
Extraction SQS queue
→ Extraction Lambda
→ Supabase processing_runs
→ Supabase extraction_results
→ Supabase audit_logs
```
