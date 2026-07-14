# Stage 4: Mock Extraction Processing

## Objective

Implement a mock extraction stage that consumes validated document messages from the extraction SQS queue and stores structured extraction output in Supabase.

## Previous State

Before this stage, the pipeline could securely upload a document, store it in S3, trigger pre-processing, validate the uploaded object, and queue the document for extraction.

However, no extraction result was generated or stored.

## New Implementation

The system now performs a mock extraction workflow:

```text
Extraction SQS queue
→ Extraction Lambda
→ processing_runs table
→ extraction_results table
→ documents status update
→ audit_logs entries
→ CloudWatch structured logs
```
##  AWS Resources Added
| Resource          | Name                                    | Purpose                                                 |
| ----------------- | --------------------------------------- | ------------------------------------------------------- |
| Extraction queue  | `capisso-extraction-queue`              | Receives extraction messages from pre-processing Lambda |
| Extraction DLQ    | `capisso-extraction-dlq`                | Stores failed extraction messages                       |
| Extraction Lambda | `document-processing-extraction-lambda` | Performs mock extraction and writes results to Supabase |
| SQS trigger       | Extraction queue trigger                | Invokes extraction Lambda when messages arrive          |

##  Supabase Tables Used
| Table                | Purpose                                                                                  |
| -------------------- | ---------------------------------------------------------------------------------------- |
| `processing_runs`    | Tracks extraction attempts, provider, model name, method, status, duration, and trace ID |
| `extraction_results` | Stores structured extracted JSON, field confidence, overall confidence, and HITL flag    |
| `documents`          | Stores lifecycle status such as `ocr_started`, `ocr_completed`, or `needs_human_review`  |
| `audit_logs`         | Stores extraction-related audit events                                                   |

##  Mock Extraction Output
| Field              | Example                                  |
| ------------------ | ---------------------------------------- |
| Supplier name      | `Mock Supplier Ltd`                      |
| Document date      | `2026-07-13`                             |
| Currency           | `EUR`                                    |
| Total amount       | `42.50`                                  |
| Line items         | One mock line item                       |
| Overall confidence | Average of field confidence values       |
| HITL flag          | Based on configured confidence threshold |

##  Status Transitions
| Step                                     | Document Status      |
| ---------------------------------------- | -------------------- |
| Extraction Lambda starts                 | `ocr_started`        |
| Extraction confidence is acceptable      | `ocr_completed`      |
| Extraction confidence is below threshold | `needs_human_review` |
| Extraction fails                         | `failed`             |

##  Audit Events Added
| Audit Event            | Meaning                                         |
| ---------------------- | ----------------------------------------------- |
| `EXTRACTION_STARTED`   | Extraction Lambda began processing the document |
| `EXTRACTION_COMPLETED` | Extraction completed and result was stored      |
| `EXTRACTION_FAILED`    | Extraction failed and the error was recorded    |

## Security Justification

This stage improves the pipeline because extraction is handled by a separate Lambda with a separate IAM policy and queue trigger. The function only consumes messages from the extraction queue and writes safe structured logs.
The output is stored in Supabase rather than CloudWatch. CloudWatch logs contain metadata such as document ID, processing run ID, confidence score, and status, but not raw document contents.

## Why Mock Extraction Is Used First

Mock extraction is used before Bedrock or SageMaker to prove the pipeline mechanics independently of AI model behavior, model cost, prompt design, and provider-specific integration issues.
This makes the architecture easier to test and provides a stable base for replacing the mock logic with a real OCR/LLM adapter later.
