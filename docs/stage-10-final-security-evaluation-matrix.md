# Stage 10 — Final Security Evaluation Matrix

## 1. Purpose

This document consolidates the implementation and security-evaluation evidence for the Capisso DEW cloud security prototype.

It links:

```text
FRD / non-functional requirement
→ threat or risk
→ implemented security control
→ security test
→ expected result
→ observed result
→ evaluation status
→ evidence
→ residual limitation
→ NIST CSF 2.0 outcome
```

The matrix is intended to provide the principal empirical evaluation artefact for the capstone project and the final research paper.

The evaluation is scoped to the implemented AWS/Supabase prototype. It does not claim that the full Capisso.ai organisation is NIST CSF 2.0 compliant, GDPR compliant, production ready, or that real-model extraction accuracy has been demonstrated.

---

## 2. Evaluation Status Definitions

| Status | Meaning |
|---|---|
| **PASS** | The implemented control produced the expected result in the controlled prototype test |
| **REMEDIATED-PASS** | The first test exposed a security/configuration weakness; remediation was applied and the repeated test produced the expected secure result |
| **PARTIAL** | The control was implemented and some evidence was produced, but the complete intended test outcome was not demonstrated |
| **DEFERRED / CONSTRAINT** | The test or capability could not be completed because of an explicitly documented external/prototype limitation |

These labels describe prototype test outcomes. They are not statistical measures of security effectiveness and are not NIST maturity scores.

---

# 3. Final Security Evaluation Matrix

