# Security Risk Register

## 1. Purpose

This risk register tracks threats identified in the STRIDE threat model and records the security controls implemented through Stage 8.

The original inherent-risk scores are retained. **Residual-risk scores are intentionally marked for Stage 9 reassessment** where the control set has materially changed; this avoids presenting unvalidated numerical reductions as completed evaluation.

Risk score methodology:

```text
Risk score = Likelihood × Impact
```

Likelihood and impact use a 1–5 scale.

| Score | Risk level |
|---:|---|
| 1–4 | Low |
| 5–9 | Medium |
| 10–16 | High |
| 17–25 | Critical |

## 2. Updated Risk Register

| Risk ID | Threat | Risk description | Inherent score | Current controls after Stage 8 | Residual status / remaining treatment |
|---|---|---|---:|---|---|
| R-01 | T-01 | Caller may request upload authority under false identity/company context | 16 High | Metadata validation, structured IDs, private upload flow | **High-priority residual:** production authentication/JWT-derived API identity not implemented |
| R-02 | T-02 | Leaked pre-signed URL may be used before expiry | 12 High | Short expiry, fixed object key and content type | Reassess in Stage 9; consider authenticated-session binding/one-time semantics |
| R-03 | T-03 | Malicious/disguised file may reach downstream processing | 16 High | Extension, content type, size and post-upload content-type checks | **High residual:** add file-signature validation/malware scanning |
| R-04 | T-04 | API abuse may create cost/backlog | 12 High | Size limit, asynchronous queues, API Gateway stage/method throttling, 4XX monitoring | Reassess in Stage 9; WAF/quotas/authenticated abuse controls remain |
| R-05 | T-05 | S3 misconfiguration may expose sensitive documents | 10 High | Block Public Access, private bucket, server-side encryption, scoped IAM | Reassess in Stage 9; automated configuration compliance not implemented |
| R-06 | T-06 | Overprivileged/compromised Lambda role may access unrelated resources | 15 High | Separate execution roles, resource-scoped IAM, deletion privilege isolation, exact-secret access | Reassess in Stage 9; periodic/automated IAM review remains |
| R-07 | T-07 | Forged/replayed queue message may cause duplicate/incorrect processing | 12 High | Restricted SQS permissions, structured messages, document IDs, DLQ/retry control | Residual remains significant; stronger schema validation/idempotency/replay protection required |
| R-08 | T-09 | PII/credentials/temporary URLs may be exposed in logs | 15 High | Structured logging, no document-body/secret/pre-signed-URL logging by design, evidence sanitisation | Reassess in Stage 9; automated sensitive-log scanning absent |
| R-09 | T-10 | Supabase service-role credential compromise gives privileged DB access | 15 High | AWS Secrets Manager, exact-secret IAM, no plaintext Lambda env secret, GitHub exclusion | Reassess in Stage 9; rotation is manual and backend credential remains privileged |
| R-10 | T-11 | Incorrect RLS may expose one company to another | 15 High | Tenant RLS, least-privilege grants, anonymous revoke, mandatory restrictive document policy, cross-tenant test/retest | Reassess in Stage 9; end-to-end production auth/token governance remains |
| R-11 | T-12 | Prompt injection in document may manipulate model output | 16 High | Fixed prompt design, strict JSON schema, pattern indicators, high-priority HITL routing | High residual: real-model adversarial testing and broader defences deferred |
| R-12 | T-13 | Hallucinated/malformed financial values may be accepted | 20 Critical | Versioned schema, required/type/date/currency/financial checks, malformed-output handling, HITL | High residual until controls are evaluated with real-model output |
| R-13 | T-14 | Low-confidence result may bypass review | 12 High | Overall/field confidence thresholds, uncertainty fields, deterministic tests, review-task creation | Reassess with real-model confidence behaviour |
| R-14 | T-15 | Repeated queue failure may remain unnoticed or cause processing loss | 12 High | DLQs, retry limits, Lambda/DLQ alarms, SNS notification, retry-exhaustion test, runbook | Reassess in Stage 9; automated/idempotent replay not implemented |
| R-15 | T-16 | Data may be retained too long or deletion may be ineffective | 16 High | Retention metadata, safety flag, scheduled enforcement, dedicated deletion Lambda, S3 verification, cascade cleanup, audit minimisation, tombstone | Reassess in Stage 9; legal retention policy selection/S3 version handling remain |
| R-16 | T-17 | Secrets or sensitive evidence may be committed publicly | 15 High | `.gitignore`, placeholders, evidence sanitisation, repository review, managed secret storage | Reassess in Stage 9; Git history/secret-scanning review remains advisable |
| R-17 | T-18 | Security failures may continue without detection/response | 12 High | CloudWatch alarms, DLQ alarms, SNS email, API 4XX alarm, retention/scheduler alarms, runbook, controlled alarm tests | Reassess in Stage 9; production incident escalation/SIEM absent |

## 3. Controls Completed Since the Original Risk Register

The following earlier priority actions are now implemented:

- R-04: API Gateway throttling and abuse monitoring.
- R-09: managed secret storage through AWS Secrets Manager.
- R-10: tenant RLS plus restrictive cross-tenant boundary and retest.
- R-11/R-12/R-13: deterministic AI-output security validation and HITL routing.
- R-14: DLQ alarms, retry-exhaustion testing and replay runbook.
- R-15: retention enforcement and verified secure deletion.
- R-17: CloudWatch/SNS monitoring and incident-response evidence.

## 4. Priority Residual Risks for Stage 9

The formal Current/Target Profile should give particular attention to:
1. production API authentication and verified tenant identity;
2. file-signature validation/malware scanning;
3. real-model adversarial and accuracy/integrity evaluation;
4. message idempotency/replay protection;
5. automated secret rotation and configuration/IAM review;
6. WAF/stronger abuse controls;
7. formal incident escalation/recovery objectives;
8. S3 version-aware deletion and legally determined retention policy.

## 5. Evaluation Note

The final residual scores should be assigned in Stage 9 after the evidence matrix is completed. The paper should clearly distinguish inherent risk, implemented treatment, observed test results and remaining residual risk.
