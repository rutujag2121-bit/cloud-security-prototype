# Stage 9C — NIST CSF 2.0 Current-to-Target Gap Analysis

## 1. Purpose

This document compares the Stage 9A **Current Profile** with the Stage 9B **Target Profile** for the Capisso DEW cloud security prototype.

The purpose is to identify the security outcomes that still require improvement, connect those gaps to the project threat/risk evidence, and define a prioritised production-hardening plan.

NIST CSF 2.0 recommends comparing Current and Target Profiles to identify and analyse gaps and then develop a prioritised action plan. This document performs that comparison for the 29 CSF 2.0 outcomes selected for this project.

## 2. Scope and Interpretation

This gap analysis applies only to the implemented AWS/Supabase prototype. It does **not** claim that the wider Capisso.ai organisation is compliant with NIST CSF 2.0.

Three gap types are used:

| Gap Type | Meaning |
|---|---|
| **Material gap** | Current state is only Partially Achieved and the Target state requires Achieved |
| **Production-hardening gap** | Current outcome is materially achieved in the prototype, but target production controls require additional governance, automation or assurance |
| **Maintain / validate** | No major implementation gap; the target is to retain and periodically verify the current control |

Priority is inherited from Stage 9B:

| Priority | Meaning |
|---|---|
| **P1 — High** | Production prerequisite or important residual risk |
| **P2 — Medium** | Material hardening activity after P1 |
| **P3 — Maintain** | Existing capability should be maintained and periodically validated |

## 3. Full Current-to-Target Gap Matrix

| CSF 2.0 Outcome | Current | Target | Gap Type | Priority | Main Gap / Required Action | Related Project Risk / Evidence |
|---|---|---|---|---|---|---|
| **GV.OC-03** | Partially Achieved | Achieved | **Material gap** | **P1** | Formalise legal/privacy requirements, approved retention basis, processor responsibilities and production GDPR governance | R-15; retention/deletion implemented, but 30-day value is prototype-only |
| **GV.RM-06** | Achieved | Achieved | Maintain / validate | P3 | Retain the likelihood × impact method and periodically review scoring criteria | STRIDE + risk register |
| **GV.OV-03** | Partially Achieved | Achieved | **Material gap** | P2 | Establish recurring security-control review, ownership, remediation tracking and closure | Stage tests exist; consolidated governance review remains manual |
| **ID.AM-02** | Achieved | Achieved | Maintain / validate | P3 | Keep the service/system inventory current and automate where practical | README architecture + Lambda function map |
| **ID.AM-03** | Achieved | Achieved | Maintain / validate | P3 | Maintain architecture, trust-boundary and data-flow documentation after changes | STRIDE trust boundaries + architecture docs |
| **ID.AM-07** | Achieved | Achieved | Production-hardening gap | P2 | Extend project metadata into a formal data inventory/classification with sensitivity and retention requirements | Supabase document/lifecycle metadata |
| **ID.AM-08** | Achieved | Achieved | **Production-hardening gap** | **P1** | Use approved retention schedules, periodic lifecycle review and version-aware deletion where needed | R-15 / T-16 / T-20; Stage 7 |
| **ID.RA-03** | Achieved | Achieved | Maintain / validate | P3 | Review threats after architecture/model changes and incorporate relevant cloud/AI threat intelligence | STRIDE threat catalogue |
| **ID.RA-04** | Achieved | Achieved | Production-hardening gap | P2 | Recalculate and document residual risk after major control changes | Risk register currently preserves inherent scoring pending final reassessment |
| **ID.RA-05** | Achieved | Achieved | Production-hardening gap | P2 | Use residual-risk results to support release/remediation priorities | Current prioritisation is project-specific |
| **ID.IM-01** | Achieved | Achieved | Maintain / validate | P3 | Continue recording improvement actions from findings and incidents | RLS failure/remediation; SNS/KMS failure/remediation |
| **ID.IM-02** | Achieved | Achieved | Production-hardening gap | P2 | Convert controlled security tests into a repeatable regression/security-test suite | DLQ, RLS, deletion, throttling and AI-output tests |
| **PR.AA-03** | Partially Achieved | Achieved | **Material gap** | **P1** | Implement verified JWT/OIDC authentication at the API boundary and derive tenant/user identity from trusted claims | R-01 / T-01; `/upload` still accepts caller-supplied `userId` and `companyId` |
| **PR.AA-05** | Achieved | Achieved | **Production-hardening gap** | **P1** | Preserve least privilege, add periodic IAM/RLS review, minimise privileged backend service-role use and enforce authorisation on administrative/destructive operations | R-06, R-09, R-10, T-19 |
| **PR.DS-01** | Achieved | Achieved | Production-hardening gap | P2 | Maintain private encrypted storage and define key/backup/versioned-object requirements | S3 encryption/BPA, RLS, lifecycle controls |
| **PR.DS-02** | Achieved | Achieved | Maintain / validate | P3 | Continue enforcing HTTPS/TLS and periodically validate configuration | API Gateway/S3/backend HTTPS paths |
| **PR.PS-01** | Partially Achieved | Achieved | **Material gap** | **P1** | Move critical AWS configuration to Infrastructure as Code, review changes and detect configuration drift | Much of prototype configuration remains console-managed |
| **PR.PS-04** | Achieved | Achieved | Production-hardening gap | P2 | Reduce unnecessary sensitive metadata, define log retention/integrity requirements and centralise security logs | CloudWatch + Supabase audit; no SIEM |
| **PR.IR-03** | Achieved | Achieved | Production-hardening gap | P2 | Define resilience objectives, backlog thresholds, replay controls and service-dependency recovery tests | SQS/DLQ resilience implemented; no formal SLO/multi-region plan |
| **DE.CM-09** | Achieved | Achieved | Production-hardening gap | P2 | Expand monitoring to authentication failures, suspicious access, secret use and broader lifecycle anomalies | Lambda/DLQ/API/retention alarms already exist |
| **DE.AE-02** | Achieved | Achieved | Production-hardening gap | P2 | Standardise event analysis, severity and investigation procedures | Existing analysis is mostly manual |
| **DE.AE-03** | Partially Achieved | Achieved | **Material gap** | P2 | Centralise and correlate API, Lambda, CloudWatch, Supabase and IAM/CloudTrail events using SIEM/security analytics | Trace IDs provide manual correlation only |
| **RS.MA-02** | Partially Achieved | Achieved | **Material gap** | **P1** | Define formal triage/severity criteria, ownership, escalation, evidence requirements and incident workflow | R-17 / T-18; current runbook is prototype/manual |
| **RS.AN-03** | Achieved | Achieved | Production-hardening gap | P2 | Formalise root-cause-analysis procedure and connect corrective actions to the risk register | RLS and SNS/KMS RCA evidence exists |
| **RS.AN-06** | Achieved | Achieved | Production-hardening gap | P2 | Establish evidence-integrity/access/retention rules for incident artefacts | Git/progress/evidence history exists but is not a forensic evidence system |
| **RS.MI-01** | Partially Achieved | Achieved | **Material gap** | P2 | Define containment playbooks for credential compromise, abuse, poisoned messages, cross-tenant attempts and unsafe model behaviour | DLQ/HITL/rate throttling provide partial containment |
| **RC.RP-02** | Partially Achieved | Achieved | **Material gap** | **P1** | Define tested recovery procedures, safe replay, service/database recovery and RTO/RPO where applicable | R-14/R-17; current recovery is mainly DLQ/manual |
| **RC.RP-05** | Partially Achieved | Achieved | **Material gap** | **P1** | Test restoration and verify application/data integrity after recovery | Pipeline retest exists; no formal backup/disaster-recovery restoration test |
| **RC.RP-06** | Partially Achieved | Achieved | **Material gap** | P2 | Define recovery-completion criteria, closure evidence and post-incident review | Current closure is documented only at project/test level |