| ID | FRD / Project Requirement | Threat / Risk | Implemented Control | Security Test | Expected Result | Observed Result | Status | Evidence | NIST CSF 2.0 | Residual Limitation |
|---|---|---|---|---|---|---|---|---|---|---|
| **EV-01** | FR-INPUT-001/002; SEC-006 | T-03/T-04; R-03/R-04 | Upload Lambda metadata validation; PDF/JPEG/PNG allow-list; 10 MB limit; filename sanitisation | Submit valid upload-initiation request | Request accepted and short-lived pre-signed PUT URL returned | Valid request created document/job identifiers and upload URL | **PASS** | Stage 1 upload tests; `lambda/upload/lambda_function.py` | PR.AA-05, PR.DS-02, PR.PS-01 | Validation is metadata based; no malware/file-signature scan |
| **EV-02** | FR-INPUT-001/002; SEC-006 | T-03/T-04; R-03/R-04 | Strict type/size/extension checks | Submit invalid/unsupported type and invalid-size requests | Request rejected before upload authority is created | Invalid requests rejected with controlled 4XX response | **PASS** | Stage 1 negative tests; upload Lambda validation code | PR.PS-01, ID.IM-02 | Does not prove resistance to polyglot/disguised malicious files |
| **EV-03** | SEC-001; SEC-002 | T-02/T-05; R-02/R-05 | Private S3 bucket, Block Public Access, server-side encryption, short-lived pre-signed PUT | Upload controlled document using pre-signed URL | PUT succeeds only through authorised temporary URL; object remains private | S3 PUT returned HTTP 200 and object stored under controlled `raw/` path | **PASS** | Stage 1 S3 evidence; bucket security configuration | PR.DS-01, PR.DS-02 | Customer-managed key lifecycle and independent TLS-version validation were not evaluated |
| **EV-04** | NFR-003; NFR-008; FR-WORK-004 | T-07/T-15; R-07/R-14 | S3 ObjectCreated → preprocessing SQS/DLQ → preprocessing Lambda | Upload document and observe event-driven handoff | Event buffered and processed without direct synchronous coupling | S3 event reached SQS; preprocessing handled event and updated lifecycle/audit state | **PASS** | Stage 3 evidence; preprocessing queue/Lambda logs | PR.IR-03, ID.AM-08 | Comprehensive replay/idempotency controls remain incomplete |
| **EV-05** | FR-WORK-004; NFR-004; NFR-008 | T-07/T-15; R-07/R-14 | Separate extraction queue/DLQ and processing-run/extraction-result records | Complete preprocessing-to-extraction handoff | Extraction message processed and trace/lifecycle preserved | Controlled pipeline created processing run/extraction result and completed document lifecycle | **PASS** | Stage 4/8A full-pipeline regression evidence | PR.IR-03, PR.PS-04, DE.CM-09 | Extraction provider is deterministic/mock in evaluated path |
| **EV-06** | FR-QUAL-002/004; FR-OUTPUT-001/003 | T-13; R-12 | Versioned schema, field/type/date/currency/financial validation | Process valid deterministic extraction scenario | Output marked valid; no unnecessary human review | `validationStatus=valid`; no validation errors; `needsHumanReview=false` | **PASS** | Stage 5C valid scenario evidence | ID.IM-02, PR.PS-04 | Real-model output distribution not evaluated |
| **EV-07** | FR-QUAL-001/004/005 | T-14; R-13 | Overall/field confidence thresholds and review-task routing | Process low-confidence extraction scenario | Low-confidence result must not silently auto-complete | Review reason/priority generated and HITL task routed | **PASS** | Stage 5C low-confidence test | ID.IM-02, RS.MI-01 | Thresholds are not calibrated against a real-model validation dataset |
| **EV-08** | FR-STRUCT-001; FR-QUAL-001/004 | T-13; R-12 | Required-field and schema validation | Process output missing required field | Missing mandatory data detected and prevented from normal valid completion | Validation errors/review routing produced | **PASS** | Stage 5C missing-required-field test | ID.IM-02, PR.PS-04 | Coverage is based on designed schema/test scenarios |
| **EV-09** | FR-QUAL-001/004; financial integrity objective | T-13; R-12 | Total/subtotal/tax and line-item consistency rules | Process deliberately inconsistent financial output | Integrity mismatch detected and escalated | Financial mismatch detected and routed for review | **PASS** | Stage 5C financial-mismatch test | ID.IM-02, RS.MI-01 | Business-rule coverage is not exhaustive |
| **EV-10** | AI-output security control; FR-QUAL-001 | T-12; R-11 | Suspicious prompt-instruction indicators and high-priority HITL escalation | Process extraction containing prompt-injection-like instruction | Suspicious content must trigger escalation rather than silent trust | Prompt-injection indicator triggered review/escalation | **PASS** | Stage 5C prompt-injection scenario | ID.IM-02, RS.MI-01 | Pattern detection is limited and is not a complete prompt-injection defence |
| **EV-11** | FR-OUTPUT-001; FR-QUAL-003/004 | T-13; R-12 | Strict JSON/schema parsing and controlled invalid-output handling | Provide malformed extraction output | Malformed output rejected/flagged and not treated as valid business data | Malformed-output scenario produced controlled validation failure/review state | **PASS** | Stage 5C malformed-output test | ID.IM-02, DE.AE-02 | Real-model malformed-output frequency is unknown |
| **EV-12** | NFR-006; NFR-008; SEC-004 | T-15/T-18; R-14/R-17 | SQS retries, DLQ redrive, Lambda/DLQ alarms, SNS notification | Send invalid extraction message to main queue and allow retry exhaustion | Message retries, moves automatically to DLQ, alarm/notification generated | Automatic retry exhaustion moved message to DLQ; alarm and notification evidence captured; controlled cleanup/recovery performed | **PASS** | Stage 6 retry-exhaustion and DLQ evidence | DE.CM-09, DE.AE-02, RS.MA-02, RC.RP-02 | Safe replay remains manual and not fully idempotent |
| **EV-13** | NFR-006; SEC-004 | T-18; R-17 | CloudWatch alarm → SNS security notification channel | Trigger controlled alarm and verify notification delivery | Alarm transition must reach security notification recipient | Initial notification failed due SNS/KMS authorisation; configuration was corrected and repeat notification succeeded | **REMEDIATED-PASS** | Stage 6 initial failure + successful SNS email evidence | ID.IM-01, DE.AE-02, RS.AN-03 | SNS topic encryption was disabled for prototype; email-only notification path |
| **EV-14** | SEC-002; SEC-005 | T-16/T-20; R-15 | Dedicated deletion Lambda, exact bucket/prefix checks, S3 delete verification, DB cleanup, audit redaction, deletion tombstone, idempotency | Perform controlled manual secure-deletion request and repeat request | S3 object absent; dependent DB data removed; identifying audit metadata minimised; repeat request safe | Deletion completed; S3 absence verified; database records removed; audit redacted; tombstone written; repeat deletion handled idempotently | **PASS** | Stage 7 manual secure-deletion evidence; deletion Lambda | ID.AM-08, PR.DS-01, RS.MI-01 | S3 version-aware deletion required if versioning is enabled |
| **EV-15** | SEC-002; SEC-005 | T-20; R-15 | `retention_until` validation and retention request safety check | Invoke retention deletion before deadline | Premature destructive action rejected | Retention request returned controlled `not_due`/409-style rejection and document remained | **PASS** | Stage 7 `retention_not_due` evidence | ID.AM-08, PR.DS-01 | Prototype policy is technical; legal retention basis not established |
| **EV-16** | SEC-002; SEC-005; NFR-008 | T-16; R-15 | Retention Lambda + EventBridge Scheduler + delegated deletion + scheduler DLQ/alarm | Set controlled document to expired retention state and run retention enforcement | Expired eligible document discovered and securely deleted | Retention scan found eligible document; delegated deletion completed; automatic scheduler invocation later verified | **PASS** | Stage 7D/7E retention and scheduler evidence | ID.AM-08, DE.CM-09, RC.RP-02 | 30-day policy is prototype-only; organisation/legal approval outstanding |
| **EV-17** | SEC-003; secret-management hardening | T-10/T-19; R-09 | AWS Secrets Manager, exact-secret ARN `GetSecretValue`, plaintext service-role env removal | Remove plaintext Supabase service-role environment secret and rerun full pipeline | Backend continues working using runtime secret retrieval; secret value absent from Lambda configuration/source | Upload-through-extraction regression reached `ocr_completed` after migration | **PASS** | Stage 8A Secrets Manager and full-pipeline evidence | PR.AA-05, PR.PS-01 | Rotation is manual; backend service credential remains highly privileged |
| **EV-18** | SEC-003 company-level isolation | T-11; R-10 | Supabase RLS using JWT `app_metadata.company_id`; least-privilege grants; mandatory restrictive document policy | Tenant A queries a known Tenant B document | Cross-tenant query returns zero rows | First test **failed** with 1 foreign row visible; restrictive policy introduced; retest returned `PASS - CROSS TENANT ACCESS BLOCKED`, `rows_visible=0` | **REMEDIATED-PASS** | Stage 8B initial-failure and final-pass screenshots; `stage-8-tenant-rls.sql` | PR.AA-05, ID.IM-01, RS.AN-03 | End-to-end API identity is incomplete; privileged backend credential can bypass RLS |
| **EV-19** | SEC-006; T-04/R-04 | API Gateway stage throttling + stricter `POST /upload` method throttling | Send controlled concurrent 15-request burst | Excessive burst should cause at least some gateway rejection | Burst produced HTTP `429 Too Many Requests` while normal requests remained accepted | **PASS** | Stage 8 screenshot `25-controlled-api-burst-throttled-429`; API throttling configuration | PR.IR-03, DE.CM-09 | API Gateway throttling is best-effort; no AWS WAF/authentication-aware limiting |
| **EV-20** | SEC-004; SEC-006; NFR-006 | T-04/T-18; R-04/R-17 | API Gateway `4XXError` CloudWatch metric/alarm | Generate throttled/4XX traffic and observe metric/alarm | 4XX metric recorded; configured threshold should alarm when threshold is reached | CloudWatch recorded the generated 4XX event; only one 429 occurred in the test minute, below the final alarm threshold of 5, so the alarm correctly remained `OK` | **PARTIAL** | Stage 8 4XX metric graph and alarm configuration | DE.CM-09, DE.AE-02 | Final-threshold ALARM/SNS transition was not demonstrated in this test |
| **EV-21** | FR-OCR-001–005; project-lead real-model objective | T-12/T-13/T-14; R-11/R-12/R-13 | AWS-native model-service integration attempt and secure model-adapter design | Invoke a real AWS extraction/model service | Real model returns extraction output for downstream security/accuracy evaluation | Textract service boundary was reached but AWS returned `SubscriptionRequiredException`; later real-model invocation remained deferred under account/service restrictions | **DEFERRED / CONSTRAINT** | Stage 5A service-attempt evidence; Stage 5B adapter/model plan | GV.OC-03, ID.RA-03, ID.IM-02 | No claims can be made about real-model accuracy, real-model prompt-injection resistance or production AI assurance |

