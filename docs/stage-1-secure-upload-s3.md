# Stage 1: Secure Upload Upgrade — S3 Pre-signed URL Flow

## Status

**Completed and tested**

## Objective

Upgrade the Stage 0 metadata-only API prototype into a secure document-upload workflow using private Amazon S3 storage and short-lived pre-signed PUT URLs.

The design allows a client to upload a receipt or invoice directly to S3 without sending the file through the Lambda function.

## Why This Stage Was Needed

Stage 0 validated metadata and created a job identifier, but it did not provide a secure destination for the actual document.

Sending large files through Lambda would increase payload, latency and cost while coupling file transfer to application logic.

Stage 1 introduced:

```text
Validated upload initiation
→ controlled S3 object path
→ short-lived pre-signed PUT URL
→ direct client-to-S3 upload
```

## Secure Upload Architecture

```text
Client
→ POST /upload/initiate
→ Amazon API Gateway
→ Upload Lambda
→ Validate file metadata
→ Generate documentId and structured object key
→ Generate short-lived pre-signed S3 PUT URL
→ Client uploads the file directly to private S3 storage
```

## Implemented Work

| Area | Implementation |
|---|---|
| S3 storage | Created a dedicated document bucket |
| Storage prefixes | Added `raw/`, `processed/`, `rejected/` and `audit-artifacts/` |
| Public access | Enabled S3 Block Public Access |
| Encryption | Enabled default S3 server-side encryption |
| API endpoint | Added the stronger `POST /upload/initiate` flow |
| Object key | Structured keys by company ID, user ID, document ID and sanitized filename |
| Pre-signed URL | Generated a short-lived S3 PUT URL |
| Allowed content types | PDF, JPEG and PNG |
| Maximum size | Increased and enforced the limit at 10 MB |
| Extension validation | Required file extension to match the declared content type |
| Filename protection | Sanitized filenames before object-key creation |
| CORS | Replaced wildcard design with configurable allowed origins |
| IAM | Restricted upload Lambda access to the required S3 `raw/` prefix |
| Logging | Added structured metadata logs with trace IDs |
| Test coverage | Added valid and rejection test events |

## Upload Request

Example metadata request:

```json
{
  "fileName": "receipt1.pdf",
  "contentType": "application/pdf",
  "fileSizeBytes": 250000,
  "userId": "test-user-1",
  "companyId": "capisso-test"
}
```

## Successful Response

A valid request returns:

- `documentId`
- `jobId`
- `objectKey`
- `uploadUrl`
- `uploadMethod`
- Required `Content-Type` header
- URL expiry time
- `traceId`
- Initial status `upload_url_created`

The complete pre-signed URL is never committed to GitHub because it temporarily authorizes an upload.

## Validation Rules

| Validation | Expected behaviour |
|---|---|
| Missing file name | Reject with HTTP `400` |
| Missing content type | Reject with HTTP `400` |
| Missing file size | Reject with HTTP `400` |
| Unsupported content type | Reject with HTTP `400` |
| File larger than 10 MB | Reject with HTTP `400` |
| Extension/content-type mismatch | Reject with HTTP `400` |
| Invalid JSON | Reject with HTTP `400` |
| Valid PDF, JPEG or PNG metadata | Generate a pre-signed upload URL |

## Valid Upload Test

The valid upload flow was tested as follows:

```text
1. Invoke upload initiation
2. Receive documentId, objectKey and pre-signed URL
3. Send an HTTP PUT request
4. Set Content-Type to application/pdf
5. Send the PDF as the binary body
6. Receive 200 OK from S3
7. Confirm the file exists under the S3 raw/ prefix
```

The test confirmed:

- Upload initiation returned HTTP `201`.
- A UUID-based `documentId` was generated.
- A structured S3 object key was generated.
- A pre-signed S3 PUT URL was returned.
- The direct S3 upload returned `200 OK`.
- The file appeared in protected S3 storage.

## Rejection Tests

The following repository test events were used:

```text
test-events/invalid-file-type.json
test-events/oversized-file.json
test-events/extension-mismatch.json
```

All three cases returned the expected HTTP `400` response.

These tests confirmed that the Lambda does not create upload URLs for unsupported or inconsistent metadata.

## Security Value

| Security Control | Improvement |
|---|---|
| Private storage | S3 Block Public Access prevents public bucket access |
| Encryption at rest | Default server-side encryption protects stored objects |
| Least privilege | Upload Lambda can write only to the required `raw/` prefix |
| Temporary authorization | Pre-signed URL expires after a limited period |
| Controlled destination | Lambda determines the bucket and object key |
| Input validation | Unsupported types, excessive sizes and mismatches are rejected |
| Filename safety | Unsafe characters are replaced before storage |
| Tenant-oriented structure | Object paths contain company, user and document identifiers |
| CORS restriction | Allowed origins are configured rather than universally trusted |
| Safe logging | Logs contain metadata and trace IDs rather than document content |
| Evidence protection | Complete pre-signed URLs are excluded from GitHub |

## Limitations and Residual Risks

Stage 1 validates declared metadata but does not yet inspect the actual file signature or scan document contents for malware.

Additional limitations at this stage included:

- No persistent document lifecycle record.
- No business-level audit table.
- No automatic processing after upload.
- No duplicate-message or replay protection.
- No complete user authentication or tenant-authorisation layer.
- Pre-signed URLs must be protected as temporary bearer credentials.
- Client clocks, networks or test tools may affect upload reliability.

These limitations are addressed or evaluated in later stages rather than being hidden.

## Transition to Stage 2

Stage 1 created a secure upload destination but did not permanently store document ownership, lifecycle status or audit events.

Stage 2 therefore added:

```text
Supabase documents table
+ audit_logs table
+ persistent trace IDs
+ upload lifecycle evidence
```

## Outcome

Stage 1 transformed the initial prototype into a secure direct-upload workflow.

```text
Validated metadata
→ controlled object key
→ short-lived upload authorization
→ encrypted private S3 object
→ traceable document identifier
```

This established the storage and upload foundation for the later database, event-driven, extraction and security-validation stages.
