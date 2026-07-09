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
| Invalid file type rejected | Pending |
| Oversized file rejected | Pending |
| Extension/content-type mismatch rejected | Pending |
| CloudWatch safe log generated | Pending |

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

```text
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
