# Project Documentation

This directory contains the stage-by-stage implementation record, threat/risk artefacts, NIST CSF 2.0 mapping, evidence index and progress history for the Capisso DEW cloud security prototype.

## Development Stages

| Stage | Document | Status |
|---|---|---|
| 0 | [AWS API Gateway and Lambda Prototype](stage-0-api-gateway-lambda-prototype.md) | Completed and tested |
| 1 | [Secure Upload and S3 Pre-signed URL Flow](stage-1-secure-upload-s3.md) | Completed and tested |
| 2 | [Supabase Document Metadata and Audit Logging](stage-2-database-audit.md) | Completed and tested |
| 3 | [Event-Driven Pre-processing](stage-3-event-driven-preprocessing.md) | Completed and tested |
| 4 | [Mock Extraction Pipeline](stage-4-mock-extraction.md) | Completed and tested |
| 5A | [Real Model Service Attempt](stage-5a-real-model-attempt.md) | Attempted; blocked by AWS account restrictions |
| 5B | [Secure AI Model Adapter Design](stage-5b-secure-model-adapter-design.md) | Design completed; real invocation deferred |
| 5C | [Post-processing Validation and HITL Routing](stage-5c-postprocessing-hitl.md) | Completed and tested |
| 6 | [Monitoring, Alerting and Incident Response](stage-6-monitoring-incident-response.md) | Completed and tested |
| 7 | [Retention and Secure Deletion](stage-7-retention-secure-deletion.md) | Completed and tested |
| 8 | [Access, Secret and API-Abuse Hardening](stage-8-access-secret-api-hardening.md) | Completed and tested |
| 9 | NIST CSF 2.0 Current/Target Profile and security evaluation | Next evaluation stage |

## Security and Evaluation Documents

- [NIST CSF 2.0 Framework Mapping](nist-csf-2-framework-mapping.md)
- [STRIDE Threat Model](threat-model.md)
- [Risk Register](risk-register.md)
- [AWS Lambda Function Map](aws-lambda-function-map.md)
- [Progress Log](progress-log.md)
- [Evidence Index](evidence/README.md)

## Documentation Principle

Each stage document distinguishes implemented/tested work, design-only work, deferred work, evidence, security value and known limitations.

Historical entries in the progress log are retained as point-in-time records. Earlier entries may therefore contain next-step statements that were later completed. The most recent stage entry and the root `README.md` represent the current implementation status.

No document should be interpreted as evidence of real-model extraction accuracy. Real AWS model execution remains deferred because the account used for the prototype did not provide the required service access.
