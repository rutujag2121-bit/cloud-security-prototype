# STRIDE Threat Model

## 1. Purpose

This document identifies cybersecurity threats affecting the AWS-based AI document-processing prototype.

The threat model covers the complete document lifecycle:

```text
Upload
→ Object storage
→ Pre-processing
→ Extraction
→ Post-processing
→ Result storage
→ Human review
→ Retention and deletion
```
The analysis uses the STRIDE methodology:
| Category               | Meaning                                                    |
| ---------------------- | ---------------------------------------------------------- |
| Spoofing               | Pretending to be another user, service or system           |
| Tampering              | Unauthorised modification of data or processing messages   |
| Repudiation            | Denying an action where sufficient evidence is unavailable |
| Information Disclosure | Exposure of confidential or personal information           |
| Denial of Service      | Preventing or degrading legitimate system operation        |
| Elevation of Privilege | Obtaining permissions beyond those authorised              |

## 2. System Scope

The threat model covers:

- Amazon API Gateway
- Upload Lambda
- Amazon S3
- Pre-processing SQS queue and DLQ
- Pre-processing Lambda
- Extraction SQS queue and DLQ
- Extraction Lambda
- Planned Amazon Bedrock or SageMaker model
- Supabase PostgreSQL
- CloudWatch logs
- Human-review workflow
- GitHub source repository
The frontend application and full production authentication interface are outside the implemented prototype scope.

## 3. Security-Sensitive Assets
| Asset                      | Security importance                                        |
| -------------------------- | ---------------------------------------------------------- |
| Receipt and invoice files  | May contain PII, financial and confidential business data  |
| Extracted financial fields | Incorrect or altered values may affect financial reporting |
| S3 object keys             | Identify document ownership and workflow location          |
| Document IDs and trace IDs | Support workflow integrity and forensic traceability       |
| Supabase service-role key  | Provides privileged database access                        |
| Lambda execution roles     | Control access to S3, SQS, logs and model services         |
| Pre-signed URLs            | Provide temporary document-upload authority                |
| SQS messages               | Control asynchronous processing operations                 |
| Model prompts and schemas  | Control model behaviour and output structure               |
| Audit logs                 | Provide evidence for investigation and compliance          |
| Model output               | Must not be trusted without validation                     |

## 4. Trust Boundaries
TB-01: User to API Gateway
Untrusted user-supplied document metadata enters the AWS backend.

TB-02: API Gateway to Upload Lambda
API Gateway invokes trusted backend code, but authentication and request validation must be enforced.

TB-03: Client to S3 pre-signed upload
A temporary URL permits direct upload to a restricted S3 object key.

TB-04: S3 to SQS
An S3 object-created event generates an asynchronous processing message.

TB-05: SQS to Lambda
Queue messages cross into trusted preprocessing and extraction functions.

TB-06: AWS Lambda to Supabase
AWS functions send metadata, status and audit information to an external managed database.

TB-07: Extraction Lambda to AI model
The uploaded document is sent to a model service and an untrusted model response is returned.

TB-08: Automated processing to human review
Low-confidence or invalid output is transferred to a human-review workflow.

