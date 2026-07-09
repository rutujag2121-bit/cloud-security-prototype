# Security Controls Implemented

## POST /upload Lambda

Implemented controls:
- Accepts only approved file types: PDF, JPEG, PNG.
- Rejects unsupported content types.
- Enforces file size limit.
- Validates filename using a safe character pattern.
- Generates UUID-based `jobId` for traceability.
- Returns structured error responses.
- Includes CORS headers for frontend compatibility.

Security improvements planned:
- Replace wildcard CORS origin with production frontend domain.
- Add Supabase Auth / JWT validation.
- Store metadata in Supabase PostgreSQL.
- Add audit logging for upload events.
- Add rate limiting in API Gateway.
- Add request validation model in API Gateway.

## Validation Evidence

| Validation Control | Evidence |
|---|---|
| Valid PDF upload initiation | Returned `201` and generated a pre-signed S3 PUT URL |
| S3 upload through pre-signed URL | Returned `200 OK` in Postman |
| Invalid file type rejection | Returned `400` |
| Oversized file rejection | Returned `400` |
| Extension/content-type mismatch rejection | Returned `400` |

The upload Lambda now enforces validation before generating an S3 upload URL. This prevents invalid upload attempts from reaching the storage layer.
