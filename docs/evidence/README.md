# Evidence Folder

This folder tracks implementation and evaluation evidence for the cloud security prototype.

Screenshots should remain private unless cropped and sanitised. The public repository should contain evidence indexes rather than sensitive console dumps.

## Evidence Handling Rule

Do not commit:
- AWS access/secret keys
- Supabase service-role credentials
- `.env` files
- complete pre-signed URLs
- real financial documents or PII
- real JWTs or session tokens
- full AWS account identifiers where not required
- screenshots containing secrets, sensitive account configuration or personal email details
- raw logs containing sensitive data

## Stage Evidence Summary

| Stage | Evidence status | Examples retained privately |
|---|---|---|
| 1 Secure upload | Complete | Private/encrypted S3, IAM scope, valid/invalid upload tests, pre-signed PUT success |
| 2 Supabase metadata/audit | Complete | `documents`, `audit_logs`, trace-linked database writes |
| 3 Event-driven preprocessing | Complete | S3 event, SQS/DLQ, Lambda trigger, Supabase/CloudWatch updates |
| 4 Mock extraction | Complete | Extraction queue/DLQ, processing run, extraction result, lifecycle/audit evidence |
| 5A Real-service attempt | Complete as constraint evidence | Textract invocation boundary and `SubscriptionRequiredException` |
| 5B Secure model adapter design | Complete as design evidence | Nova Lite selection, IAM template, prompt, schema and test plan |
| 5C Validation/HITL | Complete | Valid, low-confidence, missing-field, financial-mismatch, prompt-injection and malformed-output scenarios |
| 6 Monitoring/incident response | Complete | Lambda/DLQ alarms, controlled failures, SNS notification, retry exhaustion, recovery/runbook |
| 7 Retention/secure deletion | Complete | Premature-deletion rejection, manual deletion, S3/database verification, retention scan, scheduler/DLQ |
| 8A Secrets Manager | Complete | Secret creation, exact-secret IAM, environment-secret removal, full-pipeline regression |
| 8B Tenant isolation | Complete | Initial cross-tenant failure, restrictive policy creation, cross-tenant PASS, least-privilege table access |
| 8C API abuse protection | Complete for throttling/telemetry | Throttling configuration, normal request, controlled burst with HTTP 429, 4XX metric/alarm configuration |

## Important Evaluation Evidence to Preserve

Keep both failure and remediation evidence where available. In particular:
- initial RLS cross-tenant failure and final zero-row pass;
- initial CloudWatch/SNS notification failure and successful remediation;
- retry-exhaustion path into extraction DLQ;
- secure-deletion success/verification evidence;
- retention-not-due rejection and expired-retention success;
- HTTP 429 burst-test output.

A failed security test that is diagnosed, remediated and retested is valuable evaluation evidence and should not be removed from the private evidence set.

## Model-Evaluation Limitation

The repository/evidence does not demonstrate successful real-model extraction accuracy. Deterministic Stage 5C scenarios evaluate security-control behaviour, not model accuracy.