## 4. Gap Summary

### Outcome counts

```text
Selected CSF outcomes assessed: 29

Current state:
Achieved:             19
Partially Achieved:   10
Not Achieved:          0

Current → Target material status gaps:
10 outcomes

Stage 9B priorities:
P1 — High:       8 outcomes
P2 — Medium:    15 outcomes
P3 — Maintain:   6 outcomes
```

The absence of a `Not Achieved` rating should not be interpreted as a complete production security posture. The project intentionally selected CSF outcomes that are directly relevant to the implemented framework. Many outcomes rated `Achieved` still contain production-hardening requirements.

## 5. Highest-Priority Gap Analysis

### GAP-01 — Trusted API Identity

**Mapped outcomes:** PR.AA-03, PR.AA-05  
**Priority:** P1  
**Related risks:** R-01, R-10; T-01

#### Current state

The prototype applies IAM to AWS service identities and uses JWT `app_metadata.company_id` for Supabase RLS testing. However, the public upload-initiation path still accepts prototype `userId` and `companyId` values from the request.

#### Security consequence

A caller may attempt to initiate processing using another tenant identifier unless the API identity is verified before the trusted backend service-role path is used.

#### Target treatment

```text
Client
→ signed JWT/OIDC token
→ API authorizer verifies token
→ tenant/user derived from trusted claims
→ Lambda ignores caller-supplied tenant identity
→ database RLS enforces the same tenant
```

#### Required validation

- missing/invalid token → rejected;
- forged/modified token → rejected;
- Tenant A supplied body cannot override authenticated company;
- valid Tenant A request succeeds;
- Tenant A cannot access Tenant B.

