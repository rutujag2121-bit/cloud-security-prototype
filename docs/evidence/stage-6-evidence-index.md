# Stage 6 Evidence Index

Store original screenshots privately. Public versions must be cropped or masked.

| Evidence file | Description |
|---|---|
| `01-sns-security-alert-topic-created.png` | Central SNS alert topic |
| `02-sns-email-subscription-confirmed.png` | Confirmed email subscription |
| `03-sns-test-message-published.png` | Manual SNS test |
| `04-sns-test-email-received.png` | Notification-channel test |
| `05-controlled-extraction-lambda-error.png` | Controlled JSON parsing failure |
| `06-extraction-error-alarm-in-alarm.png` | Extraction error alarm activated |
| `07-extraction-error-alarm-action-failed-kms.png` | Initial KMS authorization failure |
| `08-sns-topic-encryption-disabled.png` | Prototype remediation |
| `09-extraction-alarm-action-successful.png` | Alarm action succeeded after remediation |
| `10-extraction-error-alert-email-received.png` | Extraction error email |
| `11-three-lambda-error-alarms-created.png` | Upload, preprocessing and extraction alarms |
| `12-preprocessing-lambda-error-alarm-configuration.png` | Example Lambda alarm configuration |
| `13-two-dlq-message-alarms-created.png` | Preprocessing and extraction DLQ alarms |
| `14-preprocessing-dlq-alarm-configuration.png` | Preprocessing DLQ configuration |
| `15-extraction-dlq-alarm-configuration.png` | Extraction DLQ configuration |
| `16-controlled-message-sent-to-extraction-dlq.png` | Direct DLQ alarm test |
| `17-extraction-dlq-one-visible-message.png` | Visible controlled message |
| `18-extraction-dlq-alarm-in-alarm.png` | DLQ alarm activated |
| `19-extraction-dlq-alarm-history.png` | DLQ state transition |
| `20-extraction-dlq-alert-email-received.png` | DLQ email notification |
| `21-controlled-extraction-dlq-message-deleted.png` | Controlled message removal |
| `22-extraction-dlq-alarm-returned-to-ok.png` | Alarm recovery |
| `23-extraction-main-queue-redrive-policy.png` | Source queue redrive configuration |
| `24-controlled-invalid-message-sent-to-main-queue.png` | Poison-message test |
| `25-extraction-lambda-repeated-message-failures.png` | Retry evidence |
| `26-message-automatically-moved-to-extraction-dlq.png` | Automatic DLQ routing |
| `27-automatic-redrive-dlq-alarm-in-alarm.png` | Alarm after retry exhaustion |
| `28-automatic-redrive-dlq-alarm-history.png` | Automatic routing alarm history |
| `29-automatic-redrive-dlq-email-received.png` | DLQ notification |
| `30-dlq-message-receive-count-evidence.png` | Multiple receive attempts |
| `31-controlled-dlq-message-deleted.png` | Poison-message removal |
| `32-extraction-dlq-alarm-recovered-to-ok.png` | Final recovery |

Never publish unmasked AWS account IDs, personal email addresses, complete ARNs, queue URLs, credentials, pre-signed URLs or document contents.
