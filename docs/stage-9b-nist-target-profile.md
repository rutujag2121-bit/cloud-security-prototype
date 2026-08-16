# Stage 9B — NIST CSF 2.0 Target Profile

## 1. Purpose

This document defines the **Target Profile** for the Capisso DEW cloud security prototype. It uses the same selected NIST CSF 2.0 outcomes assessed in the Stage 9A Current Profile so that the current and desired security postures can be compared directly in Stage 9C.

The Target Profile represents a realistic **production-oriented security state** for the document-processing workflow. It does not assert that all target controls have been implemented in the prototype.

NIST CSF 2.0 defines a Target Profile as the desired Core outcomes selected and prioritised for achieving cybersecurity risk-management objectives. The target therefore reflects the improvements required to reduce the residual risks identified after Stages 0–8.

## 2. Target-Profile Scope

The Target Profile covers the same lifecycle as the Current Profile:

```text
Authenticated client
→ API Gateway / protected API boundary
→ Upload Lambda
   ↘ AWS Secrets Manager
→ Private S3 storage
→ Event-driven preprocessing
→ Extraction/model boundary
→ Post-processing security validation / HITL
→ Tenant-isolated data store
→ Monitoring / incident response
→ Retention / verified secure deletion
→ Recovery and continuous improvement
```

The target state assumes the prototype is being hardened toward a production deployment handling sensitive invoice/receipt data.

## 3. Priority Method

| Priority | Meaning |
|---|---|
| **P1 — High** | Important residual risk or production prerequisite; should be addressed before production use |
| **P2 — Medium** | Material improvement that should follow the P1 controls |
| **P3 — Maintain** | Outcome is already materially achieved; target is to maintain, automate or periodically validate it |

Priority reflects this project’s threat model, risk register, FRD security expectations and Stage 0–8 evaluation evidence. It is not a NIST maturity score.

## 4. Target Profile

