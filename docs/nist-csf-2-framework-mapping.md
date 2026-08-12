# NIST CSF 2.0 Mapping for the AWS Document Processing Workflow

## Status

**Preliminary function-level mapping updated after Stage 8.**

This file is not yet the final NIST CSF 2.0 evaluation. Stage 9 will extend it into a formal Current Profile, Target Profile, gap analysis, evidence mapping and prioritised improvement plan.

NIST CSF 2.0 organises cybersecurity outcomes under six Functions: GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND and RECOVER.

## Current Prototype Scope

```text
API Gateway
→ Upload Lambda
→ Private S3
→ Preprocessing SQS/DLQ
→ Preprocessing Lambda
→ Extraction SQS/DLQ
→ Extraction Lambda
→ Post-processing validation / HITL routing
→ Supabase
→ CloudWatch / SNS

EventBridge Scheduler
→ Retention Lambda
→ Secure-deletion Lambda
→ S3/database cleanup and deletion evidence
```

AWS backend Lambdas retrieve the privileged Supabase credential from AWS Secrets Manager. Authenticated tenant-facing database reads are constrained by RLS.

## Function-Level Mapping

| NIST Function | Meaning in this project | Implemented controls/evidence | Important remaining gap |
|---|---|---|---|
| GOVERN | Establish security direction, risk treatment, evidence and accountability | PPD/FRD security requirements, STRIDE model, risk register, stage documentation, Git history, evidence handling rules, NIST mapping | Formal Current/Target Profile and prioritised governance actions still required |
| IDENTIFY | Understand assets, data flows, threats, dependencies and residual risk | Architecture/function map, asset/threat catalogue, document lifecycle metadata, risk register, service/account limitation analysis | Formal residual-risk reassessment and dependency prioritisation |
| PROTECT | Safeguard data, identities, services and processing integrity | S3 private/encrypted storage, short-lived pre-signed URLs, validation, least-privilege IAM, Secrets Manager, RLS, restrictive tenant policy, post-processing validation, HITL, retention/deletion controls, API throttling | Production API authentication, malware/file-signature scanning, secret rotation, WAF, real-model hardening |
| DETECT | Detect failures, abuse, unsafe output and anomalous states | Structured CloudWatch logs, trace IDs, audit records, Lambda alarms, DLQ alarms, API 4XX metric/alarm, validation errors, prompt-injection indicators, retention/scheduler alarms | Broader anomaly detection, SIEM integration and automated sensitive-log scanning |
| RESPOND | Contain, investigate and handle security/processing failures | DLQ investigation/replay runbook, SNS notifications, failed-state handling, HITL escalation, deletion failure recording, controlled remediation/retest evidence | Production incident ownership/escalation and automated response workflows |
| RECOVER | Restore safe processing and enforce lifecycle recovery after failures | DLQ recovery/replay procedure, alarm recovery testing, idempotent deletion handling, scheduled retention enforcement, secure cleanup/tombstone evidence | Formal recovery objectives, automated replay safeguards and tested disaster-recovery procedures |

## Stage 9 Required Extension

The formal evaluation will:
1. select relevant CSF 2.0 Categories/Subcategories rather than treating the Functions as a checklist;
2. define a Current Profile based only on controls actually implemented/tested;
3. define a Target Profile for production-relevant outcomes;
4. identify gaps between Current and Target states;
5. map each implemented outcome to repository/screenshot evidence;
6. link gaps to the STRIDE/risk register;
7. prioritise actions and document residual risk.
