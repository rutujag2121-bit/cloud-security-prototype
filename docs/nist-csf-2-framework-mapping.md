# NIST CSF 2.0 Mapping for the AWS Document Processing Workflow

## Purpose

This document maps the implemented AWS-based document processing pipeline to the NIST Cybersecurity Framework 2.0 functions: Govern, Identify, Protect, Detect, Respond, and Recover.

The aim is to show how the cloud security management framework is applied across the AI-driven document lifecycle.

## Current AWS Workflow

```text
API Gateway
→ Upload Lambda
→ S3 raw document storage
→ S3 ObjectCreated event
→ SQS preprocessing queue
→ Pre-processing Lambda
→ SQS extraction queue
→ Extraction Lambda
→ Supabase metadata/results/audit tables
→ CloudWatch trace logs
```
NIST CSF 2.0 Function Mapping
| NIST Function | Meaning in this project                                                                       | Implemented AWS/Supabase controls                                                                                                   | Evidence                                     |
| ------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| Govern        | Define cybersecurity governance, responsibility, policies, and risk approach                  | Security gap analysis, GitHub documentation, evidence log, FRD mapping, NIST mapping                                                | `docs/`, `security/`, evidence README        |
| Identify      | Identify assets, data flows, risks, and dependencies                                          | Asset inventory: API Gateway, Lambda, S3, SQS, Supabase, CloudWatch; document lifecycle table                                       | AWS architecture, Supabase `documents` table |
| Protect       | Protect data, systems, and services                                                           | S3 encryption, Block Public Access, pre-signed URLs, input validation, IAM least privilege, CORS control, file size/type validation | Lambda code, S3 screenshots, IAM templates   |
| Detect        | Detect events, failures, suspicious behaviour, and processing states                          | CloudWatch structured logs, trace IDs, Supabase audit logs, status transitions, DLQ message checks                                  | CloudWatch logs, `audit_logs` table          |
| Respond       | Respond to failed uploads, failed preprocessing, failed extraction, and low-confidence output | Failed document statuses, DLQs, audit events, safe error logging, `needs_human_review` flag                                         | SQS DLQ evidence, audit logs                 |
| Recover       | Recover failed workflow states and support reprocessing/deletion                              | DLQ replay plan, failed status tracking, future secure deletion endpoint, lifecycle recovery documentation                          | DLQ screenshots, future deletion stage       |

