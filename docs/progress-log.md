# Progress Log

## AWS API Gateway and Lambda Prototype

Completed:
- Created AWS REST API using API Gateway.
- Created `/upload` resource.
- Added POST method under `/upload`.
- Created `document-processing-upload-lambda`.
- Implemented file metadata validation.
- Added allowed file types: PDF, JPEG, PNG.
- Added file size validation.
- Added filename safety validation.
- Generated unique `jobId` using UUID.
- Tested Lambda directly.
- Tested API Gateway `/upload` POST method successfully.

Test result:
- API Gateway invoked Lambda successfully.
- Lambda returned `statusCode: 201`.
- Response included generated `jobId`.
- Initial processing status returned as `received`.

Issue encountered:
- Initial Lambda code expected request data inside `event["body"]`.
- API Gateway test passed JSON fields directly in the event object.
- Lambda code was updated to support both formats.

Next steps:
- Add GET `/status` endpoint.
- Connect metadata storage to Supabase PostgreSQL.
- Investigate Supabase Storage for document files.
- Move later to AWS Bedrock/SageMaker processing.


## Secure Upload Upgrade — S3 Pre-signed URL Flow

Completed:
- Created dedicated S3 bucket for document storage.
- Added S3 prefixes: `raw/`, `processed/`, `rejected/`, and `audit-artifacts/`.
- Enabled S3 Block Public Access.
- Enabled default S3 server-side encryption.
- Added Lambda environment variables for bucket name, upload prefix, max file size, CORS origin, and pre-signed URL expiry.
- Added least-privilege IAM policy allowing the upload Lambda to put objects only into the S3 `raw/` prefix.
- Updated Lambda code to validate metadata and generate a pre-signed S3 upload URL.
- Increased file size limit from 5 MB to 10 MB.
- Replaced wildcard CORS design with configurable allowed origins.
- Added safe structured logs with trace IDs.
- Added test events for valid upload, invalid file type, oversized file, and extension mismatch.

### S3 Upload Test Completed

A valid upload initiation request was tested through AWS Lambda. The Lambda returned `statusCode: 201`, generated a `documentId`, created a structured S3 object key, and returned a pre-signed S3 PUT URL.

The pre-signed URL was then tested in Postman using:

- Method: `PUT`
- Header: `Content-Type: application/pdf`
- Body: binary PDF file

The upload returned `200 OK`, confirming that the generated pre-signed URL successfully uploads the document into the S3 `raw/` prefix.

Security significance:
- The document is uploaded directly to S3 instead of passing through Lambda as a large payload.
- The S3 object path is structured by company ID, user ID, and document ID.
- The upload URL is short-lived and is not committed to GitHub.
- The uploaded document is stored in a bucket with public access blocked and encryption enabled.

Next steps:
- Test rejection cases: invalid file type, oversized file, and extension/content-type mismatch.
- Add Supabase PostgreSQL document metadata table.
- Add audit log table.
- Add S3/SQS-triggered pre-processing Lambda.

### Upload Validation Tests Completed

The upload initiation Lambda was tested using the repository test events:

- `test-events/invalid-file-type.json`
- `test-events/oversized-file.json`
- `test-events/extension-mismatch.json`

All rejection test cases returned the expected `400` response.

Security significance:
- Unsupported executable-style files are rejected.
- Files over the 10 MB limit are rejected.
- Mismatched file extension and content type combinations are rejected.
- The Lambda only generates S3 pre-signed upload URLs for valid PDF, JPEG, or PNG metadata.

This confirms that the upload boundary now enforces basic secure API validation before allowing document storage in S3.

## Stage 3 Progress — Event-Driven Pre-processing

Completed:
- Created SQS dead-letter queue `capisso-preprocess-dlq`.
- Created SQS main queue `capisso-preprocess-queue`.
- Configured the main queue to use the DLQ with maximum receives set to 3.
- Added SQS access policy so the S3 document bucket can send ObjectCreated events to the queue.
- Configured S3 event notification for the `raw/` prefix.
- Created pre-processing Lambda function.
- Added least-privilege IAM permissions for S3 raw object read, SQS message processing, and CloudWatch logging.
- Attached SQS trigger to the pre-processing Lambda.
- Deployed pre-processing Lambda code.
- Tested end-to-end upload event flow from S3 to SQS to Lambda.
- Confirmed CloudWatch logging for the pre-processing stage.
- Confirmed Supabase status/audit updates where applicable.

Why this was implemented:
- The previous stage created secure upload URLs but did not automatically start processing after upload.
- This stage introduces an event-driven processing skeleton.
- SQS provides buffering, retries, and dead-letter handling.
- The pre-processing Lambda validates uploaded objects before they move to OCR/model extraction.
- Supabase status and audit records improve traceability and compliance evidence.

Security value:
- Improves lifecycle tracking.
- Supports failure handling through DLQ.
- Keeps Lambda permissions scoped to required resources.
- Avoids logging document content or PII.
- Provides traceable status changes for uploaded documents.

Next steps:
- Add OCR/model extraction stage.
- Add processed result schema.
- Add confidence scoring.
- Add HITL routing for low-confidence results.
- Add CloudWatch alarms for failed processing.
