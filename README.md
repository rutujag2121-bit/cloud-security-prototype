# Capisso DEW Cloud Security Prototype

## Project Overview

This repository documents the incremental development of a cloud security management framework for the Capisso.ai Document Extraction Workflow (DEW).

The prototype focuses on securing an event-driven document-processing pipeline for receipts and invoices containing financial information and personally identifiable information. The implementation uses AWS serverless services for upload, storage, orchestration and processing, while Supabase PostgreSQL stores document metadata, processing results and business-level audit records.

The project applies defence-in-depth principles and is being evaluated against the NIST Cybersecurity Framework 2.0.

## Research Objective

The objective is to investigate how recognised cybersecurity controls can be operationalised within an AI-driven document-processing pipeline.

The prototype addresses:

- Secure document upload
- Input and metadata validation
- Private and encrypted object storage
- Least-privilege IAM permissions
- Event-driven processing
- Queue-based failure isolation
- Document lifecycle tracking
- Audit logging and traceability
- Extraction-result confidence handling
- Human-review readiness
- Security-framework mapping
- Threat and risk evaluation

## Current Architecture

```text
Client or API test
→ Amazon API Gateway
→ Upload Lambda
→ Pre-signed S3 PUT URL
→ S3 raw document storage
→ S3 ObjectCreated event
→ Pre-processing SQS queue
→ Pre-processing Lambda
→ Extraction SQS queue
→ Extraction Lambda
→ Supabase processing and audit records
→ CloudWatch structured logs
```
## Implementation Status
| Component                      | Status                | Description                                                                                              |
| ------------------------------ | --------------------- | -------------------------------------------------------------------------------------------------------- |
| API Gateway `/upload` endpoint | Implemented           | Receives document metadata and invokes the upload Lambda                                                 |
| Upload Lambda                  | Implemented           | Validates metadata and generates short-lived S3 pre-signed upload URLs                                   |
| File validation                | Implemented           | Supports PDF, JPEG and PNG with a 10 MB maximum size                                                     |
| Filename sanitisation          | Implemented           | Reduces unsafe object-name handling                                                                      |
| Private S3 storage             | Implemented           | Block Public Access and server-side encryption are enabled                                               |
| Structured S3 object keys      | Implemented           | Documents are organised using company, user and document identifiers                                     |
| Supabase document tracking     | Implemented           | Stores document metadata, status and trace identifiers                                                   |
| Supabase audit logging         | Implemented           | Stores business-level lifecycle and security events                                                      |
| Pre-processing SQS and DLQ     | Implemented           | Provides asynchronous buffering, retries and failure isolation                                           |
| Pre-processing Lambda          | Implemented           | Validates uploaded S3 objects before extraction                                                          |
| Extraction SQS and DLQ         | Implemented           | Separates preprocessing from extraction processing                                                       |
| Extraction Lambda              | Implemented           | Creates processing runs, extraction results and confidence metadata                                      |
| Mock extraction adapter        | Implemented           | Used for deterministic orchestration and security testing                                                |
| HITL readiness flag            | Partially implemented | Low-confidence results can be marked for human review; detailed validation testing remains               |
| NIST CSF 2.0 mapping           | Partially implemented | Initial mapping exists; Current and Target Profiles remain to be completed                               |
| Real AWS model execution       | Deferred              | Textract integration reached the service call but was blocked by the current AWS account plan            |
| Bedrock or SageMaker model     | Planned               | A specific model, prompt, IAM policy and test plan will be documented for later credential-based testing |
| Post-processing validation     | Planned               | Schema, date, currency and financial-consistency checks will be implemented                              |
| CloudWatch alarms              | Planned               | Lambda-error and DLQ-message alarms will be configured                                                   |
| Threat and risk assessment     | Planned               | STRIDE-based threat modelling and a prioritised risk register will be added                              |
| Security evaluation matrix     | Planned               | Security tests will be mapped to NIST CSF 2.0 and FRD requirements                                       |