#### Residual risk after current prototype

**High** for production deployment; acceptable only as a clearly documented prototype limitation.

---

### GAP-02 — Governed Retention and Version-Aware Deletion

**Mapped outcomes:** GV.OC-03, ID.AM-08  
**Priority:** P1  
**Related risks:** R-15; T-16, T-20

#### Current state

Stage 7 implements retention metadata, scheduler enforcement, premature-deletion protection, verified S3/database deletion and deletion tombstones.

#### Remaining gap

The 30-day period is a prototype value rather than a formally approved legal/business retention schedule. Version-aware object deletion also requires additional handling if S3 versioning is enabled.

#### Target treatment

- approved retention schedule by data category;
- documented lawful/business basis;
- retention-policy change control;
- periodic deletion verification;
- deletion of all relevant object versions/delete markers where required.

#### Residual risk

**Medium–High** until organisational/legal lifecycle policy is established.

---

### GAP-03 — Configuration as Controlled Code

**Mapped outcome:** PR.PS-01  
**Priority:** P1

#### Current state

Code and documentation are version-controlled in GitHub, but many AWS resources and security settings were configured manually through the console.

#### Security consequence

Manual configuration increases the risk of drift, inconsistent environments and weak change traceability.

#### Target treatment

- Infrastructure as Code for IAM, Lambda, S3, SQS/DLQs, alarms, API throttling, Scheduler and retention components;
- peer-reviewed security changes;
- automated policy/configuration checks;
- controlled deployment process.

#### Residual risk

**Medium** in the prototype; increases with deployment scale and multiple environments.

---

### GAP-04 — Formal Incident Management

**Mapped outcomes:** RS.MA-02, RS.MI-01  
**Priority:** P1/P2  
**Related risks:** R-17; T-18

#### Current state

The prototype has CloudWatch alarms, SNS notifications, DLQ evidence and a replay/investigation runbook. Controlled failures have been investigated and remediated.

#### Remaining gap

There is no organisational incident-severity model, accountable owner/on-call process, formal escalation path or containment catalogue.

#### Target treatment

- severity levels;
- owner and escalation matrix;
- response/notification time objectives;
- evidence requirements;
- containment playbooks;
- incident closure/post-incident review.

#### Residual risk

**Medium**, because detection exists but response remains manually coordinated.

---

### GAP-05 — Tested Recovery Capability

**Mapped outcomes:** RC.RP-02, RC.RP-05, RC.RP-06  
**Priority:** P1/P2  
**Related risks:** R-14, R-17

#### Current state

The system has queue retry/DLQ recovery procedures, manual replay guidance, alarm recovery tests and post-remediation pipeline regression tests.

#### Remaining gap

There is no formal recovery plan covering application/database restoration, RTO/RPO, integrity verification and recovery-completion criteria.

#### Target treatment

- define recoverable services/data;
- define RTO/RPO where applicable;
- test safe/idempotent replay;
- test database/application restoration where backups are used;
- verify integrity after recovery;
- record recovery closure and lessons learned.

#### Residual risk

**High** for production resilience until restoration is tested.

## 6. Important Cross-Cutting Gaps Not Fully Represented by a Single Status Change

Several important security gaps remain even where the selected NIST outcome is already rated Achieved.

### 6.1 File-content security

Current:

```text
extension + MIME + size validation
```

Target:

```text
file-signature / magic-byte verification
→ malware scanning
→ quarantine/reject path
→ downstream processing only after safe validation
```

Related risk: R-03 / T-03.

Residual risk: **High** for untrusted production uploads.

### 6.2 Queue idempotency and replay protection

Current:

```text
SQS permissions
+ retries
+ DLQ
+ manual recovery
```

Target:

```text
versioned message schema
+ idempotency key
+ duplicate-state check
+ controlled replay
```

Related risk: R-07 / T-07.

Residual risk: **Medium–High**.

### 6.3 Real-model security assurance

Current:

```text
secure adapter design
+ deterministic mock extraction
+ schema validation
+ confidence checks
+ prompt-injection indicators
+ HITL
```

Target:

```text
real model invocation
+ clean/adversarial dataset
+ prompt-injection testing
+ malformed-output measurement
+ HITL-trigger evaluation
+ labelled extraction-accuracy evaluation
```

Related risks: R-11, R-12, R-13 / T-12, T-13, T-14.

Residual risk: **High** for claims about real-model security/accuracy.

### 6.4 Secret lifecycle

Current:

```text
Secrets Manager
+ exact-secret IAM
+ no plaintext service-role key in Lambda environment variables
```

Target:

```text
rotation
+ access monitoring
+ compromise/recovery procedure
+ periodic IAM review
```

Related risk: R-09 / T-10, T-19.

Residual risk: **Medium**.

### 6.5 API abuse protection

Current:

```text
API Gateway throttling
+ HTTP 429 evidence
+ 4XX monitoring
```

Target:

```text
verified authentication
+ authentication-aware limits
+ WAF where appropriate
+ abuse analytics
+ containment/response
```

Related risk: R-04 / T-04.

Residual risk: **Medium**.

## 7. Prioritised Action Plan

| Rank | Action | Priority | Why it is prioritised | Prototype Status |
|---:|---|---|---|---|
| 1 | Implement verified API authentication and trusted tenant claims | **P1** | Directly closes identity-spoofing/tenant-context weakness at the public boundary | Not implemented |
| 2 | Establish approved retention/privacy governance and version-aware deletion requirements | **P1** | Sensitive financial/PII lifecycle needs organisational/legal basis | Partially implemented technically |
| 3 | Introduce Infrastructure as Code and configuration-change governance | **P1** | Reduces drift and makes security configuration repeatable/auditable | Not implemented |
| 4 | Define formal incident triage, ownership and escalation | **P1** | Existing alerts need a production response process | Partially implemented |
| 5 | Define and test recovery/restoration capability | **P1** | RECOVER is the weakest Current-Profile area | Partially implemented |
| 6 | Add file-signature validation and malware scanning | **P1** | Current metadata validation cannot detect all malicious/disguised files | Not implemented |
| 7 | Run real-model adversarial and accuracy evaluation | **P1/P2** | Required before production claims about AI integrity/accuracy | Deferred by account/service limitation |
| 8 | Add queue idempotency and replay protection | P2 | Reduces duplicate/forged/replayed processing risk | Partially implemented |
| 9 | Centralise/correlate security telemetry | P2 | Improves detection and investigation across services | Partially implemented |
| 10 | Automate/strengthen secret lifecycle management | P2 | Reduces privileged-credential exposure duration | Partially implemented |
| 11 | Add stronger API abuse protection/WAF where justified | P2 | Complements best-effort API Gateway throttling | Partially implemented |
| 12 | Formalise evidence, RCA and recovery-closure procedures | P2 | Converts project processes into repeatable operational processes | Partially implemented |

## 8. Security Improvement Demonstrated by the Prototype

The gap analysis should not obscure the improvements already achieved.

Before the project security work, the reference workflow primarily required:

```text
upload
→ processing
→ result storage
```

The implemented prototype now adds:

```text
validated upload
→ private encrypted storage
→ least-privilege event processing
→ managed backend secrets
→ failure isolation and DLQs
→ AI-output validation / HITL
→ tenant-aware RLS
→ monitoring and alerting
→ API throttling
→ retention enforcement
→ verified secure deletion
→ documented incident/recovery procedures
```

Two security tests also demonstrated that configuration presence alone was insufficient:

### Cross-tenant RLS test

```text
Initial tenant policy
→ adversarial cross-tenant query
→ FAIL: foreign row visible
→ restrictive policy added
→ same test repeated
→ PASS: 0 foreign rows visible
```

### Alarm notification test

```text
CloudWatch/SNS alarm configuration
→ controlled failure
→ notification failure caused by SNS/KMS authorisation
→ configuration remediated
→ notification retested successfully
```

These findings provide empirical evidence that the framework supports **continuous security improvement**, rather than only static control documentation.

## 9. Stage 9 Conclusion

The Current-to-Target comparison shows that the prototype has established substantial **IDENTIFY, PROTECT, DETECT and RESPOND** capabilities, but important production gaps remain in:

```text
trusted API identity
configuration governance
formal privacy/retention governance
file-content security
real-model assurance
incident operations
event correlation
recovery/restoration
```

The most important conclusion is therefore not that the prototype is “NIST compliant.” The defensible conclusion is:

> The implemented cloud security framework materially improves the security posture of the AI-driven document-processing workflow across selected NIST CSF 2.0 outcomes, while the Current-to-Target Profile comparison identifies clear residual gaps that must be addressed before production deployment.

## 10. Next Evaluation Step

Stage 10 will consolidate the implementation into a final **Security Evaluation Matrix** linking:

```text
FRD/security requirement
→ threat/risk
→ implemented control
→ security test
→ expected result
→ observed result
→ evidence
→ pass/fail
→ residual limitation
→ NIST CSF 2.0 outcome
```

This matrix will provide the principal empirical-results table for the final capstone paper.

## 11. References

National Institute of Standards and Technology (NIST), *The NIST Cybersecurity Framework (CSF) 2.0*, NIST CSWP 29, February 2024, https://doi.org/10.6028/NIST.CSWP.29

National Institute of Standards and Technology (NIST), *Cybersecurity Framework 2.0: Quick-Start Guide for Creating and Using Organizational Profiles*, NIST SP 1301, February 2024, https://doi.org/10.6028/NIST.SP.1301
