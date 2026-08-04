# Stage 0: AWS API Gateway and Lambda Prototype

## Status

**Completed and tested**

## Objective

Create the first working API entry point for the document-processing prototype and confirm that Amazon API Gateway could invoke an AWS Lambda function successfully.

Stage 0 established the baseline request-validation flow before secure S3 upload, persistent database records, asynchronous processing and AI extraction were introduced.

## Why This Stage Was Needed

The project first needed a small, testable API prototype that could:

- Receive receipt or invoice metadata.
- Validate the request.
- Generate a unique processing identifier.
- Return a structured response.
- Prove that API Gateway and Lambda were integrated correctly.

Without this baseline, later security and processing stages would have been harder to isolate and troubleshoot.

## Initial Architecture

```text
API client or API Gateway test
→ POST /upload
→ Amazon API Gateway
→ document-processing-upload-lambda
→ Metadata validation
→ UUID job identifier
→ Structured HTTP response
```

## Implemented Work

| Area | Implementation |
|---|---|
| REST API | Created an Amazon API Gateway REST API |
| Upload resource | Created the `/upload` resource |
| HTTP method | Added `POST /upload` |
| Lambda function | Created `document-processing-upload-lambda` |
| Required metadata | Validated file name, content type and file size |
| Allowed file types | Restricted metadata to PDF, JPEG and PNG |
| File-size validation | Rejected invalid or excessive file-size values |
| Filename validation | Added basic filename-safety checks |
| Processing identifier | Generated a UUID-based `jobId` |
| Lambda testing | Tested the Lambda directly |
| API testing | Tested the API Gateway method successfully |

## Request-Handling Correction

The first Lambda version expected request data only inside:

```python
event["body"]
```

During API Gateway testing, the test console supplied JSON fields directly in the event object.

The Lambda was updated to support both formats:

```text
API Gateway proxy-style body
or
direct Lambda/API Gateway test event
```

This correction made the prototype more reliable during development and testing.

## Test Result

The API Gateway test confirmed:

- API Gateway invoked the upload Lambda successfully.
- The Lambda returned HTTP status `201`.
- The response contained a generated `jobId`.
- The initial processing status was returned as `received`.

This established a working API-to-Lambda integration.

## Security Value

| Security Area | Stage 0 Contribution |
|---|---|
| Input validation | Rejected unsupported metadata before processing |
| File-type restriction | Allowed only PDF, JPEG and PNG metadata |
| File-size control | Prevented unrestricted size declarations |
| Traceability foundation | Created a unique job identifier |
| Controlled response | Returned structured success and error responses |
| Incremental development | Created a small baseline that later controls could strengthen |

## Limitations

Stage 0 was an initial prototype and did not yet provide:

- Direct file upload to protected cloud storage.
- S3 encryption or Block Public Access.
- Short-lived pre-signed upload URLs.
- Persistent document metadata.
- Business-level audit logging.
- Event-driven processing.
- Dead-letter queue handling.
- AI or OCR extraction.
- Human-in-the-Loop routing.

The `/upload` endpoint is therefore retained as the initial prototype endpoint. The stronger secure upload flow was introduced in Stage 1 using `POST /upload/initiate`.

## Evidence

Relevant evidence includes:

- API Gateway `/upload` resource and `POST` method.
- Upload Lambda configuration.
- Successful Lambda direct test.
- Successful API Gateway method test.
- HTTP `201` response containing a generated `jobId`.
- GitHub history showing the initial Lambda implementation and correction.

Sensitive AWS account identifiers are not included in the public documentation.

## Outcome

Stage 0 proved that the initial API request could be validated and processed by Lambda.

```text
API request
→ validation
→ unique job identifier
→ successful structured response
```

This baseline enabled Stage 1 to replace metadata-only processing with a secure S3 pre-signed upload workflow.
