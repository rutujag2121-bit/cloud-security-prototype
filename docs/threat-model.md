# STRIDE Threat Model

## 1. Purpose

This document identifies cybersecurity threats affecting the AWS-based AI document-processing prototype and records the control state after Stage 8.

Lifecycle scope:

```text
Upload
→ Object storage
→ Pre-processing
→ Extraction
→ Post-processing validation
→ Result storage
→ Human review
→ Retention
→ Secure deletion
```

STRIDE categories: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service and Elevation of Privilege.

## 2. System Scope

- Amazon API Gateway
- Upload Lambda
- Amazon S3
- Preprocessing SQS/DLQ and Lambda
- Extraction SQS/DLQ and Lambda
- Designed Bedrock/SageMaker provider boundary
- Supabase PostgreSQL and RLS
- AWS Secrets Manager
- CloudWatch and SNS
- Human-review backend
- Retention Lambda
- EventBridge Scheduler and scheduler DLQ
- Secure-deletion Lambda
- GitHub repository

The frontend and a complete production authentication interface are outside the implemented prototype scope.

## 3. Security-Sensitive Assets

| Asset | Security importance |
|---|---|
| Receipt/invoice files | May contain PII, financial and confidential business data |
| Extracted financial fields | Integrity affects downstream financial processing |
| Supabase privileged credential | Provides elevated backend database authority |
| Tenant identity claims | Determine company-level database access |
| Lambda execution roles | Authorise S3/SQS/Secrets Manager/Lambda operations |
| Pre-signed URLs | Provide temporary upload authority |
| SQS messages | Drive asynchronous processing |
| Model prompt/schema/output | Affect AI-processing integrity |
| Audit/trace records | Support investigation and lifecycle evidence |
| Retention/deletion records | Demonstrate lifecycle enforcement |

## 4. Trust Boundaries

- **TB-01 User → API Gateway:** untrusted caller metadata enters the backend.
- **TB-02 API Gateway → Upload Lambda:** request crosses into trusted serverless code; production identity verification remains incomplete.
- **TB-03 Client → S3 pre-signed PUT:** temporary upload authority permits writing one controlled object.
- **TB-04 S3 → SQS:** storage event becomes an asynchronous processing message.
- **TB-05 SQS → Lambda:** queue content crosses into trusted preprocessing/extraction code.
- **TB-06 AWS Lambda → Secrets Manager:** backend function obtains privileged database credential.
- **TB-07 AWS Lambda → Supabase:** trusted backend writes operational/business records with elevated service credentials.
- **TB-08 Authenticated tenant → Supabase RLS:** JWT company claim determines tenant-visible rows.
- **TB-09 Extraction adapter → AI model:** untrusted document content and untrusted model output cross the model boundary.
- **TB-10 Automated processing → HITL:** unsafe/uncertain output is escalated for review.
- **TB-11 Scheduler → Retention → Deletion:** automated lifecycle decision crosses into destructive processing.

## 5. Threat Catalogue

