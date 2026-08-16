# Stage 9A — NIST CSF 2.0 Current Profile

## 1. Purpose

This document defines the **Current Profile** for the Capisso DEW cloud security prototype after completion of implementation Stages 0–8.

The profile is intentionally scoped to the implemented AWS/Supabase prototype rather than to Capisso.ai as an entire organisation. It records cybersecurity outcomes that are currently achieved, partially achieved, or not yet achieved within the prototype.

NIST CSF 2.0 defines a Current Profile as the Core outcomes an organisation is currently achieving or attempting to achieve and the extent to which each outcome is being achieved. The CSF Core is organised as Functions, Categories and Subcategories.

## 2. Profile Scope

### In scope

```text
API Gateway
→ Upload Lambda
   ↘ AWS Secrets Manager
→ Private S3 raw storage
→ S3 ObjectCreated
→ Preprocessing SQS/DLQ
→ Preprocessing Lambda
   ↘ AWS Secrets Manager
→ Extraction SQS/DLQ
→ Extraction Lambda
   ↘ AWS Secrets Manager
→ Post-processing validation / HITL routing
→ Supabase
   ↳ Tenant-aware RLS
→ CloudWatch alarms
→ SNS security notifications

EventBridge Scheduler
→ Retention Lambda
→ Secure-deletion Lambda
→ S3/database cleanup
→ Deletion tombstone
```

### Out of scope / incomplete

- Complete production frontend authentication and API authorisation.
- Real managed-model extraction evaluation and measured AI accuracy.
- Complete reviewer user interface.
- AWS WAF and advanced DDoS controls.
- Malware scanning and file-signature validation.
- Complete enterprise incident-management/SIEM capability.
- Complete organisational GDPR compliance assessment.
- Formal disaster-recovery programme.
- Automated Secrets Manager rotation.

## 3. Rating Method

| Rating | Meaning |
|---|---|
| **Achieved** | The selected CSF outcome is materially implemented and supported by prototype evidence. |
| **Partially Achieved** | Relevant controls exist, but an important component of the outcome remains incomplete or prototype-limited. |
| **Not Achieved** | The selected outcome is relevant to the target system but is not materially implemented. |

These ratings are project evaluation labels; they are not NIST maturity scores or CSF Tiers.

## 4. Current Profile

