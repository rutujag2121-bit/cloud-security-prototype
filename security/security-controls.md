# Security Controls Implemented

This document maps implemented security controls to the Capisso DEW cloud security prototype. It represents the implementation after Stage 8.

## Stage 1 — Secure Upload and API Boundary

Current endpoint: `POST /upload`

| Security Area | Implemented Control | Security Purpose |
|---|---|---|
| Input validation | Requires `fileName`, `contentType` and `fileSizeBytes` | Rejects malformed requests before upload authority is issued |
| File-type restriction | PDF, JPEG and PNG only | Reduces unsupported input |
| Size control | 10 MB prototype limit | Reduces resource-abuse exposure |
| Filename sanitisation | Unsafe filename characters are replaced | Reduces object-key/filename abuse |
| Pre-signed upload | Short-lived S3 PUT URL | Avoids proxying full files through Lambda |
| Structured object path | `raw/{companyId}/{userId}/{documentId}/{fileName}` | Supports lifecycle tracking and tenant context |
| CORS | Allowed origins are configuration-driven | Avoids wildcard CORS design |
| API throttling | Stage and stricter `POST /upload` method limits | Reduces excessive request bursts |
| Abuse telemetry | API Gateway `4XXError` metric and CloudWatch alarm | Provides detection evidence for client errors/throttling |

A controlled concurrent burst test produced HTTP `429 Too Many Requests`. API Gateway throttling is treated as best-effort protection, not complete DoS prevention.

## Stage 2 — Metadata, Audit and Backend Credential Handling

| Security Area | Implemented Control | Security Purpose |
|---|---|---|
| Metadata tracking | Supabase `documents` lifecycle record | Supports governance and traceability |
| Business audit | Supabase `audit_logs` | Supports investigation and lifecycle evidence |
| Distributed traceability | `trace_id` stored across technical/business records | Correlates pipeline activity |
| Managed secret storage | Supabase service-role credential stored in AWS Secrets Manager | Removes plaintext privileged credential from Lambda environment variables |
| Least-privilege secret retrieval | Each backend Lambda receives `GetSecretValue` only for the required secret | Reduces secret-access blast radius |

## Stage 3 — Event-Driven Pre-processing

| Security Area | Implemented Control | Security Purpose |
|---|---|---|
| Event-driven processing | S3 ObjectCreated → SQS → Lambda | Separates upload from processing |
| Queue buffering | Main preprocessing SQS queue | Absorbs temporary downstream failure |
| Failure isolation | Preprocessing DLQ with retry limit | Prevents silent message loss |
| S3 boundary check | Expected bucket and `raw/` object structure validated | Reduces unintended object processing |
| Post-upload validation | Stored object content type checked before extraction | Adds a second validation point |
| Least privilege | Scoped S3/SQS/Lambda execution permissions | Reduces blast radius |

## Stage 4 / 5 — Extraction, AI-Output Validation and HITL

| Security Area | Implemented Control | Security Purpose |
|---|---|---|
| Provider isolation | Extraction provider behind dedicated Lambda boundary | Allows model replacement without changing security pipeline |
| Queue isolation | Extraction SQS and DLQ | Failure/retry separation |
| Versioned schema | Deterministic extraction schema validation | Treats model output as untrusted |
| Required-field/type checks | Mandatory field and type validation | Prevents malformed output being accepted |
| Financial validation | Total/subtotal/tax and line-item consistency rules | Detects integrity anomalies |
| Date/currency validation | Format and value checks | Reduces invalid financial records |
| Confidence controls | Overall and field-level thresholds | Routes uncertain output away from automatic completion |
| Prompt-injection indicators | Pattern-based suspicious instruction detection | Escalates potentially manipulated content |
| HITL routing | Medium/high-priority `review_tasks` | Adds a human-review control for unsafe/uncertain results |
| Audit evidence | Validation status/errors/reasons persisted | Supports explainability and evaluation |

The deterministic mock adapter validates control behaviour and orchestration. It is not evidence of real-model extraction accuracy or comprehensive prompt-injection prevention.

