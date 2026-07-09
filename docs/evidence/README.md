# Evidence Folder

This folder lists implementation evidence collected during the cloud security prototype build.

## Week 1 Evidence Checklist

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
