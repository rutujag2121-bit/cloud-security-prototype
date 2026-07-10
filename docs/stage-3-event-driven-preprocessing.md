# Stage 3: Event-Driven Pre-processing

## Objective

Implement an event-driven pre-processing stage that automatically starts after a document is uploaded to the S3 `raw/` prefix.

## Previous State

Before this stage, the system could validate upload metadata, generate a document ID, create a structured S3 object key, generate a pre-signed S3 upload URL, and store initial metadata/audit records in Supabase.

However, after the file was uploaded to S3, no automated processing stage was triggered.

## New Implementation

The system now uses an event-driven pipeline:

```text
S3 raw upload
→ S3 ObjectCreated event
→ SQS preprocessing queue
→ Pre-processing Lambda
→ Supabase document status update
→ Supabase audit log update
→ CloudWatch structured log
```
AWS Resources Added
| Resource              | Name                                    | Purpose                                                  |
| --------------------- | --------------------------------------- | -------------------------------------------------------- |
| SQS dead-letter queue | `capisso-preprocess-dlq`                | Stores messages that fail repeatedly                     |
| SQS main queue        | `capisso-preprocess-queue`              | Receives S3 ObjectCreated events                         |
| S3 event notification | `raw-upload-created`                    | Sends events for new objects under `raw/`                |
| Pre-processing Lambda | `document-processing-preprocess-lambda` | Validates uploaded objects and updates status/audit logs |
| Lambda SQS trigger    | SQS event source mapping                | Invokes pre-processing Lambda from queue messages        |

SQS was added between S3 and Lambda to avoid tightly coupling storage events directly to processing.
| Benefit           | Explanation                                                |
| ----------------- | ---------------------------------------------------------- |
| Buffering         | Upload events can wait in the queue if Lambda is busy      |
| Retry handling    | Failed events can be retried automatically                 |
| Failure isolation | Failed messages can move to the DLQ                        |
| Better evidence   | Queue and DLQ provide visible proof of event-driven design |
| Scalability       | Multiple uploaded documents can be handled asynchronously  |

The dead-letter queue stores events that fail processing multiple times. This prevents repeated failures from being hidden or retried indefinitely.
For this prototype, the maximum receive count is set to 3. If the same message fails three times, it is moved to the DLQ for investigation.

Document Status Transitions
| Stage                                | Status                    |
| ------------------------------------ | ------------------------- |
| Upload Lambda creates pre-signed URL | `upload_url_created`      |
| S3 upload event received             | `uploaded`                |
| Pre-processing starts                | `preprocessing_started`   |
| Object passes validation             | `preprocessing_completed` |
| Object fails validation              | `preprocessing_failed`    |

Audit Events Added
| Audit Event               | Meaning                                      |
| ------------------------- | -------------------------------------------- |
| `FILE_UPLOADED`           | S3 upload event was received                 |
| `PREPROCESSING_COMPLETED` | Uploaded object exists and passed validation |
| `PREPROCESSING_FAILED`    | Uploaded object failed validation            |

Validation Performed
The pre-processing Lambda checks:
| Check                                 | Reason                                                   |
| ------------------------------------- | -------------------------------------------------------- |
| Bucket name matches expected bucket   | Prevents processing events from unexpected buckets       |
| Object key starts with `raw/`         | Ensures only raw uploaded documents are processed        |
| Object key follows expected structure | Extracts company ID, user ID, document ID, and file name |
| Object exists in S3                   | Confirms upload actually completed                       |
| Content type is allowed               | Prevents unsupported files from moving forward           |

Security Controls Implemented
| Security Control        | Implementation                                                                       |
| ----------------------- | ------------------------------------------------------------------------------------ |
| Least privilege         | Pre-processing Lambda can only read from S3 `raw/`, consume from SQS, and write logs |
| Queue-based resilience  | SQS and DLQ reduce risk of lost processing events                                    |
| Safe logging            | CloudWatch logs metadata only, not document contents                                 |
| Traceability            | `traceId` and `documentId` are used in logs and Supabase                             |
| Auditability            | Supabase audit logs record file upload and pre-processing completion                 |
| Data lifecycle tracking | Supabase document status changes as the file moves through the pipeline              |

This stage improves the system because document processing no longer depends on manual checking after upload. The system automatically detects newly uploaded files, places the event into a queue, and processes it through a dedicated Lambda function.
This supports a stronger security posture because the document lifecycle is traceable, failed processing events are recoverable, and the pre-processing function has a restricted role with only the permissions needed for this stage.
