# Security Controls Implemented

This file maps implemented security controls to the Capisso DEW cloud security prototype.

---

## Stage 1: Secure Upload Initiation

### Endpoint

`POST /upload/initiate`

### Previous State

The initial `/upload` endpoint accepted metadata, validated basic fields, generated a UUID `jobId`, and returned status `received`.

### Improved Security Posture

The upload flow has been upgraded to generate a controlled S3 pre-signed upload URL. The uploaded document is stored directly in encrypted S3 object storage under a structured `raw/` prefix.

---

## Implemented Controls

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

## AWS Configuration Evidence

| AWS Area | Required Evidence |
|---|---|
| S3 bucket | Dedicated bucket exists for document storage |
| S3 prefixes | `raw/`, `processed/`, `rejected/`, `audit-artifacts/` |
| S3 public access | Block Public Access enabled |
| S3 encryption | Default encryption enabled |
| Lambda environment variables | `BUCKET_NAME`, `UPLOAD_PREFIX`, `MAX_FILE_SIZE_BYTES`, `ALLOWED_ORIGINS`, `PRESIGNED_URL_EXPIRES_SECONDS` |
| IAM | Inline policy restricts Lambda to S3 object upload on the raw prefix |
| CloudWatch | Upload initiation logs contain trace IDs and no raw document data |

---

## FRD SEC Mapping

| FRD Security Requirement | Current Coverage |
|---|---|
| SEC-001 | Encrypted object storage and traceable upload activity |
| SEC-002 | S3 storage hardening through encryption and public access blocking |
| SEC-003 | Initial least-privilege IAM policy for upload Lambda |
| SEC-004 | Safe CloudWatch security-relevant logging |
| SEC-005 | No raw PII or document content logged |
| SEC-006 | File type validation, file size validation, CORS control, and secure API boundary |


## Stage 3: Event-Driven Pre-processing Security Controls

### Architecture

```text
S3 ObjectCreated event
→ SQS queue
→ Pre-processing Lambda
→ Supabase status/audit update
```
Implemented Controls

| Security Area           | Implemented Control                                                  | Reason                                                                          |
| ----------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------|              
| Event-driven processing | S3 upload events trigger SQS messages                                | Starts processing automatically after upload                                    |
| Queue buffering         | SQS queue receives upload events                                     | Prevents processing events from being lost ifLambda is temporarily unavailable  |
| Failure handling        | DLQ stores repeatedly failed messages                                | Supports investigation and graceful failure handling                            |
| Least privilege         | Pre-processing Lambda has scoped S3, SQS, and CloudWatch permissions | Reduces blast radius                                                            |
| Prefix isolation        | S3 event notification is limited to `raw/`                           | Prevents processed/rejected artifacts from re-triggering this stage             |
| Safe logging            | CloudWatch logs metadata only                                        | Prevents leakage of document contents or PII                                    |
| Audit logging           | Supabase audit logs record upload and pre-processing events          | Supports traceability and compliance evidence                                   |
| Status tracking         | Supabase document status is updated across pipeline stages           | Enables lifecycle governance                                                    |


FRD Security Mapping
| FRD Security Requirement | Stage 3 Coverage                                             |
| ------------------------ | ------------------------------------------------------------ |
| SEC-001                  | Adds traceable processing activity and audit evidence        |
| SEC-002                  | Maintains protected storage workflow through S3 raw prefix   |
| SEC-003                  | Adds function-specific least-privilege access                |
| SEC-004                  | Adds pre-processing event logs and processing status records |
| SEC-005                  | Avoids logging raw document contents or extracted PII        |
| SEC-006                  | Supports controlled backend processing after secure upload   |