## Stage 6 — Monitoring, Alerting and Incident Response

| Security Area | Implemented Control | Security Purpose |
|---|---|---|
| Lambda error alarms | Upload, preprocessing and extraction error alarms | Detects processing failures |
| DLQ alarms | Preprocessing/extraction visible-message alarms | Detects exhausted retries/poison messages |
| SNS notification | Confirmed email security-notification channel | Escalates alarm state |
| Retry-exhaustion test | Invalid extraction message forced through retries to DLQ | Validates failure path |
| Incident runbook | Investigation, replay decision and recovery guidance | Supports repeatable response |
| Trace logs | Structured CloudWatch trace IDs | Supports investigation |

A KMS-related SNS notification failure was discovered during testing, remediated for the prototype and retested successfully. SNS encryption remains disabled in the prototype and is documented as a residual limitation.

## Stage 7 — Retention and Secure Deletion

| Security Area | Implemented Control | Security Purpose |
|---|---|---|
| Retention metadata | `retention_until`, policy metadata and enforcement flag | Makes lifecycle policy explicit |
| Destructive-role isolation | Dedicated deletion Lambda | Separates destructive permissions |
| Prefix-scoped deletion | S3 deletion restricted to `raw/` | Limits destructive scope |
| Retention safety check | Deletion rejects future `retention_until` values | Prevents premature automatic deletion |
| S3 deletion verification | Object absence verified after delete | Provides stronger deletion evidence |
| Database cleanup | Processing/result/review data removed | Minimises retained sensitive data |
| Audit minimisation | Identifying audit metadata redacted | Balances audit evidence and privacy |
| Deletion tombstone | Minimal SHA-256 fingerprint/status record | Preserves non-content deletion evidence |
| Idempotency | Repeat completed deletion handled safely | Reduces duplicate-destructive behaviour |
| Scheduler | Daily EventBridge retention invocation | Automates prototype enforcement |
| Scheduler DLQ/alarm | Delivery failure monitoring | Detects automation failure |

The 30-day interval is a prototype configuration, not a universal GDPR retention period.

## Stage 8 — Access, Secrets and API-Abuse Hardening

| Security Area | Implemented Control | Security Purpose |
|---|---|---|
| Secrets Manager | Backend Supabase service-role credential moved out of Lambda env vars | Reduces credential exposure |
| Tenant RLS | Authenticated tenant reads constrained by `app_metadata.company_id` | Enforces company-level database isolation |
| Restrictive RLS boundary | Mandatory document tenant policy | Prevents permissive-policy interaction from bypassing tenant boundary |
| Least-privilege grants | Tenant role only receives required table reads | Reduces database exposure |
| Anonymous denial | Application-data privileges revoked from `anon` | Blocks unauthenticated database reads |
| API throttling | Stage and `/upload` method throttles | Reduces burst abuse |
| 4XX monitoring | API Gateway 4XX metric/alarm | Detects abnormal client/throttling activity |

The first cross-tenant test failed despite the existence of a tenant policy. A restrictive policy was introduced and the same test then passed with zero cross-tenant rows visible. The failure/remediation/retest sequence is retained as evaluation evidence.

## Logging and Privacy Notes

CloudWatch logs intentionally avoid document body content, secret values and complete pre-signed URLs. Technical identifiers such as trace IDs, document IDs and some object metadata may be logged for operational traceability. Supabase business audit records hold richer lifecycle metadata and are protected as backend data.

## Current Residual Limitations

- The API currently accepts prototype `userId`/`companyId` values rather than deriving them from a fully implemented production API authorizer.
- Secrets Manager rotation is manual.
- Trusted backend service credentials remain privileged.
- API Gateway throttling is best-effort; AWS WAF is not implemented.
- Malware scanning and file-signature verification are not implemented.
- SQS replay/idempotency protections are not comprehensive.
- Real-model adversarial testing and model accuracy evaluation remain deferred.
- The HITL backend exists, but a complete reviewer UI is outside prototype scope.
- The project does not claim complete GDPR compliance or production readiness.
