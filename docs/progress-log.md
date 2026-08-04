# Progress Log

## Stage 0: AWS API Gateway and Lambda Prototype

Completed:

- Created AWS REST API using API Gateway.
- Created `/upload` resource.
- Added POST method under `/upload`.
- Created `document-processing-upload-lambda`.
- Implemented file metadata validation.
- Added allowed file types: PDF, JPEG, PNG.
- Added file size validation.
- Added filename safety validation.
- Generated unique `jobId` using UUID.
- Tested Lambda directly.
- Tested API Gateway `/upload` POST method successfully.

Test result:

- API Gateway invoked Lambda successfully.
- Lambda returned `statusCode: 201`.
- Response included generated `jobId`.
- Initial processing status returned as `received`.

Issue encountered:

- Initial Lambda code expected request data inside `event["body"]`.
- API Gateway test passed JSON fields directly in the event object.
- Lambda code was updated to support both formats.

---

## Stage 1: Secure Upload Upgrade — S3 Pre-signed URL Flow

Completed:

- Created dedicated S3 bucket for document storage.
- Added S3 prefixes: `raw/`, `processed/`, `rejected/`, and `audit-artifacts/`.
- Enabled S3 Block Public Access.
- Enabled default S3 server-side encryption.
- Added Lambda environment variables for bucket name, upload prefix, max file size, CORS origin, and pre-signed URL expiry.
- Added least-privilege IAM policy allowing the upload Lambda to put objects only into the S3 `raw/` prefix.
- Updated Lambda code to validate metadata and generate a pre-signed S3 upload URL.
- Increased file size limit from 5 MB to 10 MB.
- Replaced wildcard CORS design with configurable allowed origins.
- Added safe structured logs with trace IDs.
- Added test events for valid upload, invalid file type, oversized file, and extension mismatch.

Security value:

- Documents are uploaded directly to S3 rather than through Lambda as large payloads.
- Upload URLs are short-lived.
- The S3 object path is structured by company ID, user ID, and document ID.
- Public access is blocked at the bucket level.
- Storage encryption is enabled.

---

## Stage 1 Validation: S3 Upload Test

Completed:

- A valid upload initiation request was tested through AWS Lambda.
- Lambda returned `statusCode: 201`.
- Lambda generated a `documentId`.
- Lambda created a structured S3 object key.
- Lambda returned a pre-signed S3 PUT URL.
- The pre-signed URL was tested in Postman.
- Postman upload returned `200 OK`.
- The file appeared under the S3 `raw/` prefix.

Postman upload configuration:

- Method: `PUT`
- Header: `Content-Type: application/pdf`
- Body: binary PDF file

Security significance:

- The full pre-signed URL is not committed to GitHub.
- The document is uploaded directly to protected S3 storage.
- The object path supports lifecycle tracking.

---

## Stage 1 Validation: Upload Rejection Tests

Completed using repository test events:

- `test-events/invalid-file-type.json`
- `test-events/oversized-file.json`
- `test-events/extension-mismatch.json`

All rejection cases returned the expected `400` response.

Security significance:

- Unsupported executable-style files are rejected.
- Files over the 10 MB limit are rejected.
- Mismatched file extension and content type combinations are rejected.
- Lambda only generates S3 pre-signed upload URLs for valid PDF, JPEG, or PNG metadata.

---

## Stage 2: Supabase Metadata and Audit Logging

Completed:

- Created Supabase `documents` table.
- Created Supabase `audit_logs` table.
- Added schema file to `database/supabase-schema.sql`.
- Added Supabase URL and service role key as Lambda environment variables.
- Updated upload Lambda to insert document metadata.
- Updated upload Lambda to insert an `UPLOAD_INITIATED` audit event.
- Stored `trace_id` in Supabase records.
- Confirmed database insert after upload initiation.

Why this was implemented:

- The previous stage returned a document ID but did not persist lifecycle metadata.
- Supabase now stores document status, S3 object location, trace ID, user ID, and company ID.
- Audit logs provide compliance and investigation evidence.

Security value:

- Adds persistent document lifecycle tracking.
- Adds business-level audit logging separate from CloudWatch technical logs.
- Prepares the system for deletion, status retrieval, HITL routing, and processing history.

---

## Stage 3: Event-Driven Pre-processing

Completed:

