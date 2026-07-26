# Evidence Folder

This folder tracks implementation evidence for the cloud security prototype.

Screenshots are stored locally unless they are cropped and sanitized. The public GitHub repository should contain an evidence index, not a dump of sensitive screenshots.

---

## Stage 1 — Secure Upload Evidence

| Evidence Item | Status | Storage |
|---|---|---|
| S3 bucket created | Completed | Local screenshot |
| S3 Block Public Access enabled | Completed | Local screenshot |
| S3 default encryption enabled | Completed | Local screenshot |
| S3 prefixes created: `raw`, `processed`, `rejected`, `audit-artifacts` | Completed | Local screenshot |
| Upload Lambda environment variables configured | Completed | Local screenshot |
| Upload Lambda IAM inline policy attached | Completed | Local screenshot |
| Valid upload initiation test passed | Completed | Local screenshot |
| Invalid file type rejected | Completed | Local screenshot |
| Oversized file rejected | Completed | Local screenshot |
| Extension/content-type mismatch rejected | Completed | Local screenshot |
| S3 object uploaded through pre-signed URL | Completed | Local screenshot |
| CloudWatch safe log generated with trace ID | Completed | Local screenshot |

---

## Stage 2 — Supabase Metadata and Audit Evidence

| Evidence Item | Status | Storage |
|---|---|---|
| Supabase `documents` table created | Completed | Local screenshot |
| Supabase `audit_logs` table created | Completed | Local screenshot |
| Upload initiation created document record | Completed | Local screenshot |
| Upload initiation created audit record | Completed | Local screenshot |
| CloudWatch log confirms database write | Completed | Local screenshot |

---

## Stage 3 — Event-Driven Pre-processing Evidence

| Evidence Item | Status | Storage |
|---|---|---|
| SQS dead-letter queue `capisso-preprocess-dlq` created | Completed | Local screenshot |
| SQS main queue `capisso-preprocess-queue` created | Completed | Local screenshot |
| Dead-letter queue configured with maximum receives set to 3 | Completed | Local screenshot |
| SQS access policy allows S3 bucket to send messages | Completed | Local screenshot |
| S3 event notification created for `raw/` prefix | Completed | Local screenshot |
| Pre-processing Lambda created | Completed | Local screenshot |
| Pre-processing Lambda IAM policy attached | Completed | Local screenshot |
| SQS trigger attached to pre-processing Lambda | Completed | Local screenshot |
| File uploaded to S3 through pre-signed URL | Completed | Local screenshot |
| Pre-processing Lambda CloudWatch log generated | Completed | Local screenshot |
| Supabase document status updated by pre-processing Lambda | Completed | Local screenshot |
| Supabase audit log records generated | Completed | Local screenshot |

---

## Evidence Handling Rule

Do not commit:

- AWS access keys
- Supabase service-role keys
- `.env` files
- Full pre-signed URLs
- Real receipt or invoice files containing PII
- Full screenshots exposing account details, tokens, or sensitive configuration
- Raw CloudWatch logs containing sensitive values

Screenshots should be kept in a private local folder unless they are cropped and sanitized.

Recommended private local structure:

```text
capstone-evidence-private/
  stage-1-secure-upload/
  stage-2-supabase-audit/
  stage-3-event-driven-preprocessing/
```
## Stage 4 — Mock Extraction Pipeline

### Objective

Validate the extraction-stage orchestration independently of paid model access. This stage tested the extraction queue, Lambda processing, result persistence, confidence handling, document-status updates, audit logging and CloudWatch traceability.

### Evidence

| Evidence file | Description |
|---|---|
| `stage-4/01-extraction-queue-and-dlq.png` | Extraction SQS queue and associated dead-letter queue |
| `stage-4/02-extraction-lambda-sqs-trigger.png` | Extraction queue configured as the Lambda trigger |
| `stage-4/03-extraction-lambda-code-deployed.png` | Mock extraction Lambda implementation deployed |
| `stage-4/04-extraction-lambda-iam-policy.png` | Least-privilege extraction Lambda permissions |
| `stage-4/05-supabase-processing-run.png` | Processing-run record created for the extraction operation |
| `stage-4/06-supabase-extraction-result.png` | Structured mock extraction result stored in Supabase |
| `stage-4/07-supabase-document-status.png` | Document lifecycle status updated after extraction |
| `stage-4/08-supabase-audit-events.png` | Extraction lifecycle events recorded in the audit table |
| `stage-4/09-cloudwatch-extraction-trace.png` | Structured CloudWatch log containing the trace ID and extraction result |

### Outcome

The extraction queue and Lambda were successfully integrated with the existing preprocessing workflow.

The stage demonstrated:

- Extraction-message consumption from SQS
- Processing-run creation
- Structured-result persistence
- Field and overall confidence storage
- `needs_human_review` readiness
- Document-status transitions
- Audit-event creation
- Trace-ID continuity

The mock output was used only for deterministic pipeline and security-control testing. It is not presented as evidence of real AI extraction accuracy.

---

## Stage 5A — Real AWS Extraction Integration Attempt

### Objective

Replace the mock extraction adapter with an AWS-native receipt and invoice extraction service.

Amazon Textract `AnalyzeExpense` was selected for the initial integration attempt because it supports structured extraction of receipt and invoice fields.

### Evidence

| Evidence file | Description |
|---|---|
| `stage-5a/01-textract-iam-permission.png` | Extraction Lambda permission for `textract:AnalyzeExpense` |
| `stage-5a/02-textract-extraction-code-deployed.png` | Textract adapter deployed in the extraction Lambda |
| `stage-5a/03-cloudwatch-subscription-required-error.png` | CloudWatch error showing `SubscriptionRequiredException` |
| `stage-5a/04-aws-free-plan-access-limitation.png` | AWS console page showing free-account service limitations |
| `stage-5a/05-project-lead-model-guidance.txt` | Sanitised record of the decision to defer paid model execution |

### Outcome

The AWS event-driven pipeline successfully reached the Amazon Textract API call. The request was rejected with:

```text
SubscriptionRequiredException
```
The AWS console confirmed that the current free account plan restricts access to the required service. Therefore, the failure was caused by an account-level service limitation rather than the SQS trigger, Lambda invocation flow or extraction-adapter control path.

Following project-lead guidance, paid model execution has been deferred until billing-enabled project credentials are available.

The next model-related tasks are:

- Select a suitable Amazon Bedrock model
- Identify a SageMaker alternative
- Define the secure model-invocation workflow
- Prepare the IAM policy template
- Prepare the extraction prompt and JSON schema
- Define the real-model evaluation plan

