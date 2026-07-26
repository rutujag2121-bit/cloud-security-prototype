# Planned Bedrock Extraction IAM Policy

The policy template in `iam-bedrock-extraction-policy-template.json` defines the proposed least-privilege permissions for invoking Amazon Nova Lite from the extraction Lambda.

## Status

This policy is a planned implementation artefact.

It has not been deployed because the current AWS account does not provide billing-enabled access to Amazon Bedrock or the required paid AI services.

## Required substitutions

Before deployment, replace:

- `<AWS_ACCOUNT_ID>`
- `<EXTRACTION_QUEUE_NAME>`
- `<DOCUMENT_BUCKET_NAME>`
- `<EXTRACTION_LAMBDA_NAME>`

## Security rationale

The extraction Lambda is permitted to:

1. Consume only the designated extraction queue.
2. Read only documents from the S3 `raw/` prefix.
3. Invoke only Amazon Nova Lite.
4. Write operational logs only to its own CloudWatch log group.

The policy does not grant document deletion, unrestricted S3 access, unrestricted Bedrock access or access to unrelated AWS resources.