| CSF 2.0 Subcategory | Target State | Priority | Target implementation / evidence expectation |
|---|---|---|---|
| **GV.OC-03** | **Achieved** | **P1** | Maintain a documented legal/privacy requirement register covering GDPR-relevant processing, retention, deletion, breach handling and processor responsibilities; obtain stakeholder/legal approval for production retention periods |
| **GV.RM-06** | **Achieved** | **P3** | Retain the defined likelihood × impact method; review scoring criteria periodically and apply the method consistently to new risks |
| **GV.OV-03** | **Achieved** | **P2** | Establish recurring security-control reviews using the NIST profile, risk register, alarms, incidents and test results; record remediation ownership and closure |
| **ID.AM-02** | **Achieved** | **P3** | Maintain an authoritative inventory of AWS/Supabase services, Lambda functions, queues, secrets, data stores and external dependencies; automate inventory where practical |
| **ID.AM-03** | **Achieved** | **P3** | Maintain current architecture/data-flow diagrams and trust boundaries as the workflow changes |
| **ID.AM-07** | **Achieved** | **P2** | Maintain a data inventory/classification for uploaded documents, extracted financial data, identifiers, audit data and deletion evidence; document sensitivity and retention requirements |
| **ID.AM-08** | **Achieved** | **P1** | Govern the full data lifecycle using approved retention schedules, automated enforcement, verified deletion and version-aware object deletion where versioning is enabled |
| **ID.RA-03** | **Achieved** | **P3** | Review the STRIDE threat model after architecture/model changes and incorporate relevant cloud/AI threat intelligence |
| **ID.RA-04** | **Achieved** | **P2** | Reassess likelihood/impact after significant control or threat changes and record residual risk rather than only inherent risk |
| **ID.RA-05** | **Achieved** | **P2** | Use residual-risk results to prioritise remediation, funding and release decisions |
| **ID.IM-01** | **Achieved** | **P3** | Continue documenting improvements produced by incidents, security findings and operational reviews |
| **ID.IM-02** | **Achieved** | **P2** | Establish a repeatable security-test suite covering tenant isolation, queue failure, deletion, API abuse, model-output integrity, authentication and recovery |
| **PR.AA-03** | **Achieved** | **P1** | Replace caller-supplied identity trust with verified production authentication; validate JWT issuer/audience/signature and derive `userId`/`companyId` from trusted claims at the API boundary |
| **PR.AA-05** | **Achieved** | **P1** | Preserve least privilege and separation of duties; periodically review IAM/RLS; minimise privileged service-role use; add explicit authorisation checks for destructive/administrative actions |
| **PR.DS-01** | **Achieved** | **P2** | Maintain private encrypted storage, tenant isolation and lifecycle controls; define key-management requirements and verify backup/versioned-object treatment |
| **PR.DS-02** | **Achieved** | **P3** | Enforce HTTPS/TLS for all external and service-to-service connections and periodically verify configuration |
| **PR.PS-01** | **Achieved** | **P1** | Move critical cloud security configuration toward Infrastructure as Code and automated configuration validation; require reviewed changes for IAM, queues, alarms, API controls, retention and deletion |
| **PR.PS-04** | **Achieved** | **P2** | Maintain structured security logging while reducing unnecessary sensitive metadata; define retention and integrity requirements; centralise logs for correlation |
| **PR.IR-03** | **Achieved** | **P2** | Define resilience objectives, queue/backlog thresholds, replay controls and tested recovery procedures; consider multi-AZ/service dependency failure scenarios |
| **DE.CM-09** | **Achieved** | **P2** | Expand monitoring to authentication failures, suspicious access patterns, unusual queue/backlog behaviour, secret-access anomalies and lifecycle-control failures |
| **DE.AE-02** | **Achieved** | **P2** | Define repeatable investigation procedures and severity criteria for detected adverse events |
| **DE.AE-03** | **Achieved** | **P2** | Centralise and correlate API Gateway, Lambda, CloudWatch, Supabase, IAM/CloudTrail and application security events through SIEM/security analytics or an equivalent correlation mechanism |
| **RS.MA-02** | **Achieved** | **P1** | Establish incident severity/triage criteria, ownership, escalation paths and evidence requirements; connect alerts to a managed incident process |
| **RS.AN-03** | **Achieved** | **P2** | Formalise root-cause analysis for security incidents and recurring failure patterns; link corrective actions to the risk register |
| **RS.AN-06** | **Achieved** | **P2** | Protect incident/audit evidence integrity, access and retention; maintain provenance for investigation artefacts |
| **RS.MI-01** | **Achieved** | **P2** | Add containment playbooks for compromised credentials, abusive clients, poisoned messages, cross-tenant attempts and unsafe model behaviour; automate safe containment where feasible |
| **RC.RP-02** | **Achieved** | **P1** | Define and test recovery procedures for failed processing, queue replay, service/credential failures and data-service outages; establish RTO/RPO where applicable |
| **RC.RP-05** | **Achieved** | **P1** | Verify restored system/data integrity through controlled recovery tests, including application/database restoration where backups are part of the production design |
| **RC.RP-06** | **Achieved** | **P2** | Define documented recovery-completion criteria and post-incident review requirements |

## 5. Target Security Capabilities

| Capability | Current prototype position | Target |
|---|---|---|
| API identity | Caller supplies prototype user/company fields | Verified JWT/OIDC identity; tenant identity derived from trusted claims |
| Tenant authorisation | RLS tested and restrictive document policy added | End-to-end tenant authorisation from API through database, with periodic negative testing |
| File security | Extension/MIME/size checks | File-signature validation and malware scanning before downstream processing |
| API abuse protection | API Gateway throttling + 4XX monitoring | Authentication-aware limits, AWS WAF/rules as appropriate, abuse analytics and response |
| Secrets | Secrets Manager + exact-secret IAM | Automated/managed rotation, access monitoring and credential-recovery procedure |
| Cloud configuration | Manually configured and documented | Infrastructure as Code, peer-reviewed changes and automated configuration checks |
| Queue integrity | IAM, retries, DLQs | Strong message schema validation, idempotency keys and safe automated/manual replay |
| AI/model security | Secure adapter design + deterministic validation/HITL | Real-model adversarial tests, prompt-injection evaluation, threshold calibration and model-security monitoring |
| Logging | Structured CloudWatch + Supabase audit | Central correlation/SIEM, sensitive-log controls, defined retention/integrity requirements |
| Incident response | Alarms, SNS, DLQ runbook | Severity model, ownership/escalation, containment playbooks and formal post-incident review |
| Data lifecycle | Scheduled retention + verified deletion | Legally approved retention schedule, version-aware deletion and periodic deletion-control audit |
| Recovery | Manual recovery/replay evidence | Defined RTO/RPO where relevant, tested restoration/recovery and completion criteria |