---

# 4. FRD Data Security & Privacy Coverage

The FRD defines six explicit security/privacy requirements. The table below evaluates them at requirement-family level rather than treating the presence of one control as full compliance.

| FRD Requirement | FRD Intent | Prototype Coverage | Assessment | Evidence / Reason |
|---|---|---|---|---|
| **SEC-001** | Applicable data-protection compliance; encryption at rest and in transit; compliance audit logging | Private encrypted S3, HTTPS service paths, audit records, traceability, lifecycle controls | **PARTIALLY SATISFIED** | Core technical protections are implemented, but the prototype does not prove full GDPR compliance, PostgreSQL transparent/application-field encryption, backup encryption governance or formal legal approval |
| **SEC-002** | Defence-in-depth storage, public-access restriction, encryption, application-level DB protection and secure deletion | S3 Block Public Access/encryption, least privilege, tenant RLS, retention and verified deletion | **PARTIALLY SATISFIED** | Strong storage/deletion controls implemented; application-level encrypted sensitive DB fields were not implemented/evaluated |
| **SEC-003** | Least privilege, RBAC, user permissions and company isolation | Separate IAM roles, resource-scoped IAM, exact-secret access, Supabase grants/RLS, cross-tenant adversarial test | **PARTIALLY SATISFIED** | Company isolation was empirically remediated/tested, but production API authentication/user identity is incomplete and the backend service credential remains privileged |
| **SEC-004** | Security event logging, authentication/authorization event logs and anomaly detection | CloudWatch logs/alarms, DLQ alarms, SNS, trace IDs, API 4XX monitoring, failure investigations | **PARTIALLY SATISFIED** | Processing/security-event monitoring is strong, but production authentication-event logging, denied-authorization telemetry, SIEM correlation and broad anomaly detection remain incomplete |
| **SEC-005** | Identify/protect/manage PII, support data-subject access and deletion | Private storage, least privilege/RLS, retention metadata, deletion-on-request workflow, audit minimisation | **PARTIALLY SATISFIED** | Deletion/lifecycle protection implemented; automated PII identification and a complete GDPR DSAR access workflow are not implemented |
| **SEC-006** | Rate limiting, strict API input validation, HTTPS-only and strict CORS; SQLi/XSS prevention | API throttling, 10 MB limit, PDF/JPEG/PNG validation, filename sanitisation, HTTPS API/S3 paths, configurable CORS | **PARTIALLY / SUBSTANTIALLY SATISFIED** | Main prototype API controls are implemented/tested; no dedicated SQL-injection/XSS test suite, WAF or production-authenticated API boundary |