## Implemented Security Controls
### Upload and API controls
- File-type and extension validation
- Maximum file-size validation
- Filename sanitisation
- Short-lived S3 pre-signed URLs
- Configurable CORS origin
- UUID-based document identifiers
- Structured and non-public S3 object paths

### Storage controls
- S3 Block Public Access
- Server-side encryption
- Restricted raw/ storage prefix
- No credentials or pre-signed URLs committed to GitHub

### Identity and access controls
- Separate Lambda execution roles
- Least-privilege IAM policy templates
- S3 access limited to required prefixes
- SQS permissions limited to the appropriate processing queues

### Processing and resilience controls
- Event-driven S3-to-SQS workflow
- Separate preprocessing and extraction queues
- Dead-letter queues
- Controlled retry behaviour
- Status transitions stored in Supabase

### Logging and traceability controls
- Structured CloudWatch logs
- Trace IDs across processing stages
- Supabase audit events
- Processing-run records
- No document contents intentionally written to CloudWatch

### Mock Extraction Rationale
The mock extraction adapter was introduced to test the pipeline independently of model availability, billing requirements and model-specific behaviour.

It validates:

- SQS-to-Lambda orchestration
- Processing-run creation
- Extraction-result persistence
- Confidence-score handling
- Document-status transitions
- Human-review flags
- Audit-event creation
- CloudWatch trace continuity

The mock output is not presented as evidence of real AI extraction accuracy.

## Real Model Integration Status

Amazon Textract AnalyzeExpense was investigated as an AWS-native receipt and invoice extraction service.
The extraction Lambda successfully reached the Textract API call, but AWS returned a SubscriptionRequiredException. The AWS console confirmed that the current free account plan restricts access to the required service.

Following project-lead guidance, paid model execution has been deferred until suitable credentials are provided.
The next model-related deliverable is therefore to document:

- The selected Bedrock or SageMaker model
- Model-selection criteria
- Proposed invocation workflow
- Required IAM permissions
- Secure extraction prompt
- Expected JSON output schema
- Test dataset and evaluation metrics

 ## NIST CSF 2.0 Alignment
The framework is being organised around the six NIST CSF 2.0 Functions:

- Govern
- Identify
- Protect
- Detect
- Respond
- Recover

The existing function-level mapping will be extended into:

- A Current Profile
- A Target Profile
- A security gap analysis
- A prioritised implementation plan
- Evidence references
- Residual-risk documentation

## Remaining Capstone Work

The remaining work focuses on security evaluation and framework validation rather than adding unrelated cloud services.

Priority deliverables are:

1. Select and document the proposed Bedrock or SageMaker model.
2. Create a formal threat model and risk register.
3. Develop the NIST CSF 2.0 Current and Target Profiles.
4. Implement post-processing validation.
5. Demonstrate low-confidence human-review routing.
6. Configure CloudWatch alarms and document the DLQ response procedure.
7. Run a controlled security test matrix.
8. Map the implementation and test results to the NIST CSF 2.0 and FRD security requirements.
9. Use the implementation and evaluation findings in the final research paper.

## Repository Structure

```text
api-gateway/
    API Gateway configuration documentation

database/
    Supabase database schemas

docs/
    Stage documentation, progress logs, framework mapping and evidence index

lambda/
    upload/
    preprocess/
    extraction/

security/
    IAM policy templates and security-control documentation

test-events/
    Valid and invalid Lambda and SQS test events

README.md
```

## Evidence Handling

Implementation screenshots are primarily stored in a private local evidence folder.
The public repository does not intentionally contain:

- AWS access keys
- Supabase service-role keys
- Environment files
- Complete pre-signed URLs
- Real financial documents
- Screenshots exposing sensitive account or credential details

The public docs/evidence/README.md file provides an evidence index without publishing confidential configuration.

## Current Limitation
The current prototype demonstrates the secured AWS pipeline and mock-based extraction orchestration. It does not claim successful real-model extraction, production readiness, complete GDPR compliance or a completed human-review interface.
