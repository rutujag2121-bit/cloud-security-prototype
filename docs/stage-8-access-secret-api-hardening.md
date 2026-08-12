# Stage 8 — Access, Secret and API-Abuse Hardening

## Status
**Implemented and tested**

## 8A — Secrets Manager migration

The Supabase service-role credential was moved from Lambda environment variables into AWS Secrets Manager.

Secret:
```text
capisso/supabase/service-role
```

Each backend Lambda was granted only `secretsmanager:GetSecretValue` on the exact secret ARN.

Migrated functions:
- Upload Lambda
- Preprocessing Lambda
- Extraction Lambda
- Secure-deletion Lambda
- Retention Lambda

The plaintext `SUPABASE_SERVICE_ROLE_KEY` environment variable was removed after successful regression testing.

The Lambda code caches the retrieved secret in the warm execution environment rather than requesting it repeatedly within the same execution environment.

### Regression testing

The complete upload pipeline was retested after the migration:

```text
Upload Lambda
→ S3
→ Preprocessing SQS
→ Preprocessing Lambda
→ Extraction SQS
→ Extraction Lambda
→ Supabase
```

The test document reached `ocr_completed`, with one processing run and one extraction result.

A regional S3 presigned-URL issue was also identified during testing. The upload Lambda was hardened to create the S3 client with the correct region, Signature Version 4 and virtual-hosted addressing.

## 8B — Tenant-aware Supabase RLS

RLS and PostgreSQL grants were configured so that authenticated tenant-facing access is restricted to:
- Own-company document metadata
- Own-company extraction results
- Own-company review tasks

Direct authenticated access remains blocked for:
- `processing_runs`
- `audit_logs`
- `deletion_requests`

Anonymous application-data access is revoked.

Authorization uses `app_metadata.company_id` from the authenticated JWT.

### Security finding and remediation

The first cross-tenant test failed:
```text
Tenant A → Tenant B document
Result: visible
```

Investigation showed that a permissive policy interaction did not create a mandatory tenant boundary.

A `RESTRICTIVE` document policy was then added.

Retest:
```text
PASS - CROSS TENANT ACCESS BLOCKED
rows_visible = 0
```

This failure/remediation/retest sequence is retained as security-evaluation evidence.

## 8C — API abuse protection

API Gateway throttling was configured at stage and method level.

Controlled concurrent traffic produced an HTTP `429 Too Many Requests`, proving that excessive requests can be rejected at the API boundary.

The API Gateway `4XXError` metric was monitored in CloudWatch and an alarm was configured through the existing SNS security notification channel.

## Security value

Stage 8 provides:
- Managed backend-secret storage
- Least-privilege secret retrieval
- Removal of plaintext backend credentials from Lambda configuration
- Tenant-level database isolation
- Mandatory cross-tenant row restriction
- Least-privilege table exposure
- Anonymous-access denial
- API request throttling
- Abuse telemetry and alerting
- Regression testing after security changes

## Known limitations

- Supabase secret rotation is manual.
- Trusted backend service credentials retain elevated database access.
- Tenant identity is represented by JWT claims but a complete production authentication frontend is not implemented.
- API Gateway throttling is best-effort and is not complete DoS protection.
- AWS WAF is not implemented.
- Detailed per-method API Gateway metrics are not enabled.