- Created SQS dead-letter queue `capisso-preprocess-dlq`.
- Created SQS main queue `capisso-preprocess-queue`.
- Configured the main queue to use the DLQ with maximum receives set to 3.
- Added SQS access policy so the S3 document bucket can send ObjectCreated events to the queue.
- Configured S3 event notification for the `raw/` prefix.
- Created pre-processing Lambda function.
- Added least-privilege IAM permissions for S3 raw object read, SQS message processing, and CloudWatch logging.
- Attached SQS trigger to the pre-processing Lambda.
- Deployed pre-processing Lambda code.
- Tested end-to-end upload event flow from S3 to SQS to Lambda.
- Confirmed CloudWatch logging for the pre-processing stage.
- Confirmed Supabase status/audit updates where applicable.

Why this was implemented:

- The previous stage created secure upload URLs but did not automatically start processing after upload.
- This stage introduces an event-driven processing skeleton.
- SQS provides buffering, retries, and dead-letter handling.
- The pre-processing Lambda validates uploaded objects before they move to OCR/model extraction.
- Supabase status and audit records improve traceability and compliance evidence.

Security value:

- Improves lifecycle tracking.
- Supports failure handling through DLQ.
- Keeps Lambda permissions scoped to required resources.
- Avoids logging document content or PII.
- Provides traceable status changes for uploaded documents.


## Stage 4 Progress — Mock Extraction Processing

Completed:
- Created extraction SQS dead-letter queue `capisso-extraction-dlq`.
- Created extraction SQS main queue `capisso-extraction-queue`.
- Configured extraction queue with DLQ and maximum receives set to 3.
- Added Supabase tables `processing_runs` and `extraction_results`.
- Updated pre-processing Lambda to send validated documents to the extraction queue.
- Created extraction Lambda function.
- Added least-privilege IAM permissions for extraction queue processing and CloudWatch logging.
- Attached SQS trigger to extraction Lambda.
- Implemented mock structured extraction output.
- Stored processing metadata in `processing_runs`.
- Stored structured extracted data and confidence values in `extraction_results`.
- Updated document lifecycle status after extraction.
- Added extraction audit events.
- Confirmed expected results in Supabase.

Why this was implemented:
- The previous pipeline could upload and pre-process documents but did not create extraction output.
- This stage proves the extraction pipeline mechanics before introducing Bedrock or SageMaker.
- Mock extraction allows controlled testing of status tracking, audit logging, confidence scoring, and HITL readiness.

Security value:
- Keeps extraction as a separate Lambda with separate IAM scope.
- Uses SQS and DLQ for retry and failure isolation.
- Stores structured results in Supabase instead of logs.
- Logs only metadata and trace information in CloudWatch.
- Adds processing traceability through `processing_runs`, `extraction_results`, and `audit_logs`.

Next steps:
- Add post-processing validation rules.
- Add HITL routing evidence for low-confidence results.
- Add CloudWatch alarms for failed Lambda executions and DLQ messages.
- Replace mock extraction with Bedrock/SageMaker or model adapter.

---

## Stage 4: Mock Extraction Pipeline

### Work completed

- Created the extraction SQS queue and extraction dead-letter queue.
- Connected the extraction queue to the extraction Lambda.
- Added the extraction Lambda execution-role permissions.
- Created the `processing_runs` and `extraction_results` Supabase tables.
- Implemented deterministic mock extraction output.
- Added field-level and overall confidence values.
- Added the `needs_human_review` decision field.
- Added document lifecycle status updates.
- Added extraction-stage audit events.
- Added structured CloudWatch logs with trace IDs.
- Tested the full asynchronous workflow from document upload through extraction-result storage.

### Result

The complete event-driven workflow was successfully validated:

```text
API Gateway
→ Upload Lambda
→ S3
→ Pre-processing SQS
→ Pre-processing Lambda
→ Extraction SQS
→ Extraction Lambda
→ Supabase
→ CloudWatch
```
The mock adapter was used to test the architecture independently of model billing, availability, latency and provider-specific behaviour.

### Limitation
This stage did not demonstrate real AI document extraction. The mock output was used only to validate orchestration, status handling, audit logging, confidence routing and result persistence.

## 26 July 2026 — Real Model Execution Decision
Project-lead guidance

The project lead confirmed that real paid-model execution can be deferred until billing-enabled credentials are available.
The project should instead identify a suitable model from Amazon Bedrock or SageMaker so that it can be tested once project credentials are provided.

## Decision

The following implementation strategy was adopted:

- Retain the working mock adapter for deterministic pipeline testing.
- Do not redesign or migrate the existing AWS workflow.
- Select and justify the proposed Bedrock model.
- Identify a SageMaker alternative.
- Prepare the secure model-invocation design.
- Prepare the IAM policy, extraction prompt and JSON output schema.
- Continue with framework, threat, post-processing and evaluation work.

