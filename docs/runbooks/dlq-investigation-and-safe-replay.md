# Runbook — DLQ Investigation and Safe Replay

## Purpose

Use this runbook when either of these alarms enters `ALARM`:

```text
capisso-preprocessing-dlq-messages
capisso-extraction-dlq-messages
```

The objective is to investigate the failed message, preserve evidence, correct the underlying issue and recover the workflow without causing duplicate processing or repeated failures.

## Safety Rules

1. Do not purge a DLQ.
2. Do not redrive an invalid message without correcting the cause.
3. Do not paste complete message bodies into tickets, email or GitHub.
4. Do not expose document contents, pre-signed URLs, credentials, PII or financial values.
5. Do not replay a message until duplicate-processing risk has been checked.
6. Do not disable alarms to hide a known failure.
7. Preserve trace IDs, timestamps and error types.
8. Escalate suspicious or malicious content instead of replaying it.

## Step 1 — Record the Incident

Record:

```text
Incident ID:
Detected at:
Alarm name:
AWS region:
Source queue:
Dead-letter queue:
Alarm state:
Approximate visible messages:
Investigator:
```

Use operational metadata only.

## Step 2 — Validate the Alert

Open:

```text
CloudWatch
→ Alarms
→ affected alarm
→ History
```

Confirm:

- The state changed to `ALARM`.
- The monitored metric is correct.
- The SNS action succeeded.
- The alarm refers to the expected queue.
- The alarm is not an old or duplicate notification.

For a DLQ incident, verify:

```text
Metric = ApproximateNumberOfMessagesVisible
Value >= 1
```

## Step 3 — Check Related Lambda Errors

Open the corresponding Lambda error alarm:

```text
Preprocessing DLQ → capisso-preprocessing-lambda-errors
Extraction DLQ → capisso-extraction-lambda-errors
```

Record the first failure time, repeated error datapoints and recovery state.

## Step 4 — Inspect CloudWatch Logs

Open the affected Lambda log group and search near the incident time for:

- `traceId`
- `documentId`
- `errorType`
- `errorMessage`
- `status = failed`
- Lambda request ID

Classify the error:

| Category | Examples |
|---|---|
| Invalid message | Malformed JSON or missing required fields |
| Code defect | Unhandled exception or parsing bug |
| Permission failure | Access denied to S3, SQS, model or database |
| Downstream outage | Supabase, model service or network failure |
| Configuration failure | Missing or invalid environment variable |
| Transient service error | Timeout or temporary service failure |
| Suspicious input | Prompt injection, malformed document or unexpected payload |

## Step 5 — Inspect the DLQ Message

Open:

```text
SQS
→ affected DLQ
→ Send and receive messages
→ Poll for messages
```

Inspect one message at a time.

Record:

- Message ID.
- Approximate receive count.
- Sent timestamp.
- First receive timestamp.
- Trace ID.
- Document ID, when present.
- Source queue.
- Error classification.

Do not delete the message yet.

## Step 6 — Check Duplicate-Processing Risk

Before replay, check Supabase using the document ID and trace ID.

Review:

```text
documents
processing_runs
extraction_results
review_tasks
audit_logs
```

Determine whether processing never started, started but did not complete, already produced a result, already produced a review task or later completed successfully.

If a valid result already exists, do not replay automatically.

## Step 7 — Choose the Response

### A. Invalid or poison message

Examples: non-JSON message, missing identifiers or unsupported schema.

```text
Preserve evidence
→ document the reason
→ do not replay
→ delete only after approval
```

### B. Transient downstream failure

```text
Confirm service recovery
→ verify no completed duplicate
→ replay one controlled message
→ monitor result
```

### C. Permission or configuration failure

```text
Correct configuration
→ verify permissions
→ replay one controlled message
```

### D. Code defect

```text
Reproduce safely
→ correct and deploy code
→ test outside production
→ replay one controlled message
```

### E. Suspicious or malicious input

```text
Do not replay
→ preserve evidence
→ restrict access
→ escalate for security review
```

## Step 8 — Safe Replay Method

For this low-volume prototype, prefer one-message manual replay when the DLQ contains mixed or unreviewed messages.

### Manual controlled replay

1. Copy only the reviewed message body and required message attributes.
2. Open the original source queue.
3. Send the reviewed message to the source queue.
4. Record a recovery trace or incident reference where supported.
5. Do not delete the DLQ copy yet.
6. Monitor the corresponding Lambda logs.
7. Confirm successful Supabase lifecycle updates.
8. Confirm no duplicate extraction result or review task was created.
9. Delete the original DLQ message only after success.

### Bulk DLQ redrive

Use bulk redrive only when:

- The root cause is fixed.
- Every message in the redrive set has been reviewed.
- Bulk replay will not create duplicates.
- The source queue and destination are confirmed.
- Alarm and log monitoring are active.

Do not use bulk redrive for mixed, unknown or malicious messages.

## Step 9 — Verify Recovery

Confirm:

```text
Source message processed successfully
DLQ visible messages reduced
DLQ alarm returned to OK
Lambda error alarm returned to OK
CloudWatch logs show success
Supabase status is correct
Audit records are present
No duplicate result was created
```

If any check fails, stop replay and return to investigation.

## Step 10 — Close the Incident

Record:

```text
Root cause:
Containment action:
Correction:
Replay method:
Replay result:
Data affected:
Duplicate check:
Alarm recovery time:
Residual risk:
Follow-up action:
Closed by:
Closed at:
```

## Escalation Criteria

Escalate when:

- Multiple documents are affected.
- The same error repeats after correction.
- A message contains suspicious instructions or content.
- Credentials or secrets may have been exposed.
- Tenant isolation may have failed.
- Financial values may have been corrupted.
- A real document cannot be safely replayed.
- The DLQ continues to grow.
