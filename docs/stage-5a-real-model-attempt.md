# Stage 5A — Real Model Service Attempt and Constraint Analysis

## Status

**Attempted — execution blocked by AWS account restrictions**

## 1. Objective

Stage 5A investigated whether the working extraction stage could be connected to a real AWS-managed document extraction service without redesigning the existing event-driven pipeline.

The intended flow was:

```text
Extraction SQS queue
→ Extraction Lambda
→ Amazon Textract AnalyzeExpense
→ Structured extraction result
→ Supabase processing and audit records
→ Post-processing and Human-in-the-Loop routing
```

The purpose was to replace the deterministic mock output with real document extraction while preserving the upload, storage, queue, audit and database components already implemented.

## 2. Service Investigated

Amazon Textract `AnalyzeExpense` was selected for the first real-service attempt because it is designed to extract structured fields from receipts and invoices.

The attempted integration used the existing extraction Lambda as the provider-adapter point. This meant that the surrounding architecture did not need to change.

## 3. Implementation Work Performed

- Added a Textract client to the extraction Lambda.
- Prepared the Lambda to call `AnalyzeExpense`.
- Used the existing S3 object reference as the document source.
- Retained the existing `processing_runs`, `extraction_results`, `documents` and `audit_logs` lifecycle.
- Preserved trace-ID propagation and CloudWatch logging.
- Tested whether the Lambda could reach the AWS managed-service invocation point.

## 4. Test Result

The extraction Lambda reached the Textract service call, but AWS returned:

```text
SubscriptionRequiredException
```

The AWS account interface also indicated that the current account plan did not provide the billing-enabled access required for the service.

Therefore, the test established that:

```text
Pipeline and adapter path reached the managed-service boundary
→ AWS account restriction prevented model execution
→ no real extraction result was produced
```

## 5. Project-Lead Decision

The project lead confirmed that paid-model execution could be deferred until suitable credentials were available.

The agreed direction was to:

- Retain the working mock adapter for deterministic pipeline and security testing.
- Avoid redesigning the existing AWS workflow.
- Select a suitable Bedrock or SageMaker model.
- Prepare the secure invocation design, IAM policy, extraction prompt and JSON schema.
- Continue with post-processing, HITL, threat modelling and framework evaluation.

## 6. Security Significance

Although real extraction was not completed, the attempt provided useful security and architectural evidence.

It confirmed that:

- The model provider can be isolated behind the extraction Lambda.
- The upload, S3, SQS, Supabase and audit layers do not depend on a specific model.
- Provider failure can be separated from the rest of the workflow.
- Real-model permissions should be scoped independently through least-privilege IAM.
- Model output must still pass deterministic post-processing controls before acceptance.
- Account and service dependencies are external operational risks that must be recorded honestly.

## 7. Evidence

Relevant evidence includes:

- CloudWatch error showing `SubscriptionRequiredException`.
- AWS account-plan restriction screen.
- Extraction Lambda attempt.
- Project-lead email approving deferral.
- Progress-log entry recording the decision.

Sensitive screenshots, complete AWS identifiers and credentials are retained outside the public repository.

## 8. Outcome

Stage 5A did not demonstrate successful real-model extraction.

Its accurate outcome is:

```text
Real AWS service integration attempted
→ service invocation blocked by account restrictions
→ architectural adapter approach validated
→ real execution deferred
```

This stage must not be cited as evidence of Textract accuracy, AI-model accuracy or successful production integration.

## 9. Next Stage

Stage 5B formalises the secure AI model adapter design so that the real provider can be tested later without changing the wider pipeline.
