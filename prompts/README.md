# Model Prompt and Output Validation Artefacts

This folder contains the planned prompt and output schema for Amazon Bedrock document extraction.

## Files

| File | Purpose |
|---|---|
| `bedrock-receipt-extraction-prompt.md` | Defines secure extraction instructions for the selected multimodal model |
| `receipt-extraction-schema.json` | Defines the application-level JSON validation contract |

## Current Status

These artefacts are prepared for credential-based testing.

They have not yet been executed against Amazon Bedrock because the current AWS account does not provide the required billing-enabled model access.

## Security Purpose

The prompt and schema address:

- Prompt injection contained inside uploaded documents
- Hallucinated or unsupported field values
- Unexpected model-output properties
- Invalid date and currency formats
- Negative financial values
- Missing mandatory fields
- Financial inconsistencies
- Human-review routing

Model output must not be accepted solely because it is valid JSON. It must also pass application-level schema and financial validation.
