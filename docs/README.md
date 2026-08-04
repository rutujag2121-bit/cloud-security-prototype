# Project Documentation

This directory contains the stage-by-stage implementation record and the security-framework artefacts for the Capisso DEW cloud security prototype.

## Development Stages

| Stage | Document | Status |
|---|---|---|
| 0 | [AWS API Gateway and Lambda Prototype](stage-0-api-gateway-lambda-prototype.md) | Completed and tested |
| 1 | [Secure Upload and S3 Pre-signed URL Flow](stage-1-secure-upload-s3.md) | Completed and tested |
| 2 | [Supabase Document Metadata and Audit Logging](stage-2-database-audit.md) | Completed and tested |
| 3 | [Event-Driven Pre-processing](stage-3-event-driven-preprocessing.md) | Completed and tested |
| 4 | [Mock Extraction Pipeline](stage-4-mock-extraction.md) | Completed and tested |
| 5A | [Real Model Service Attempt](stage-5a-real-model-attempt.md) | Attempted; blocked by AWS account restrictions |
| 5B | [Secure AI Model Adapter Design](stage-5b-secure-model-adapter-design.md) | Design completed; invocation deferred |
| 5C | [Post-processing Validation and HITL Routing](stage-5c-postprocessing-hitl.md) | Completed and tested |
| 6 | Monitoring, Alerting and Incident Response | Next implementation stage |

## Security and Evaluation Documents

- [NIST CSF 2.0 Framework Mapping](nist-csf-2-framework-mapping.md)
- [STRIDE Threat Model](threat-model.md)
- [Risk Register](risk-register.md)
- [AWS Lambda Function Map](aws-lambda-function-map.md)
- [Progress Log](progress-log.md)
- [Evidence Index](evidence/)

## Documentation Principle

Each stage document distinguishes:

- Implemented and tested work.
- Design-only work.
- Deferred work.
- Test evidence.
- Security value.
- Known limitations and residual risks.

No stage should be interpreted as evidence of real-model accuracy unless a real model was successfully executed and evaluated.
