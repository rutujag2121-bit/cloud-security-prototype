# API Gateway Endpoints

## API

- API name: `document-processing-rest-api`
- Stage: `Dev`
- Active prototype route: `POST /upload`

## POST /upload

### Purpose

Creates the secure upload-initiation flow for receipt/invoice documents. The endpoint validates upload metadata, creates a document identifier, builds a structured S3 object key, writes initial Supabase lifecycle/audit records and returns a short-lived pre-signed S3 PUT URL.

### Request Body

```json
{
  "fileName": "receipt1.pdf",
  "contentType": "application/pdf",
  "fileSizeBytes": 250000,
  "userId": "test-user",
  "companyId": "test-company"
}
```

`userId` and `companyId` are prototype request fields. Production identity should be derived from a verified authentication/authorization context rather than trusted directly from caller input.

### Successful Response Shape

```json
{
  "message": "Secure upload URL created",
  "documentId": "generated-uuid",
  "jobId": "generated-uuid",
  "status": "upload_url_created",
  "bucket": "<S3_BUCKET_NAME>",
  "objectKey": "raw/test-company/test-user/generated-uuid/receipt1.pdf",
  "uploadUrl": "<SHORT_LIVED_PRESIGNED_URL>",
  "uploadMethod": "PUT",
  "requiredHeaders": {
    "Content-Type": "application/pdf"
  },
  "expiresInSeconds": 900,
  "traceId": "request-trace-id",
  "createdAt": "timestamp"
}
```

Complete pre-signed URLs must never be committed to the public repository.

### Rejection Cases

| Case | Expected result |
|---|---|
| Missing required metadata | HTTP 400 |
| Invalid JSON | HTTP 400 |
| Unsupported content type | HTTP 400 |
| File size <= 0 | HTTP 400 |
| File over 10 MB | HTTP 400 |
| Extension/content-type mismatch | HTTP 400 |
| Excessive request burst | API Gateway may return HTTP 429 |

### Security Controls

| Control | Implementation |
|---|---|
| File validation | PDF/JPEG/PNG metadata only |
| File-size limit | 10 MB prototype limit |
| Filename sanitisation | Unsafe characters replaced |
| Controlled upload authority | Short-lived S3 PUT pre-signed URL |
| Private destination | Structured `raw/` S3 path |
| CORS | Configuration-driven allowed origins |
| Traceability | UUID document ID and request trace ID |
| Stage throttling | Prototype stage request-rate/burst limit |
| Method throttling | Stricter `POST /upload` limit |
| Abuse monitoring | API Gateway `4XXError` CloudWatch metric/alarm |

### Current Flow

```text
Client
→ POST /upload
→ API Gateway
→ Upload Lambda
→ validate request
→ obtain backend database credential from Secrets Manager
→ write initial Supabase document/audit record
→ create S3 object key
→ return short-lived pre-signed S3 PUT URL
→ client uploads directly to private S3
```

## Historical Route Note

Earlier repository documentation referred to `POST /upload/initiate` while the upload design was being upgraded. The current deployed/tested prototype route documented by the root README and Stage 8 work is `POST /upload`. Historical references are retained only in older progress material where they describe earlier development decisions.