## 6. P1 Priority Actions

### P1-01 — Verified API authentication and trusted tenant identity

**Addresses:** PR.AA-03, PR.AA-05, R-01/T-01

Current limitation:

```text
POST /upload accepts prototype userId/companyId values from the request.
```

Target:

```text
Verified JWT/OIDC token
→ API authorisation
→ company/user identity derived from trusted claims
→ backend processing
→ matching RLS tenant boundary
```

Success evidence would include:
- invalid/missing token rejected;
- modified tenant field cannot override authenticated company;
- Tenant A cannot create/read Tenant B records;
- valid Tenant A request succeeds.

### P1-02 — Production data-lifecycle governance

**Addresses:** GV.OC-03, ID.AM-08, R-15/T-16/T-20

Target:
- approved retention policy rather than a prototype-only 30-day value;
- version-aware S3 deletion if versioning is used;
- periodic deletion verification;
- documented lawful/business retention basis.

### P1-03 — Security configuration as controlled code

**Addresses:** PR.PS-01

Target:
- deploy critical API/IAM/SQS/alarm/retention configuration through Infrastructure as Code;
- review configuration changes through source control;
- prevent uncontrolled console drift;
- use automated security/configuration checks.

### P1-04 — Formal incident management

**Addresses:** RS.MA-02

Target:
- severity classification;
- named owner/escalation route;
- alert-to-incident workflow;
- evidence collection requirements;
- response deadlines;
- documented closure/post-incident review.

### P1-05 — Tested recovery capability

**Addresses:** RC.RP-02 and RC.RP-05

Target:
- define what must be recoverable;
- establish RTO/RPO where relevant;
- test queue replay and service/database recovery;
- verify integrity after restoration;
- document test results and remediation.

## 7. Important Target Controls Supporting Existing Risks

### File-content security
Add:
- magic-byte/file-signature verification;
- malware scanning/quarantine;
- reject/quarantine workflow.

### Queue idempotency and replay control
Add:
- message schema/version validation;
- idempotency key/document-processing state check;
- duplicate detection;
- safe replay tooling.

### Real-model security evaluation
When credentials/service access permit:
- invoke the selected real model through the secure adapter;
- test clean documents and adversarial documents;
- test prompt-injection scenarios;
- measure malformed-output rate;
- evaluate HITL trigger behaviour;
- separately evaluate extraction accuracy against labelled ground truth.

### WAF / stronger API abuse controls
Evaluate:
- AWS WAF managed/custom rules where appropriate;
- authentication-aware rate limits;
- source/reputation controls;
- abuse dashboards and alert thresholds.

## 8. Target Profile Summary

The desired target is not “more AWS services.” It is a transition from a successfully tested security prototype to a **repeatable, authenticated, continuously evaluated and recoverable production security posture**.

The most important target-state themes are:

```text
Trusted identity
→ least privilege
→ secure content ingestion
→ controlled configuration
→ real-model assurance
→ correlated detection
→ formal incident response
→ verified recovery
→ governed data lifecycle
→ continuous reassessment
```

## 9. Relationship to the Current Profile

Stage 9A documented the **as-is** state.

This Stage 9B document defines the **to-be** state.

Stage 9C will compare the two profiles outcome by outcome and produce:
1. the security gap;
2. the associated threat/risk;
3. priority;
4. recommended action;
5. implementation status;
6. residual risk;
7. evidence supporting the assessment.

## 10. References

National Institute of Standards and Technology (NIST), *The NIST Cybersecurity Framework (CSF) 2.0*, NIST CSWP 29, February 2024, https://doi.org/10.6028/NIST.CSWP.29

National Institute of Standards and Technology (NIST), *Cybersecurity Framework 2.0: Quick-Start Guide for Creating and Using Organizational Profiles*, NIST SP 1301, February 2024, https://doi.org/10.6028/NIST.SP.1301