The FRD explicitly requires encryption, defence-in-depth storage, least privilege/company isolation, security-event logging, PII lifecycle handling and secure API controls. The prototype therefore addresses the principal security themes, but **none of the six FRD requirement families should be described as full production compliance**.

---

# 5. Supporting Functional and Non-Functional Requirement Evaluation

| Requirement | Prototype Result | Assessment |
|---|---|---|
| **FR-WORK-004 — workflow orchestration/error handling/retry** | S3/SQS/Lambda pipeline, retry/DLQ behaviour and recovery procedure implemented | **Strong prototype coverage** |
| **FR-QUAL-001 — low-confidence review routing** | Low-confidence scenarios automatically route to review tasks | **Implemented and tested** |
| **FR-QUAL-002 — processing status** | Lifecycle states stored in Supabase throughout upload/preprocess/extraction/deletion | **Implemented** |
| **FR-QUAL-003 — processing error logging** | Controlled structured errors/trace IDs stored in CloudWatch and business audit records | **Implemented with privacy-conscious sanitisation; not every FRD-requested debug field is deliberately logged** |
| **FR-QUAL-004 — quality/confidence indicators** | Overall/field confidence plus validation errors/reasons are persisted | **Implemented in deterministic adapter path** |
| **FR-QUAL-005 — HITL corrections** | HITL backend/review tasks exist; correction schema is available | **Partially implemented; complete reviewer UI/model-training feedback loop is out of scope** |
| **NFR-004 — comprehensive audit trail** | Upload, preprocessing, extraction, validation, deletion and trace records exist | **Partially/strongly implemented; real-model invocation metadata is unavailable because real model was deferred** |
| **NFR-006 — observability** | Trace IDs, Lambda/DLQ alarms, SNS, retention/scheduler monitoring and API 4XX metric | **Strong prototype coverage; no full operations dashboard/SIEM and no complete SLA metric suite** |
| **NFR-007 — comprehensive testing** | Controlled negative, integration, end-to-end and security-scenario testing across stages | **Partially satisfied; testing is largely manual and no complete automated unit/A-B test framework exists** |
| **NFR-008 — graceful failure/recovery** | SQS retries/DLQs, alarms, runbook, scheduler DLQ and controlled recovery evidence | **Partially/strongly implemented; formal backup restoration/DR/RTO/RPO not tested** |
| **NFR-009 — documentation** | Stage docs, architecture, API docs, threat model, risk register, NIST profiles, evidence index and Git history | **Implemented at prototype/project level** |

