# Progress Log

## 23 June 2026 — AWS API Gateway and Lambda Prototype

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