| CSF 2.0 Subcategory | Current State | Prototype Evidence | Current Limitation / Observation |
|---|---|---|---|
| **GV.OC-03** — Legal, regulatory and contractual cybersecurity/privacy requirements are understood and managed | **Partially Achieved** | FRD/PPD security requirements; GDPR-aware retention/deletion design; data minimisation and audit controls | Prototype does not claim complete GDPR compliance or formal legal-policy validation |
| **GV.RM-06** — A standard method for calculating, documenting, categorising and prioritising cybersecurity risk is established | **Achieved** | STRIDE threat model; likelihood × impact risk register; High/Critical prioritisation | Residual scores require Stage 9 reassessment after the final control set |
| **GV.OV-03** — Cybersecurity risk-management performance is evaluated and reviewed | **Partially Achieved** | Stage security tests, failure/remediation/retest records, evidence index | Consolidated framework evaluation is being completed in Stage 9 |
| **ID.AM-02** — Inventories of software, services and systems are maintained | **Achieved** | README architecture; AWS Lambda function map; documented API Gateway, Lambda, S3, SQS, Supabase, Secrets Manager, CloudWatch, SNS and EventBridge components | Inventory is project-level rather than an automated enterprise asset inventory |
| **ID.AM-03** — Authorised network communication and internal/external data flows are represented | **Achieved** | Architecture diagrams, processing flows and STRIDE trust boundaries | Diagrams are manually maintained |
| **ID.AM-07** — Inventories of data and corresponding metadata for designated data types are maintained | **Achieved** | Supabase `documents` metadata, lifecycle status, object references, trace IDs, retention metadata | Prototype metadata inventory is limited to the document-processing use case |
| **ID.AM-08** — Systems, services and data are managed throughout their life cycles | **Achieved** | Upload lifecycle, processing statuses, retention metadata, scheduled retention enforcement and secure-deletion workflow | S3 version-aware deletion and legally approved production retention periods remain |
| **ID.RA-03** — Internal and external threats are identified and recorded | **Achieved** | STRIDE threat catalogue covering upload, storage, queues, AI output, database, logging, retention and deletion | Threat intelligence feeds are not integrated |
| **ID.RA-04** — Potential impacts and likelihoods of threats exploiting vulnerabilities are identified and recorded | **Achieved** | Risk register with likelihood, impact and inherent-risk scoring | Final residual-risk values still require Stage 9 reassessment |
| **ID.RA-05** — Threats, vulnerabilities, likelihoods and impacts are used to understand inherent risk and prioritise response | **Achieved** | Prioritised risk register and security-stage roadmap | Prioritisation is project-specific rather than organisation-wide |
| **ID.IM-01** — Improvements are identified from evaluations | **Achieved** | RLS cross-tenant test failure led to restrictive-policy remediation; SNS/KMS alerting issue led to configuration remediation | Continuous operational review is not automated |
| **ID.IM-02** — Improvements are identified from security tests and exercises | **Achieved** | Controlled DLQ retry-exhaustion test, RLS attack test, deletion tests, throttling test, AI-output security scenarios | Tests are prototype controlled scenarios rather than production exercises |
| **PR.AA-03** — Users, services and hardware are authenticated | **Partially Achieved** | AWS service identities/IAM roles; Secrets Manager access by execution role; authenticated Supabase role/JWT used for RLS testing | `POST /upload` still accepts caller-supplied `userId` and `companyId`; production API authentication is incomplete |
| **PR.AA-05** — Permissions and authorisations are defined, enforced and reviewed using least privilege/separation of duties | **Achieved** | Separate Lambda execution roles; resource-scoped S3/SQS permissions; exact-secret ARN access; dedicated destructive deletion role; Supabase grants/RLS | IAM review is manual and trusted backend service credential remains privileged |
| **PR.DS-01** — Confidentiality, integrity and availability of data at rest are protected | **Achieved** | Private S3 bucket, Block Public Access, server-side encryption, private Supabase data model and RLS | No customer-managed encryption-key lifecycle is evaluated |
| **PR.DS-02** — Confidentiality, integrity and availability of data in transit are protected | **Achieved** | API Gateway HTTPS endpoint, HTTPS pre-signed S3 upload and TLS-based backend service calls | No independent TLS configuration/compliance assessment was performed |
| **PR.PS-01** — Configuration-management practices are established and applied | **Partially Achieved** | Incremental GitHub configuration/code documentation, stage records and IAM policy templates | Significant AWS configuration remains manually managed; infrastructure as code is not implemented |
| **PR.PS-04** — Log records are generated and made available for continuous monitoring | **Achieved** | Structured CloudWatch logs, trace IDs, Supabase audit logs, processing runs and alarms | No central SIEM or automated sensitive-log inspection |
| **PR.IR-03** — Mechanisms are implemented to achieve resilience requirements in normal and adverse situations | **Achieved** | SQS buffering, retry handling, DLQs, CloudWatch alarms, SNS notifications and scheduler DLQ | No formal availability SLO or multi-region resilience |
| **DE.CM-09** — Computing/software/runtime environments and their data are monitored to find adverse events | **Achieved** | Lambda error alarms, DLQ alarms, retention alarm, scheduler DLQ alarm, API 4XX monitoring and structured runtime logs | Coverage is focused on selected prototype signals |
| **DE.AE-02** — Potentially adverse events are analysed to understand associated activity | **Achieved** | DLQ investigation, CloudWatch trace analysis, RLS failure analysis, SNS/KMS failure analysis | Analysis remains mostly manual |
| **DE.AE-03** — Information is correlated from multiple sources | **Partially Achieved** | Trace IDs correlate API/Lambda/CloudWatch/Supabase records; audit and processing records support investigation | No SIEM/automated cross-source correlation |
| **RS.MA-02** — Incident reports are triaged and validated | **Partially Achieved** | Incident-response runbook, alarm/DLQ investigation procedure, controlled failure validation | No production service-desk/on-call incident process |
| **RS.AN-03** — Analysis is performed to determine what occurred and the root cause | **Achieved** | Root-cause analysis of SNS/KMS notification failure and RLS permissive-policy interaction | Evidence derives from controlled prototype incidents |
| **RS.AN-06** — Investigation actions are recorded and record integrity/provenance is preserved | **Achieved** | Git commit history, stage documentation, progress log, screenshot evidence index and CloudWatch/Supabase audit evidence | Evidence management is project-based rather than a formal forensic evidence system |
| **RS.MI-01** — Incidents are contained | **Partially Achieved** | DLQ isolation, HITL escalation, failed-state handling, least-privilege destructive workflow and rate throttling | No automated enterprise containment/orchestration |
| **RC.RP-02** — Recovery actions are selected, scoped, prioritised and performed | **Partially Achieved** | DLQ replay/recovery runbook, controlled message cleanup and recovery tests | Automated idempotent replay remains incomplete |
| **RC.RP-05** — Restored asset integrity is verified and normal operating status is confirmed | **Partially Achieved** | Alarm recovery checks and controlled pipeline retesting after security changes | No formal disaster-recovery restoration test or backup recovery validation |
| **RC.RP-06** — End of incident recovery is declared based on criteria and documentation is completed | **Partially Achieved** | Controlled incident/test closure documented through progress logs and evidence records | Formal organisational recovery-closure criteria are not established |