---

# 6. Evaluation Summary

## 6.1 Security-scenario results

The final matrix contains **21 evaluated scenarios/capabilities**:

```text
PASS:                 17
REMEDIATED-PASS:       2
PARTIAL:               1
DEFERRED / CONSTRAINT: 1
```

The two remediated results are significant because they represent **observed security weaknesses discovered by testing**, not merely planned controls:

```text
RLS tenant isolation
FAIL → root cause identified → restrictive policy → PASS
```

and:

```text
SNS alarm notification
FAIL → KMS/SNS authorisation issue identified → configuration remediation → PASS
```

This count should not be converted into a percentage “security score.” The test cases are heterogeneous and do not have equal risk weight.

## 6.2 Strongest demonstrated areas

The strongest evidence is concentrated in:

- input validation and controlled upload;
- private S3 storage;
- event-driven queue isolation;
- least-privilege AWS service roles;
- Secrets Manager credential handling;
- deterministic AI-output integrity checks;
- low-confidence/HITL escalation;
- retry exhaustion and DLQ monitoring;
- security alerting;
- retention safety;
- verified secure deletion;
- tenant-isolation adversarial testing;
- API throttling;
- traceability and evidence-driven remediation.

These results align with the Stage 9A finding that **IDENTIFY** and **PROTECT** are the strongest Current-Profile areas, with meaningful **DETECT** and **RESPOND** capability.

## 6.3 Weakest / incomplete areas

The largest remaining limitations are:

1. **Production API authentication and trusted tenant identity**.
2. **Malware/file-signature validation** for untrusted uploads.
3. **Real-model security and accuracy evaluation**.
4. **Formal legal/privacy governance** for retention and GDPR obligations.
5. **Infrastructure as Code and drift/configuration governance**.
6. **Queue idempotency and replay protection**.
7. **Centralised SIEM/event correlation**.
8. **Formal incident triage/ownership/escalation**.
9. **Backup/restoration testing, RTO/RPO and formal recovery**.
10. **Automated secret rotation**.
11. **Version-aware secure deletion if S3 versioning is enabled**.
12. **Complete HITL reviewer UI and training feedback loop**.

---

# 7. Key Empirical Findings

## Finding F-01 — A configured control can still fail its security objective

The first tenant-isolation test returned:

```text
FAIL - CROSS TENANT DOCUMENT VISIBLE
rows_visible = 1
```

This demonstrated that the existence of an RLS policy was not sufficient evidence of isolation.

A mandatory restrictive policy was introduced and the same cross-tenant test subsequently returned:

```text
PASS - CROSS TENANT ACCESS BLOCKED
rows_visible = 0
```

**Interpretation:** negative/adversarial validation is necessary for access-control assurance.

---

## Finding F-02 — Monitoring configuration must be end-to-end tested

The first controlled CloudWatch/SNS alert test detected the Lambda failure but notification delivery was affected by SNS/KMS authorisation.

After remediation, the notification path was retested successfully.

**Interpretation:** an alarm in the console is not equivalent to an operational incident-notification capability.

---

## Finding F-03 — Security controls can be evaluated independently of model accuracy

The real model could not be executed under the available AWS account/service entitlement. Instead of presenting mock data as AI performance evidence, deterministic extraction scenarios were used to test:

- schema validation;
- required-field enforcement;
- confidence handling;
- financial consistency;
- malformed output;
- prompt-injection indicators;
- HITL routing.

