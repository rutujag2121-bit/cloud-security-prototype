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
