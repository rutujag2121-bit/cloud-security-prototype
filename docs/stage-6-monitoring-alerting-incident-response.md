# Stage 6 — Monitoring, Alerting and Incident Response

## Status

**Implemented and tested**

## 1. Objective

Stage 6 adds active operational monitoring and a documented incident-response process to the Capisso DEW pipeline.

Before this stage, failures were visible only through manual inspection of CloudWatch logs, Lambda metrics and SQS queues.

The implemented flow is:

```text
Failure or exhausted retry
→ CloudWatch metric
→ CloudWatch alarm
→ SNS notification
→ Email alert
→ Investigation
→ Containment
→ Safe replay or controlled removal
→ Recovery verification
```

## 2. Why This Stage Was Required

Logging alone does not provide timely detection. A document-processing failure may leave a receipt or invoice unprocessed, prevent extraction results from being stored or cause a message to remain outside the normal workflow.

Stage 6 therefore adds controls for failure detection, automated notification, retry-exhaustion detection, dead-letter queue investigation, safe replay decisions, recovery verification and evidence preservation.

## 3. Notification Channel

An Amazon SNS topic was created:

```text
capisso-security-alerts
```

A confirmed email subscription receives CloudWatch alarm state notifications. A manual SNS message test confirmed delivery.

### SNS Encryption Issue and Resolution

The first CloudWatch alarm notification failed because the SNS topic encryption key did not permit the CloudWatch Alarms service to use the key.

CloudWatch correctly entered the alarm state, but its notification action failed.

For this prototype, SNS server-side encryption was disabled because alarm notifications contain operational metadata only and must not contain document contents, credentials, pre-signed URLs, PII or extracted financial values.

The controlled Lambda failure was repeated and the email notification was then delivered successfully.

## 4. Lambda Error Alarms

| Alarm | Metric | Condition |
|---|---|---|
| `capisso-upload-lambda-errors` | `AWS/Lambda Errors` | Sum greater than or equal to 1 in 1 minute |
| `capisso-preprocessing-lambda-errors` | `AWS/Lambda Errors` | Sum greater than or equal to 1 in 1 minute |
| `capisso-extraction-lambda-errors` | `AWS/Lambda Errors` | Sum greater than or equal to 1 in 1 minute |

Common configuration:

```text
Statistic: Sum
Period: 1 minute
Datapoints to alarm: 1 out of 1
Missing data: not breaching
Notification: capisso-security-alerts
```

## 5. Dead-Letter Queue Alarms

| Alarm | Metric | Condition |
|---|---|---|
| `capisso-preprocessing-dlq-messages` | `AWS/SQS ApproximateNumberOfMessagesVisible` | Maximum greater than or equal to 1 in 1 minute |
| `capisso-extraction-dlq-messages` | `AWS/SQS ApproximateNumberOfMessagesVisible` | Maximum greater than or equal to 1 in 1 minute |

Common configuration:

```text
Statistic: Maximum
Period: 1 minute
Datapoints to alarm: 1 out of 1
Missing data: not breaching
Notification: capisso-security-alerts
```

## 6. Controlled Tests

### Test 1 — Extraction Lambda failure

A direct Lambda test used an invalid SQS message body:

```text
this-is-not-valid-json
```

Observed result:

```text
JSONDecodeError
→ Lambda Errors metric increased
→ extraction Lambda alarm entered ALARM
→ SNS email notification received
→ CloudWatch log recorded the failure
→ alarm later returned to OK
```

### Test 2 — Direct extraction DLQ alarm

A harmless test message was placed directly into the extraction DLQ.

Observed result:

```text
Visible DLQ message
→ extraction DLQ alarm entered ALARM
→ email notification received
→ controlled message deleted
→ alarm returned to OK
```

### Test 3 — Automatic retry exhaustion and redrive

An invalid message was sent to the extraction main queue.

Observed result:

```text
Extraction Lambda failed
→ SQS retried the message
→ maximum receive count was exceeded
→ message moved automatically to extraction DLQ
→ Lambda error alarm activated
→ DLQ message alarm activated
→ email notifications received
→ message inspected and deleted
→ alarms recovered
```

## 7. Security Value

Stage 6 demonstrates:

- Automated detection of Lambda failures.
- Detection of exhausted queue retries.
- Centralised email notification.
- Separation between transient invocation errors and DLQ incidents.
- Evidence-based investigation.
- Controlled handling of poison messages.
- Recovery-state verification.
- Documented response and replay decisions.

## 8. Operational Distinction

| Alarm type | Interpretation |
|---|---|
| Lambda error alarm | At least one invocation failed; automatic retry may still recover |
| DLQ message alarm | Retry handling was exhausted; manual intervention is required |

## 9. Known Limitations

- Email is the only notification endpoint.
- There is no on-call rota or escalation platform.
- SNS encryption is disabled in the prototype.
- Alarm thresholds are tuned for a low-volume prototype.
- Upload and preprocessing Lambda alarms were configured but not deliberately failed.
- The Lambda/SQS integration does not yet use partial batch failure reporting.
- Full idempotency and replay protection are not implemented.
- Incident records are manual.
- CloudWatch alarm configuration is not managed through infrastructure as code.

## 10. Future Hardening

- Enable a customer-managed SNS KMS key with required service permissions.
- Add SNS delivery-failure monitoring.
- Use partial batch responses for SQS-triggered Lambdas.
- Add idempotency checks before replay.
- Tune alarm thresholds using production traffic.
- Add a second notification channel.
- Manage alarms, topics and queues through infrastructure as code.
- Ensure DLQ retention exceeds source-queue retention.