## 5. Threat Catalogue
| ID   | STRIDE                                          | Component           | Threat scenario                                                                                      | Potential impact                                                        | Existing controls                                                               | Remaining gap                                                                           |
| ---- | ----------------------------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| T-01 | Spoofing                                        | API Gateway         | An unauthenticated attacker requests upload URLs while pretending to be a legitimate user or company | Unauthorised uploads, resource consumption and false ownership metadata | UUID document identifiers, metadata validation and structured object keys       | Production authentication and verified company/user identity are not implemented        |
| T-02 | Spoofing / Tampering                            | Pre-signed URL      | A leaked URL is used by another party or reused before expiry                                        | Unauthorised object upload or replacement                               | Short expiry, fixed bucket/key and content type                                 | No one-time-use enforcement or authenticated uploader binding                           |
| T-03 | Tampering                                       | File upload         | A malicious file is disguised as a PDF, JPEG or PNG using a misleading extension or content type     | Malware storage, parser exploitation or invalid model processing        | Extension, MIME type and size validation                                        | File-signature validation and malware scanning remain pending                           |
| T-04 | Denial of Service                               | API and S3          | An attacker generates many upload requests or large uploads                                          | Cost increase, Lambda throttling and processing backlog                 | 10 MB limit and asynchronous queues                                             | API throttling, quotas and WAF controls remain pending                                  |
| T-05 | Information Disclosure                          | S3                  | Bucket policy or access settings accidentally expose uploaded documents                              | PII and financial-data breach                                           | Block Public Access, private bucket and server-side encryption                  | Automated configuration-compliance checking is not implemented                          |
| T-06 | Elevation of Privilege                          | IAM                 | A Lambda role receives excessive permissions or is compromised                                       | Access to unrelated buckets, queues, logs or models                     | Separate execution roles and restricted IAM templates                           | Formal periodic IAM review is not automated                                             |
| T-07 | Tampering / Spoofing                            | SQS                 | A forged, altered or replayed queue message references another document                              | Incorrect processing, duplicate results or cross-document access        | Restricted SQS permissions, structured message fields and document IDs          | Message schema validation, replay detection and idempotency controls need strengthening |
| T-08 | Repudiation                                     | Processing pipeline | A processing operation cannot be reliably linked to its initiating event                             | Weak forensic evidence and inability to investigate failures            | Trace IDs, processing-run records, audit logs and CloudWatch                    | Authentication events and end-user identity verification remain incomplete              |
| T-09 | Information Disclosure                          | CloudWatch          | Document text, PII, credentials or pre-signed URLs are written to logs                               | Confidential information exposure                                       | Structured safe logs and no intentional document-body logging                   | Automated sensitive-log scanning is not implemented                                     |
| T-10 | Elevation of Privilege / Information Disclosure | Supabase            | The Supabase service-role key is exposed or misused                                                  | Full database read/write access and tenant-data exposure                | Environment variables and exclusion of secrets from GitHub                      | Secrets Manager integration and key rotation remain pending                             |
| T-11 | Information Disclosure                          | Database            | Missing or incorrect row-level policies expose one company’s records to another                      | Cross-tenant data breach                                                | Company and user identifiers stored; RLS enabled in schema                      | Complete production RLS policies are not demonstrated                                   |
| T-12 | Tampering                                       | AI model            | A document contains prompt-injection text instructing the model to ignore extraction rules           | Manipulated output, leaked instructions or false data                   | Fixed server-side prompt, untrusted-document instruction and strict JSON schema | Real-model adversarial testing is deferred until credentials are available              |
| T-13 | Tampering / Repudiation                         | AI output           | The model hallucinates supplier, date, currency or total values                                      | Incorrect financial records and unreliable automated decisions          | Planned schema validation, uncertain-fields list and HITL routing               | Post-processing validation must be implemented                                          |
| T-14 | Tampering                                       | Confidence handling | Low-confidence or invalid output is incorrectly accepted as completed                                | Incorrect information bypasses human review                             | `needs_human_review` field and status support                                   | Deterministic low-confidence testing is still required                                  |
| T-15 | Denial of Service                               | SQS and Lambda      | Repeated failures create retries, queue backlog or poison messages                                   | Processing delay and resource consumption                               | DLQs and retry limits                                                           | DLQ alarms and operational replay procedure remain pending                              |
| T-16 | Information Disclosure / Repudiation            | Data lifecycle      | Documents remain stored longer than required or cannot be deleted on request                         | GDPR and data-retention non-compliance                                  | Lifecycle statuses include deletion planning                                    | Retention rules and controlled deletion workflow remain pending                         |
| T-17 | Tampering                                       | GitHub              | Secrets, account identifiers or sensitive screenshots are committed publicly                         | Credential compromise and infrastructure exposure                       | `.gitignore`, placeholders and sanitised evidence policy                        | Repository scanning should be conducted before final submission                         |
| T-18 | Denial of Service / Repudiation                 | Monitoring          | Failures occur without alarms or timely investigation                                                | Extended outage and incomplete incident response                        | CloudWatch logs and Supabase audit records                                      | CloudWatch alarms and incident runbook remain pending                                   |

## The following threats require the highest priority before the final evaluation:

1. T-01 — Missing production authentication.
2. T-03 — Malicious or disguised uploaded files.
3. T-04 — API abuse and cost-based denial of service.
4. T-10 — Supabase service-role credential compromise.
5. T-11 — Incomplete tenant isolation.
6. T-12 — Document prompt injection.
7. T-13 — Hallucinated or invalid financial output.
8. T-16 — Missing retention and deletion enforcement.

## 7. Threat Treatment Strategy
| Treatment | Meaning in this project                                     |
| --------- | ----------------------------------------------------------- |
| Mitigate  | Implement a control reducing likelihood or impact           |
| Avoid     | Disable or exclude an unsafe feature                        |
| Transfer  | Rely on contractual or managed-service responsibility       |
| Accept    | Document residual risk where implementation is not feasible |
Advanced controls not completed within the prototype will be explicitly recorded as accepted residual risks or future work.

## 8. Relationship to the Security Framework

The threat model supports:
- Govern: risk ownership, policies and priorities
- Identify: assets, threats, dependencies and vulnerabilities
- Protect: validation, encryption, IAM and access control
- Detect: audit logs, CloudWatch and anomaly monitoring
- Respond: DLQs, failed statuses and incident procedures
- Recover: replay, reprocessing and controlled restoration

## 9. Current Limitations

The threat model describes both implemented and planned controls.
It does not claim that the prototype currently provides:
- Complete user authentication
- Complete tenant isolation
- Malware scanning
- Real-model adversarial testing
- Production incident response
- Automated GDPR compliance
- A complete HITL interface
  