**Interpretation:** the framework’s orchestration and output-security controls can be evaluated independently, but **real-model accuracy and adversarial robustness remain unverified**.

---

## Finding F-04 — Data-lifecycle security requires more than object deletion

The secure-deletion workflow verifies S3 deletion, removes dependent processing data, minimises audit identifiers and preserves a non-content deletion tombstone.

**Interpretation:** lifecycle governance is stronger when deletion is treated as a verifiable multi-system process rather than a single `DeleteObject` API call.

---

# 8. Residual-Risk Interpretation

The Stage 9 Current-to-Target analysis identified the highest-priority residual areas as:

| Residual Area | Qualitative Concern | Reason |
|---|---|---|
| API identity spoofing | **High** | `/upload` still accepts prototype tenant/user fields |
| Malicious/disguised file content | **High** | No magic-byte or malware-scanning stage |
| Real-model manipulation/output integrity | **High** | No real-model adversarial evaluation |
| Recovery/restoration | **High** | No formal backup restoration/RTO/RPO test |
| Queue replay/idempotency | **Medium–High** | DLQ/retries exist but comprehensive duplicate/replay defence does not |
| Retention/legal governance | **Medium–High** | Technical retention works; legal/business policy selection is prototype-limited |
| Privileged backend service credential | **Medium** | Secrets Manager reduces exposure, but credential remains privileged and rotation is manual |
| API abuse | **Medium** | Throttling/4XX monitoring exist; no WAF/authenticated abuse policy |
| Incident operations | **Medium** | Detection/runbook exists; production ownership/escalation is incomplete |
| Telemetry correlation | **Medium** | Trace IDs support manual correlation; no SIEM |

These are **residual concerns for production hardening**, not evidence that the prototype implementation failed.

---

# 9. Paper-Ready Evaluation Statement

The following is the defensible high-level interpretation of the evaluation:

> The implemented framework materially improved the security posture of the AI-driven document-processing workflow by introducing defence-in-depth controls across ingestion, storage, asynchronous processing, AI-output validation, access control, monitoring, retention and deletion. Controlled negative and failure-path testing demonstrated that most implemented controls behaved as intended, while two tests exposed configuration weaknesses in tenant isolation and alarm delivery that were subsequently remediated and successfully retested. The evaluation also identified material production gaps in authenticated tenant identity, malicious-file inspection, real-model assurance, configuration governance and recovery capability. Accordingly, the prototype demonstrates a testable cloud security management framework rather than production compliance or complete AI-system assurance.

---

# 10. Evidence and Traceability Sources

Primary evidence is distributed across:

```text
README.md
security/security-controls.md
docs/threat-model.md
docs/risk-register.md
docs/stage-9a-nist-current-profile.md
docs/stage-9b-nist-target-profile.md
docs/stage-9c-nist-gap-analysis.md
docs/evidence/README.md
docs/progress-log.md
lambda/
database/
api-gateway/
security/
private implementation screenshots
CloudWatch/SNS/SQS/Supabase test evidence
```

The public repository should continue to contain only sanitised documentation/evidence indexes. Raw screenshots containing account details or sensitive configuration should remain private.

---

# 11. Stage 10 Conclusion

Stage 10 completes the formal framework evaluation sequence:

```text
Implementation Stages 0–8
        ↓
STRIDE threat model + risk register
        ↓
Stage 9A Current Profile
        ↓
Stage 9B Target Profile
        ↓
Stage 9C Gap Analysis
        ↓
Stage 10 Security Evaluation Matrix
        ↓
Final research paper
```

No additional major AWS feature is required to make the existing prototype evaluable.

The next work should focus on converting these implementation and evaluation results into the final capstone paper, with explicit separation between:

```text
Implemented and tested
Implemented but partially evaluated
Designed/deferred
Production target / future work
```

---

## References

- Capisso.ai, *Functional Requirements Document — Document Extraction Workflow (DEW)*, Version 1.1.
- National Institute of Standards and Technology, *The NIST Cybersecurity Framework (CSF) 2.0*, NIST CSWP 29, 2024.
- National Institute of Standards and Technology, *Cybersecurity Framework 2.0: Quick-Start Guide for Creating and Using Organizational Profiles*, NIST SP 1301, 2024.
