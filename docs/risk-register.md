# Security Risk Register

## 1. Purpose

This risk register prioritises the threats identified in the STRIDE threat model.

Risk is calculated as:

```text
Risk score = Likelihood × Impact
```
## 2. Rating Scale
### Likelihood
| Score | Meaning        |
| ----: | -------------- |
|     1 | Rare           |
|     2 | Unlikely       |
|     3 | Possible       |
|     4 | Likely         |
|     5 | Almost certain |

### Impact
| Score | Meaning    |
| ----: | ---------- |
|     1 | Negligible |
|     2 | Minor      |
|     3 | Moderate   |
|     4 | Major      |
|     5 | Severe     |

### Risk level
| Score | Level    |
| ----: | -------- |
|   1–4 | Low      |
|   5–9 | Medium   |
| 10–16 | High     |
| 17–25 | Critical |

## 3. Risk Register
| Risk ID | Related threat | Risk description                                                                         | Likelihood | Impact | Inherent score | Current controls                                              | Residual score | Treatment | Priority action                                                           |
| ------- | -------------- | ---------------------------------------------------------------------------------------- | ---------: | -----: | -------------: | ------------------------------------------------------------- | -------------: | --------- | ------------------------------------------------------------------------- |
| R-01    | T-01           | Unauthenticated users may obtain upload URLs and submit documents under false identities |          4 |      4 |        16 High | Metadata validation and structured identifiers                |        12 High | Mitigate  | Add authentication and verified user/company claims in production         |
| R-02    | T-02           | Leaked pre-signed URLs may be used by unauthorised parties before expiry                 |          3 |      4 |        12 High | Short expiry and fixed S3 key                                 |       8 Medium | Mitigate  | Reduce expiry where practical and bind requests to authenticated sessions |
| R-03    | T-03           | Malicious or incorrectly labelled files may reach document parsers or models             |          4 |      4 |        16 High | Extension, content-type and size validation                   |        12 High | Mitigate  | Add file-signature verification and malware-scanning design               |
| R-04    | T-04           | API or upload abuse may create processing backlog and unexpected cloud cost              |          3 |      4 |        12 High | Size limit and asynchronous queues                            |       9 Medium | Mitigate  | Configure API Gateway throttling and monitoring                           |
| R-05    | T-05           | Incorrect S3 access configuration may expose sensitive documents                         |          2 |      5 |        10 High | Block Public Access and encryption                            |       5 Medium | Mitigate  | Add configuration-review evidence and policy checks                       |
| R-06    | T-06           | Overprivileged or compromised Lambda roles may access unrelated resources                |          3 |      5 |        15 High | Separate least-privilege IAM policies                         |       8 Medium | Mitigate  | Review resource-level permissions and remove unused actions               |
| R-07    | T-07           | Forged, modified or replayed SQS messages may cause duplicate or unauthorised processing |          3 |      4 |        12 High | Restricted queue access and structured IDs                    |       9 Medium | Mitigate  | Add schema validation and idempotent processing checks                    |
| R-08    | T-09           | PII, credentials or temporary URLs may be exposed through logs                           |          3 |      5 |        15 High | Safe structured logging                                       |       8 Medium | Mitigate  | Conduct log review and document prohibited log fields                     |
| R-09    | T-10           | Supabase service-role key compromise may provide privileged database access              |          3 |      5 |        15 High | Environment-variable storage and secret exclusion from GitHub |        10 High | Mitigate  | Use managed secret storage and define key-rotation procedure              |
| R-10    | T-11           | Incomplete RLS policies may allow cross-company data access                              |          3 |      5 |        15 High | Company/user fields and RLS enabled                           |        12 High | Mitigate  | Add or explicitly document production RLS policy requirements             |
| R-11    | T-12           | Prompt injection embedded in uploaded documents may influence the model                  |          4 |      4 |        16 High | Fixed prompt and document-as-untrusted-data instruction       |        12 High | Mitigate  | Test adversarial documents once Bedrock credentials are available         |
| R-12    | T-13           | Hallucinated or malformed extraction values may be stored as valid financial data        |          4 |      5 |    20 Critical | JSON schema and planned HITL decision                         |        15 High | Mitigate  | Implement post-processing and financial consistency validation            |
| R-13    | T-14           | Low-confidence output may incorrectly bypass human review                                |          3 |      4 |        12 High | Confidence threshold and review flag                          |       9 Medium | Mitigate  | Add deterministic low-confidence and malformed-output tests               |
| R-14    | T-15           | Failed queue messages may remain unnoticed and cause processing loss                     |          3 |      4 |        12 High | DLQs and retry limits                                         |       8 Medium | Mitigate  | Add DLQ alarms and investigation/replay runbook                           |
| R-15    | T-16           | Missing retention and deletion enforcement may violate privacy obligations               |          4 |      4 |        16 High | Planned lifecycle statuses                                    |        12 High | Mitigate  | Define retention period and secure deletion workflow                      |
| R-16    | T-17           | Sensitive configuration or evidence may be committed to the public repository            |          3 |      5 |        15 High | Placeholders, `.gitignore` and evidence sanitisation          |       8 Medium | Mitigate  | Perform repository secret and evidence review                             |
| R-17    | T-18           | Security failures may continue without alarms or incident response                       |          3 |      4 |        12 High | CloudWatch logs and audit records                             |       9 Medium | Mitigate  | Configure alarms and document response responsibilities                   |

## 4. Priority Order
The immediate implementation priorities are:
| Rank | Risk | Required action                                      |
| ---: | ---- | ---------------------------------------------------- |
|    1 | R-12 | Implement post-processing and financial validation   |
|    2 | R-11 | Finalise prompt-injection controls and test plan     |
|    3 | R-10 | Define tenant-isolation and RLS requirements         |
|    4 | R-09 | Document secret-management and rotation controls     |
|    5 | R-15 | Define retention and secure deletion                 |
|    6 | R-03 | Strengthen uploaded-file validation                  |
|    7 | R-14 | Add DLQ alarms and replay procedure                  |
|    8 | R-17 | Add monitoring alarms and incident-response guidance |

## 5. Residual Risk

Some risks remain because the project is a prototype and the available AWS account does not support real Bedrock, SageMaker or Textract execution.
These limitations will be documented rather than represented as completed controls.
The risk register will be updated after:
- Post-processing implementation
- HITL routing tests
- Monitoring configuration
- NIST Current and Target Profile analysis
- Final security evaluation
