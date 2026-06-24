# API Gateway Endpoints

## API Name
document-processing-rest-api

## Stage
Dev

## Implemented Endpoint

### POST /upload

Purpose:
Accepts document metadata for receipt/invoice upload and creates an initial document-processing job.

Request body:

```json
{
  "fileName": "receipt1.pdf",
  "contentType": "application/pdf",
  "fileSizeBytes": 250000
}


Expected response:

When tested through API Gateway, the method returns HTTP `200` at the API Gateway execution level because API Gateway successfully invokes the Lambda function. Inside the response body, the Lambda returns `statusCode: 201`, which means the upload request was accepted and a new document-processing job was created.

```json
{
  "statusCode": 201,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "POST,OPTIONS"
  },
  "body": "{\"message\": \"Document upload request accepted\", \"jobId\": \"generated-uuid\", \"fileName\": \"receipt1.pdf\", \"contentType\": \"application/pdf\", \"fileSizeBytes\": 250000, \"status\": \"received\", \"receivedAt\": \"timestamp\"}"
}
```

Example successful output:

```json
{
  "statusCode": 201,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "POST,OPTIONS"
  },
  "body": "{\"message\": \"Document upload request accepted\", \"jobId\": \"44fc7da4-b198-43e6-b8eb-8cc228cd9cb6\", \"fileName\": \"receipt1.pdf\", \"contentType\": \"application/pdf\", \"fileSizeBytes\": 250000, \"status\": \"received\", \"receivedAt\": \"2026-06-23T16:07:21.533069Z\"}"
}
```
