# Evidence Folder

This folder lists implementation evidence collected during the cloud security prototype build.

##  Evidence Checklist

| Evidence Item | Status |
|---|---|
| S3 bucket created | Completed |
| S3 Block Public Access enabled | Completed |
| S3 default encryption enabled | Completed |
| S3 prefixes created: raw, processed, rejected, audit-artifacts | Completed |
| Lambda IAM inline policy attached | Completed |
| Lambda environment variables configured | Completed |
| Valid upload initiation test passed | Completed |
| S3 object uploaded through pre-signed URL | Completed |
| Invalid file type rejected | Completed |
| Oversized file rejected | Completed |
| Extension/content-type mismatch rejected | Completed |
| CloudWatch safe log generated | Completed |

## Successful Upload Initiation Test

The Lambda upload initiation test returned `statusCode: 201` and generated:

- `documentId`
- `jobId`
- `status: upload_url_created`
- S3 `objectKey`
- pre-signed S3 PUT upload URL
- `traceId`
- `createdAt` timestamp

The full pre-signed URL is not committed to GitHub because it is a temporary upload credential.

## Successful S3 Upload Test

The generated pre-signed URL was tested using Postman.

Test configuration:

Method: PUT
Header: Content-Type = application/pdf
Body: binary PDF file

result :
200 ok

{
  "statusCode": 201,
  "body": {
    "message": "Secure upload URL created",
    "documentId": "generated-uuid",
    "jobId": "generated-uuid",
    "status": "upload_url_created",
    "bucket": "capisso-documents-dev-rutuja-731039144759-ap-southeast-2-an",
    "objectKey": "raw/capisso-test/test-user-1/generated-uuid/receipt1.pdf",
    "uploadUrl": "[REDACTED]",
    "uploadMethod": "PUT",
    "requiredHeaders": {
      "Content-Type": "application/pdf"
    },
    "expiresInSeconds": 900,
    "traceId": "aws-request-id",
    "createdAt": "timestamp"
  }
}
## Upload Validation Rejection Tests

The Lambda upload initiation function was tested against invalid upload metadata to confirm that unsupported or unsafe files are rejected before an S3 upload URL is generated.

| Test Case | Expected Result | Status |
|---|---|---|
| Unsupported file type: `application/x-msdownload` | `400` error response | Passed |
| Oversized file greater than 10 MB | `400` error response | Passed |
| Extension/content-type mismatch | `400` error response | Passed |

These tests confirm that the upload API does not create pre-signed S3 URLs for unsupported, oversized, or inconsistent file metadata.

| Supabase documents table created | Completed |
| Supabase audit_logs table created | completedt |
| Upload initiation created document record | completed |
| Upload initiation created audit record | completed |
| CloudWatch log with databaseWrite completed | completed |

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

## Stage 3 Evidence Handling Rule

Screenshots are stored locally unless cropped and sanitized. Do not commit AWS account IDs, full ARNs where unnecessary, pre-signed URLs, access tokens, Supabase service-role keys, or real receipt/invoice data.


