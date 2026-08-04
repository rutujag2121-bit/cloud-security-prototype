# Stage 5C — Post-processing Validation and Human-in-the-Loop Routing

## 1. Objective

Stage 5C adds deterministic validation and Human-in-the-Loop (HITL) routing after extraction. The purpose is to prevent structurally invalid, incomplete, mathematically inconsistent, low-confidence or potentially adversarial model output from being accepted automatically.

## 2. Processing Flow

```text
Extraction output
→ schema and type checks
→ required-field checks
→ date and currency validation
→ financial-consistency checks
→ confidence evaluation
→ prompt-injection indicator scan
→ validation result stored
→ review task created when required
→ audit and CloudWatch evidence recorded
```

## 3. Database Changes

The `extraction_results` table was extended with:

- `schema_version`
- `validation_status`
- `validation_errors`
- `review_reasons`
- `validated_at`

The `review_tasks` table was created to support the lifecycle:

```text
pending → in_review → approved / corrected / rejected
```

Row Level Security is enabled on `review_tasks`. The prototype backend currently uses the Supabase service-role key; user-facing RLS policies remain a production requirement.

## 4. Implemented Validation Controls

The extraction Lambda now checks:

- Required fields: supplier, date, currency and total
- ISO date format: `YYYY-MM-DD`
- Three-letter uppercase currency format
- Non-negative monetary values
- Allowed document categories
- Line-item array structure
- Subtotal plus tax against total
- Line-item sum against subtotal
- Overall and field-level confidence thresholds
- Model-reported uncertainty
- Prompt-injection indicator phrases
- Malformed or non-schema model output

CloudWatch logs contain validation metadata and trace identifiers, not full document contents or credentials.

## 5. Deterministic Security Tests

| Scenario | Expected validation status | Expected document status | Review priority |
|---|---|---|---|
| Valid output | `valid` | `ocr_completed` | No task |
| Low confidence | `review_required` | `needs_human_review` | Medium |
| Missing required field | `review_required` | `needs_human_review` | High |
| Financial mismatch | `review_required` | `needs_human_review` | High |
| Prompt-injection indicator | `review_required` | `needs_human_review` | High |
| Malformed output | `invalid` | `needs_human_review` | High |

All scenarios were executed through direct Lambda SQS-style test events because the existing upload pipeline had already been tested previously. This Stage 5C test set isolates post-processing and HITL behaviour.

## 6. Security Value

The implementation demonstrates that:

- AI confidence is not treated as proof of correctness.
- Financial values are checked using deterministic business rules.
- Uncertain or suspicious output is blocked from automatic completion.
- Review decisions are recorded in structured database fields.
- High-risk cases are prioritised.
- Audit events and trace IDs support investigation.
- Model output is treated as untrusted data.

## 7. Limitations

- The extraction provider remains a deterministic mock adapter.
- Prompt-injection detection is pattern-based and cannot detect all attacks.
- The reviewer user interface is not implemented.
- Authenticated tenant-aware RLS policies remain future work.
- Real Bedrock, SageMaker or Textract execution requires suitable AWS credentials.
