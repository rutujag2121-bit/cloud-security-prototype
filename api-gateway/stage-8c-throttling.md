# Stage 8C — API Gateway Throttling and Abuse Protection

## Status
Implemented and tested.

## Configuration

REST API stage: `Dev`

Stage-level throttling:
```text
Rate: 5 requests/second
Burst: 10 requests
```

`POST /upload` method override:
```text
Rate: 2 requests/second
Burst: 2 requests
```

The API was redeployed after the change.

## Controlled burst test

A PowerShell concurrent burst test generated fifteen requests.

Observed result included:
```text
HTTP 200 responses
HTTP 429 Too Many Requests
```

This demonstrated that excessive traffic can be rejected at the API boundary before all requests reach downstream Lambda/Supabase processing.

## Monitoring

CloudWatch alarm:
```text
capisso-api-high-4xx-errors
```

Metric:
```text
API Gateway 4XXError
Statistic: Sum
Period: 1 minute
```

Final prototype threshold:
```text
>= 5
```

The test graph recorded the generated 4XX response. A temporary lower threshold may be used only to prove alarm/SNS delivery, after which the threshold should be restored.

## Limitation

API Gateway throttling is a best-effort control and is not presented as complete denial-of-service protection.
