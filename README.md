# Capisso DEW Cloud Security Prototype

## Project Overview

This repository documents the incremental development of a cloud security management framework for the Capisso.ai Document Extraction Workflow (DEW).

The prototype secures an event-driven document-processing pipeline for receipts and invoices containing financial information and personally identifiable information. AWS serverless services provide upload, storage, orchestration and processing, while Supabase PostgreSQL stores document metadata, processing results, validation evidence, Human-in-the-Loop review tasks and business-level audit records.

The project applies defence-in-depth principles and is being evaluated against the NIST Cybersecurity Framework 2.0.

## Research Objective

The objective is to investigate how recognised cybersecurity controls can be operationalised within an AI-driven document-processing pipeline.

The prototype addresses secure document upload, private storage, least-privilege access, event-driven processing, queue-based failure isolation, lifecycle tracking, audit logging, AI-output validation, Human-in-the-Loop routing, threat evaluation and framework mapping.

## Current Architecture

```text
Client or API test
→ Amazon API Gateway
→ Upload Lambda
→ Pre-signed S3 PUT URL
→ Private S3 raw document storage
→ S3 ObjectCreated event
→ Pre-processing SQS queue and DLQ
→ Pre-processing Lambda
→ Extraction SQS queue and DLQ
→ Extraction Lambda
→ Post-processing validator
→ Supabase results, validation evidence and review tasks
→ CloudWatch structured logs
```

## Development Stages

| Stage | Name | Status |
|---|---|---|
| 0 | API Gateway and Lambda prototype | Completed |
| 1 | Secure S3 upload | Completed and tested |
| 2 | Supabase metadata and audit logging | Completed and tested |
| 3 | Event-driven preprocessing | Completed and tested |
| 4 | Mock extraction pipeline | Completed and tested |
| 5A | Real model service attempt | Attempted; blocked by AWS account restrictions |
| 5B | Secure AI model adapter design | Design completed; real invocation deferred |
| 5C | Post-processing validation and HITL routing | Completed and tested |
| 6 | Monitoring, alerting and incident response | Completed and tested |
| 7 | Retention and secure deletion | Next implementation stage |

## Implementation Status

| Component | Status | Description |
|---|---|---|
| API Gateway `/upload` endpoint | Implemented | Receives document metadata and invokes the upload Lambda |
| Upload Lambda | Implemented | Validates metadata and generates short-lived S3 pre-signed upload URLs |
| File validation | Implemented | Supports PDF, JPEG and PNG with a 10 MB maximum size |
| Filename sanitisation | Implemented | Reduces unsafe object-name handling |
| Private S3 storage | Implemented | Block Public Access and server-side encryption are enabled |
| Structured S3 object keys | Implemented | Uses company, user and document identifiers |
| Supabase document tracking | Implemented | Stores document lifecycle status and trace identifiers |
| Supabase audit logging | Implemented | Stores business-level lifecycle and security events |
| Pre-processing SQS and DLQ | Implemented | Provides buffering, retries and failure isolation |
| Pre-processing Lambda | Implemented | Validates uploaded S3 objects before extraction |
| Extraction SQS and DLQ | Implemented | Separates preprocessing from extraction |
| Extraction Lambda | Implemented | Creates processing runs, extraction results and validation evidence |
| Mock extraction adapter | Implemented | Supports deterministic orchestration and security testing |
| Real Textract service attempt | Attempted | Service invocation was blocked by account-plan restrictions |
| Bedrock model adapter | Designed | Nova Lite prompt, schema, IAM template and test plan are prepared |
| Post-processing validation | Implemented | Validates schema, fields, dates, currency, totals and line items |
| Human-in-the-Loop routing | Implemented | Creates prioritised review tasks for uncertain or unsafe output |
| Stage 5C security scenarios | Tested | Six deterministic validation scenarios completed |
| Threat and risk assessment | Implemented | STRIDE threat model and prioritised risk register documented |
| NIST CSF 2.0 mapping | Partially implemented | Current and Target Profiles remain |
| CloudWatch alarms | Planned | Lambda-error and DLQ-message alarms are next |
| Secure deletion workflow | Planned | Retention and deletion controls remain |
| Tenant-aware RLS | Planned | Backend RLS is enabled; tenant policies remain |
| Security evaluation matrix | In progress | Stage 5C evidence is complete |
| SNS security notification channel | Implemented | Confirmed email delivery for CloudWatch alarms |
| Lambda error monitoring | Implemented | Upload, preprocessing and extraction error alarms |
| DLQ monitoring | Implemented | Preprocessing and extraction visible-message alarms |
| Retry-exhaustion test | Completed | Invalid extraction message moved automatically to the DLQ |
| Incident-response runbook | Implemented | Investigation, replay decision and recovery procedure documented |

