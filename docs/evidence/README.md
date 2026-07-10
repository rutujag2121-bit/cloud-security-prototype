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
