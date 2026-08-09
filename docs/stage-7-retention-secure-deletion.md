# Stage 7 — Retention and Secure Deletion

## Status
**Implemented and tested**

## Objective
Stage 7 completes the document lifecycle by adding retention metadata, controlled deletion, deletion evidence, expiry enforcement, scheduling and monitoring.

```text
Manual deletion request OR retention expiry
→ Secure Deletion Lambda
→ S3 deletion and verification
→ audit redaction
→ database deletion
→ minimal deletion tombstone
→ sanitised completion evidence
```

Automatic enforcement uses:

```text
EventBridge Scheduler
→ Retention Lambda
→ eligible expired documents
→ Secure Deletion Lambda
```

## 7A — Retention and deletion schema
The `documents` table was extended with `retention_until`, `retention_policy` and `retention_enforcement_enabled`.

The prototype uses a 30-day interval only to exercise retention controls. It is not presented as a universal GDPR or legal retention period.

The `deletion_requests` table preserves minimal non-content evidence including a SHA-256 document fingerprint, request type, operation status, deletion results, trace ID and timestamps.

## 7B — Dedicated secure-deletion Lambda
Function: `document-processing-deletion-lambda`

The Lambda validates the request, obtains the trusted S3 location from Supabase, restricts deletion to the configured bucket and `raw/` prefix, deletes and verifies the S3 object, redacts identifying audit metadata, hard-deletes the document record, relies on existing cascades for dependent processing data, preserves a minimal tombstone and writes a sanitised `SECURE_DELETION_COMPLETED` audit event.

The caller cannot submit an arbitrary S3 key.

The S3 execution role is limited to `s3:GetObject` and `s3:DeleteObject` for the `raw/*` prefix.

## 7B negative tests
- Invalid UUID: rejected before destructive action.
- Valid but unknown UUID: returned not found without deletion.
- CloudWatch logged only safe operational metadata.

## 7C — Manual secure-deletion test
A disposable document was selected and its before-state recorded.

The test confirmed:
- S3 raw object removed.
- `documents` row removed.
- Associated `processing_runs`, `extraction_results` and `review_tasks` removed through database cascades.
- Identifying audit metadata redacted.
- Minimal deletion tombstone preserved.
- Sanitised completion event preserved.
- Repeated deletion request handled idempotently.

## 7D — Retention-expiry enforcement
Function: `document-processing-retention-lambda`

The retention Lambda identifies expired records and invokes the deletion Lambda. It has no S3 deletion permission.

For `requestType=retention`, the deletion Lambda independently checks the stored retention deadline.

A future deadline was rejected. A controlled expiry was simulated on a disposable document and the expired record was successfully deleted through the same secure-deletion workflow.

## 7E — Scheduled enforcement and monitoring
Historical records were initially protected with `retention_enforcement_enabled=false`. New documents default to automatic enforcement.

Automatic selection requires:

```text
retention_until <= current time
AND
retention_enforcement_enabled = true
```

An EventBridge Scheduler schedule named `capisso-retention-enforcement` was tested with a short interval and then changed to `rate(1 day)`.

A scheduler delivery DLQ named `capisso-retention-scheduler-dlq` was created.

Monitoring includes:
- `capisso-retention-lambda-errors`
- `capisso-retention-scheduler-dlq-messages`

The scheduled invocation was tested successfully without deleting protected historical records.

## Security value
- Explicit retention metadata.
- Restricted destructive IAM.
- Separation of retention selection from deletion execution.
- Independent expiry validation.
- S3 deletion verification.
- Database cascade cleanup.
- Audit-data minimisation.
- Minimal tombstones.
- Idempotent repeated deletion handling.
- Controlled scheduled enforcement.
- Monitoring for invocation and delivery failures.

## Limitations
- 30 days is a prototype policy value, not a universal legal rule.
- Supabase service-role credentials remain in Lambda environment variables pending Stage 8 hardening.
- Versioned-object deletion would require explicit version handling.
- Automatic enforcement was evaluated at prototype scale.
- There is no legal-policy engine selecting retention by document class or jurisdiction.
- Scheduler and alarm configuration remain console-managed rather than infrastructure-as-code.