## Implemented Security Controls

### Upload and API controls

- File-type and extension validation
- Maximum file-size validation
- Filename sanitisation
- Short-lived S3 pre-signed URLs
- Configurable CORS origin
- UUID-based document identifiers
- Structured, non-public S3 object paths

### Storage and access controls

- S3 Block Public Access
- Server-side encryption
- Restricted `raw/` storage prefix
- Separate Lambda execution roles
- Least-privilege IAM policy templates
- Restricted S3 and SQS permissions
- No credentials or complete pre-signed URLs committed to GitHub

### Processing and resilience controls

- Event-driven S3-to-SQS workflow
- Separate preprocessing and extraction queues
- Dead-letter queues
- Controlled retry behaviour
- Supabase lifecycle transitions
- Replaceable extraction-provider boundary

### Logging and traceability controls

- Structured CloudWatch logs
- Trace IDs across processing stages
- Supabase audit events
- Processing-run records
- Validation timestamps and review reasons
- No document contents intentionally written to CloudWatch

### Post-processing and AI-output controls

- Versioned extraction schema
- Required-field and type validation
- ISO date and currency-format validation
- Financial-total and line-item consistency checks
- Overall and field-level confidence thresholds
- Model uncertainty handling
- Pattern-based prompt-injection indicator detection
- Malformed-output rejection
- Human-review task creation and prioritisation
- Validation evidence stored in Supabase
- Post-processing audit traceability

## AI Model Integration

### Stage 5A — Real-service attempt

Amazon Textract `AnalyzeExpense` was investigated as an AWS-native receipt and invoice extraction service.

The extraction Lambda reached the service invocation point, but AWS returned `SubscriptionRequiredException`. The current account plan did not provide the required billing-enabled access. Real extraction was therefore not completed.

### Stage 5B — Secure adapter design

Amazon Nova Lite was selected as the proposed Bedrock model for later credential-based testing.

Prepared artefacts include:

- `security/iam-bedrock-extraction-policy-template.json`
- `security/README-bedrock-policy.md`
- `prompts/bedrock-receipt-extraction-prompt.md`
- `prompts/receipt-extraction-schema.json`
- `docs/stage-5b-secure-model-adapter-design.md`

The design treats each model response as untrusted input and passes it through Stage 5C validation.

### Mock extraction rationale

The deterministic mock adapter supports repeatable testing of orchestration, result persistence, confidence handling, status transitions, validation controls, review-task creation, audit events and CloudWatch trace continuity.

The mock output is not presented as evidence of real AI extraction accuracy.

## Stage 5C Validation Results

| Scenario | Expected decision | Result |
|---|---|---|
| Valid output | Complete automatically | Passed |
| Low confidence | Medium-priority review | Passed |
| Missing required field | High-priority review | Passed |
| Financial mismatch | High-priority review | Passed |
| Prompt-injection indicator | High-priority review | Passed |
| Malformed output | Mark invalid and create high-priority review | Passed |

These tests evaluate security-control behaviour and orchestration. They do not measure real-model extraction accuracy.

## NIST CSF 2.0 Alignment

The framework is organised around Govern, Identify, Protect, Detect, Respond and Recover.

The remaining framework work includes a Current Profile, Target Profile, gap analysis, prioritised actions, evidence mapping and residual-risk mapping.

## Remaining Capstone Work

1. Configure CloudWatch alarms for Lambda errors and DLQ messages.
2. Document and test the DLQ investigation and replay procedure.
3. Implement a controlled retention and secure-deletion workflow.
4. Strengthen secret-management and rotation guidance.
5. Define and test tenant-aware Supabase RLS requirements.
6. Configure API Gateway throttling and abuse controls.
7. Complete the NIST CSF 2.0 Current and Target Profiles.
8. Complete the security evaluation matrix.
9. Run a bounded real-model experiment when suitable credentials are available.
10. Use the implementation and evaluation findings in the final research paper.

## Repository Structure

```text
api-gateway/
database/
docs/
lambda/
    upload/
    preprocess/
    extraction/
prompts/
security/
test-events/
README.md
```

## Evidence Handling

Implementation screenshots are primarily stored in a private local evidence folder.

The public repository does not intentionally contain AWS access keys, Supabase service-role keys, environment files, complete pre-signed URLs, real financial documents or screenshots exposing sensitive account details.

## Current Limitations

The prototype does not claim successful real-model extraction, measured AI accuracy, production readiness, complete GDPR compliance, complete tenant authentication, a finished reviewer interface or comprehensive prompt-injection prevention.

The current implementation demonstrates a secured event-driven pipeline, deterministic AI-output security controls and a documented path for later real-model integration.