## 5. Current Profile Summary

| Function | Achieved | Partially Achieved | Not Achieved in selected profile | Main interpretation |
|---|---:|---:|---:|---|
| GOVERN | 1 | 2 | 0 | Risk method exists, but formal governance/oversight remains prototype-level |
| IDENTIFY | 9 | 0 | 0 | Strongest area: assets, flows, lifecycle, threats, tests and improvements are documented |
| PROTECT | 5 | 2 | 0 | Strong technical safeguards; production identity and configuration automation remain important gaps |
| DETECT | 2 | 1 | 0 | Monitoring exists across key runtime/failure signals; correlation is still manual |
| RESPOND | 2 | 2 | 0 | Runbooks and remediation evidence exist; organisation-scale incident operations do not |
| RECOVER | 0 | 3 | 0 | Recovery is the least mature selected Function and remains largely manual |

**Selected outcomes assessed: 29**

The profile demonstrates that the prototype is strongest in **IDENTIFY** and **PROTECT**, with meaningful **DETECT** and **RESPOND** capabilities. The largest remaining weaknesses are production API authentication, automated configuration/secret governance, real-model security validation, advanced abuse/malware controls, and formal recovery capability.

## 6. Evidence Sources Used

Current-profile ratings are based on the following repository artefacts and private screenshot evidence:

- `README.md`
- `security/security-controls.md`
- `docs/threat-model.md`
- `docs/risk-register.md`
- `docs/aws-lambda-function-map.md`
- `docs/progress-log.md`
- `docs/evidence/README.md`
- Stage 5C AI-output validation evidence
- Stage 6 monitoring/incident-response evidence
- Stage 7 retention/secure-deletion evidence
- Stage 8 Secrets Manager, RLS and API-throttling evidence

## 7. Interpretation Rule for the Final Paper

This Current Profile must not be presented as evidence that the full Capisso platform or Capisso.ai organisation is compliant with NIST CSF 2.0.

The defensible claim is:

> The prototype operationalises a selected set of NIST CSF 2.0 cybersecurity outcomes across an AI-driven document-processing lifecycle and identifies the remaining gap between the implemented prototype and a production-oriented Target Profile.

## 8. Next Step

Stage 9B will define the **Target Profile** for the same selected outcomes. The Target Profile will then be compared with this Current Profile to produce the gap analysis, prioritised action plan and residual-risk evaluation.
