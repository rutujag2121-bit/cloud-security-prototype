# API Gateway Endpoints

## API Name

`document-processing-rest-api`

## Stage

`Dev`

---

## Endpoint 1: POST /upload

### Purpose

Initial prototype endpoint used to validate receipt/invoice upload metadata and create a UUID-based processing job.

### Current Status

This endpoint is retained as the first prototype version. The stronger design is now `POST /upload/initiate`, which creates a secure S3 upload destination.

---

## Endpoint 2: POST /upload/initiate

### Purpose

Creates a secure upload initiation flow for receipt/invoice documents. The endpoint validates upload metadata, creates a document ID, generates a structured S3 object key, and returns a pre-signed S3 PUT URL.

### Request Body

```json
{
  "fileName": "receipt1.pdf",
  "contentType": "application/pdf",
  "fileSizeBytes": 250000,
  "userId": "test-user-1",
  "companyId": "capisso-test"
}
```

### Successful Response

```json
{
  "message": "Secure upload URL created",
  "documentId": "generated-uuid",
  "jobId": "generated-uuid",
  "status": "upload_url_created",
  "bucket": "<S3_BUCKET_NAME>",
  "objectKey": "raw/capisso-test/test-user-1/generated-uuid/receipt1.pdf",
  "uploadUrl": "pre-signed-url-not-committed-to-github",
  "uploadMethod": "PUT",
  "requiredHeaders": {
    "Content-Type": "application/pdf"
  },
  "expiresInSeconds": 900,
  "traceId": "aws-request-id",
  "createdAt": "timestamp"
}
```

### Rejection Cases

| Case | Expected Response |
|---|---|
| Missing `fileName` | 400 error |
| Missing `contentType` | 400 error |
| Missing `fileSizeBytes` | 400 error |
| Unsupported file type | 400 error |
| File over 10 MB | 400 error |
| Extension/content-type mismatch | 400 error |
| Invalid JSON body | 400 error |

### Security Controls

| Control | Implementation |
|---|---|
| File type validation | Allows PDF, JPEG, and PNG only |
| File size validation | Rejects files over 10 MB |
| Filename protection | Sanitizes file names before object key creation |
| Upload destination control | Generates S3 object key under the `raw/` prefix |
| CORS | Uses allowed origins from Lambda environment variable |
| Traceability | Returns `documentId`, `jobId`, and `traceId` |
| PII-aware logging | Logs metadata only, not document contents |

### Upload Flow

```text
Client
→ POST /upload/initiate
→ API Gateway
→ Upload Lambda
→ Validate metadata
→ Generate documentId and S3 objectKey
→ Return pre-signed S3 PUT URL
→ Client uploads file directly to S3
```

### Important Note

Pre-signed URLs must not be committed to GitHub because they temporarily authorize uploads to S3.