## Reasoning

This decision avoids spending additional time on account-restricted services while preserving the existing AWS architecture.
The extraction stage was deliberately designed as a replaceable provider adapter. A Bedrock or SageMaker implementation can therefore replace the mock adapter later without changing the upload, storage, queue, audit or database components.

## Current project status
| Area                                  | Status                                                    |
| ------------------------------------- | --------------------------------------------------------- |
| Secure upload pipeline                | Implemented                                               |
| S3 storage and event trigger          | Implemented                                               |
| Pre-processing queue and Lambda       | Implemented                                               |
| Extraction queue and Lambda           | Implemented                                               |
| Supabase processing and audit records | Implemented                                               |
| Mock extraction orchestration         | Implemented                                               |
| Real Textract adapter                 | Implemented but execution blocked by account restrictions |
| Bedrock model selection               | Next task                                                 |
| Threat modelling and risk register    | Pending                                                   |
| NIST Current and Target Profiles      | Pending                                                   |
| Post-processing validation            | Pending                                                   |
| Low-confidence HITL testing           | Pending                                                   |
| Monitoring alarms and evaluation      | Pending                                                   |

# Immediate next steps
- Document the selected Bedrock and SageMaker models.
- Add the proposed Bedrock IAM policy template.
- Add the secure extraction prompt and JSON schema.
- Complete the threat model and risk register.
- Extend the NIST CSF 2.0 mapping into Current and Target Profiles.
- Implement post-processing and low-confidence routing tests.
- Complete the security evaluation by 30 July 2026.

## Stage 5A: Real Model Service Attempt and Constraint Analysis

### Work completed

- Investigated Amazon Textract `AnalyzeExpense` for real receipt and invoice extraction.
- Prepared the extraction Lambda to reach the managed-service invocation point.
- Preserved the existing S3, SQS, Supabase, audit and CloudWatch workflow.
- Executed the service attempt.
- Recorded the resulting `SubscriptionRequiredException`.
- Confirmed that the AWS account plan restricted the required paid-service access.
- Obtained project-lead approval to defer paid-model execution.

### Result

The extraction pipeline reached the real AWS service boundary, but no real extraction result was produced because service access was blocked by the account plan.

### Security and architectural value

- Confirmed that the provider can remain isolated behind the extraction Lambda.
- Preserved the existing event-driven pipeline.
- Identified service availability and billing as operational dependencies.
- Established that real model output must still pass independent validation.

### Limitation

This stage does not demonstrate Textract accuracy or successful real-model execution.

---

## Stage 5B: Secure AI Model Adapter Design

### Work completed

- Selected Amazon Nova Lite as the proposed Bedrock model for later credential-based testing.
- Identified a SageMaker-hosted document model as an alternative.
- Prepared a least-privilege Bedrock IAM policy template.
- Prepared a secure receipt and invoice extraction prompt.
- Prepared a strict JSON extraction schema.
- Defined the extraction Lambda as the replaceable provider-adapter boundary.
- Defined the Bedrock invocation and Stage 5C validation flow.
- Defined a bounded real-model test and evaluation plan.

### Result

The secure model-integration design is complete and can be tested when suitable AWS credentials are available.

### Limitation

The design artefacts have not been deployed against a real Bedrock or SageMaker model, and model accuracy has not been evaluated.

---

## Stage 5C: Post-processing Validation and HITL Routing

### Work completed

- Extended `extraction_results` with validation status, validation errors, review reasons, schema version and validation timestamp.
- Created the `review_tasks` table for Human-in-the-Loop workflow tracking.
- Enabled Row Level Security on the review-task table.
- Updated the extraction Lambda with deterministic schema, date, currency, monetary and line-item validation.
- Added financial consistency checks for subtotal, tax, total and line-item sums.
- Added overall and field-level confidence routing.
- Added prompt-injection indicator detection.
- Added malformed-output handling.
- Added medium- and high-priority review-task creation.
- Added post-processing and HITL audit events.
- Added safe structured CloudWatch validation logs.
- Tested valid, low-confidence, missing-field, financial-mismatch, prompt-injection and malformed-output scenarios.

### Result

Valid output completed automatically. Every risky scenario was prevented from automatic completion and routed to Human-in-the-Loop review with validation evidence, priority and audit traceability.

### Limitation

The tests use a deterministic mock extraction adapter. They validate security-control behaviour and orchestration, not real-model extraction accuracy.