| ID | STRIDE | Threat scenario | Implemented controls | Remaining gap |
|---|---|---|---|---|
| T-01 | Spoofing | Caller requests upload authority while claiming another identity/company | Validation, structured IDs, private upload flow | Production API authentication and verified JWT-derived identity |
| T-02 | Spoofing/Tampering | Leaked pre-signed URL is reused before expiry | Short expiry, fixed key/content type | No one-time-use/session binding |
| T-03 | Tampering | Disguised/malicious file reaches processing | Extension/MIME/size validation and post-upload content-type check | File-signature verification and malware scanning |
| T-04 | Denial of Service | Excessive upload-initiation traffic causes cost/backlog | 10 MB limit, SQS buffering, stage/method throttling, 4XX monitoring | WAF/stronger quotas/authenticated rate policy |
| T-05 | Information Disclosure | S3 is accidentally exposed | Block Public Access, private storage, encryption, scoped IAM | Automated configuration-compliance checking |
| T-06 | Elevation of Privilege | Lambda role is overprivileged/compromised | Separate roles, resource-scoped IAM, destructive-role isolation, exact-secret access | Automated/periodic IAM review |
| T-07 | Tampering/Spoofing | Queue message is forged/replayed | Restricted queue permissions, structured IDs, retry/DLQ | Stronger schema validation, replay detection and idempotency |
| T-08 | Repudiation | Processing action cannot be linked to evidence | Trace IDs, audit records, processing runs, CloudWatch | End-user authentication event evidence incomplete |
| T-09 | Information Disclosure | Logs expose PII/secrets/temporary URLs | Structured logging, no document body/secret/pre-signed URL by design | Automated sensitive-log scanning |
| T-10 | Elevation of Privilege/Disclosure | Supabase service credential is exposed/misused | Secrets Manager, exact-secret IAM, no plaintext env credential | Manual rotation; privileged backend credential remains high impact |
| T-11 | Information Disclosure | RLS exposes another company’s data | Tenant RLS, least-privilege grants, anonymous revoke, restrictive document policy; cross-tenant retest passed | Complete production authentication/token governance |
| T-12 | Tampering | Document prompt injection manipulates model behaviour | Fixed prompt/schema design, suspicious-pattern detection, high-priority HITL | Real-model adversarial testing and broader prompt-injection defence |
| T-13 | Tampering/Repudiation | Hallucinated/malformed financial output is accepted | Schema/field/date/currency/financial checks, malformed-output handling, HITL | Real-model validation still deferred |
| T-14 | Tampering | Low-confidence output bypasses review | Confidence thresholds, uncertainty handling, deterministic tests, review-task creation | Real-model threshold calibration |
| T-15 | Denial of Service | Poison/repeatedly failing messages cause backlog | DLQs, retry limits, alarms, SNS, retry-exhaustion test, runbook | Automated/idempotent replay |
| T-16 | Disclosure/Repudiation | Data remains beyond policy or cannot be deleted | Retention metadata, scheduler, dedicated deletion, verification, cleanup, audit minimisation, tombstone | Legal policy selection and S3 version-aware deletion |
| T-17 | Tampering/Disclosure | Sensitive material is committed publicly | `.gitignore`, placeholders, sanitised evidence policy, repository review | Historical secret scanning remains advisable |
| T-18 | Denial of Service/Repudiation | Failures occur without timely detection/response | Lambda/DLQ/API/retention alarms, SNS and incident runbook | Production incident escalation/SIEM |
| T-19 | Elevation of Privilege | Backend service credential bypasses tenant RLS if compromised | Server-side-only Secrets Manager storage and scoped retrieval | Architectural reliance on privileged backend credential |
| T-20 | Tampering | Incorrect automated retention/deletion decision destroys valid data | `retention_enforcement_enabled`, future-date rejection, delegated deletion | Formal legal-policy governance and stronger change control |

## 6. Key Evaluation Findings

Two findings are particularly important for the final paper:

1. **Tenant-isolation failure and remediation:** the first cross-tenant test exposed a row despite an existing tenant policy. A mandatory restrictive policy was added and the same test then passed with zero visible cross-tenant rows.
2. **Alerting configuration failure and remediation:** a controlled alarm test exposed an SNS/KMS authorisation issue. The prototype notification configuration was corrected and notification delivery was retested.

These findings demonstrate why security controls were evaluated through failure/adversarial scenarios rather than judged only by configuration presence.

## 7. Highest-Priority Residual Threats

- T-01 production identity spoofing.
- T-03 disguised/malicious document content.
- T-07 message replay/idempotency.
- T-10/T-19 privileged backend credential compromise.
- T-12/T-13 real-model manipulation and output-integrity uncertainty.
- T-16/T-20 lifecycle policy/governance limitations.

## 8. Relationship to NIST CSF 2.0

The threat model supplies evidence for GOVERN and IDENTIFY and drives control/evaluation decisions across PROTECT, DETECT, RESPOND and RECOVER.

Stage 9 will map these threats and controls into Current/Target Profiles and residual-risk priorities.
